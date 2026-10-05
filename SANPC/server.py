from __future__ import annotations

import hashlib
import hmac
import getpass
import json
import mimetypes
import os
import secrets
import sqlite3
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from http.cookies import SimpleCookie
from typing import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
ADMIN_DIR = ROOT / "admin"
DATA_DIR = Path(os.environ.get("SANPC_DATA_DIR", ROOT / "data")).resolve()
UPLOAD_DIR = DATA_DIR / "uploads"
DATABASE = DATA_DIR / "sanpc.sqlite3"
ADMIN_FILE = ADMIN_DIR / "admin.html"
MAX_REQUEST_BYTES = 8 * 1024 * 1024
MAX_IMAGE_BYTES = 7 * 1024 * 1024
SESSION_SECONDS = 8 * 60 * 60
PASSWORD_ITERATIONS = 310_000
ALLOWED_CATEGORIES = {"GPU", "CPU", "RAM", "PC bộ", "Màn hình", "Mainboard"}
ALLOWED_CONDITIONS = {"Đã dùng tốt", "Còn bảo hành", "Như mới", "Cần sửa"}
ALLOWED_LOCATIONS = {"Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Tỉnh/thành khác"}
IMAGE_TYPES = {
    "image/jpeg": (".jpg", lambda data: data.startswith(b"\xff\xd8\xff")),
    "image/png": (".png", lambda data: data.startswith(b"\x89PNG\r\n\x1a\n")),
    "image/gif": (".gif", lambda data: data.startswith((b"GIF87a", b"GIF89a"))),
    "image/webp": (".webp", lambda data: len(data) > 12 and data.startswith(b"RIFF") and data[8:12] == b"WEBP"),
}
SESSIONS: dict[str, float] = {}
LOGIN_ATTEMPTS: dict[str, list[float]] = {}


@contextmanager
def connect_db() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    UPLOAD_DIR.mkdir(exist_ok=True)
    with connect_db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                condition TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                image TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def admin_is_configured() -> bool:
    with connect_db() as connection:
        return connection.execute("SELECT 1 FROM admin WHERE id = 1").fetchone() is not None


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def password_digest(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)


def parse_multipart(content_type: str, body: bytes) -> tuple[dict[str, str], tuple[str, bytes] | None]:
    message = BytesParser(policy=policy.default).parsebytes(
        b"Content-Type: " + content_type.encode("ascii", "strict") + b"\r\nMIME-Version: 1.0\r\n\r\n" + body
    )
    if not message.is_multipart():
        raise ValueError("Dữ liệu tải lên không hợp lệ.")

    fields: dict[str, str] = {}
    image: tuple[str, bytes] | None = None
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        if not name:
            continue
        payload = part.get_payload(decode=True) or b""
        filename = part.get_filename()
        if filename:
            if payload:
                image = (part.get_content_type(), payload)
        else:
            charset = part.get_content_charset() or "utf-8"
            fields[name] = payload.decode(charset, errors="replace").strip()
    return fields, image


def image_extension(content_type: str, data: bytes) -> str | None:
    image_type = IMAGE_TYPES.get(content_type.lower())
    if image_type and image_type[1](data):
        return image_type[0]
    return None


class SanpcHandler(BaseHTTPRequestHandler):
    server_version = "SANPC/1.0"

    def log_message(self, format_string: str, *args: object) -> None:
        print(f"{self.address_string()} - {format_string % args}")

    def send_bytes(self, status: int, payload: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.end_headers()
        self.wfile.write(payload)

    def send_json(self, status: int, payload: object, extra_headers: dict[str, str] | None = None) -> None:
        encoded = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(encoded)

    def read_body(self, limit: int = MAX_REQUEST_BYTES) -> bytes:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("Kích thước yêu cầu không hợp lệ.") from error
        if length <= 0 or length > limit:
            raise ValueError("Dữ liệu trống hoặc vượt quá dung lượng cho phép.")
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError("Dữ liệu gửi lên chưa đầy đủ.")
        return body

    def request_json(self) -> dict[str, object]:
        body = self.read_body(16 * 1024)
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("Dữ liệu JSON không hợp lệ.") from error
        if not isinstance(payload, dict):
            raise ValueError("Dữ liệu không hợp lệ.")
        return payload

    def request_is_same_origin(self) -> bool:
        origin = self.headers.get("Origin")
        return not origin or urlsplit(origin).netloc.lower() == self.headers.get("Host", "").lower()

    def session_token(self) -> str | None:
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
        except Exception:
            return None
        morsel = cookie.get("sanpc_session")
        if morsel is None:
            return None
        token = morsel.value
        expires = SESSIONS.get(token)
        if expires is None or expires < time.time():
            SESSIONS.pop(token, None)
            return None
        return token

    def require_admin(self) -> bool:
        if self.session_token():
            return True
        self.send_json(401, {"error": "Vui lòng đăng nhập quản trị."})
        return False

    def do_GET(self) -> None:
        path = unquote(urlsplit(self.path).path)
        if path == "/api/products":
            with connect_db() as connection:
                rows = connection.execute(
                    "SELECT id, title, category, price, condition, location, description, image, created_at "
                    "FROM products ORDER BY created_at DESC"
                ).fetchall()
            products = [dict(row) | {"age": "SANPC cập nhật"} for row in rows]
            self.send_json(200, products)
            return
        if path == "/api/admin/status":
            self.send_json(200, {"configured": admin_is_configured(), "authenticated": self.session_token() is not None})
            return
        if path == "/admin":
            self.send_file(ADMIN_FILE)
            return
        if path.startswith("/uploads/"):
            self.send_file(UPLOAD_DIR / path.removeprefix("/uploads/"), UPLOAD_DIR)
            return
        if path == "/":
            self.send_file(WEB_DIR / "index.html", WEB_DIR)
            return
        if path.startswith("/web/"):
            self.send_file(WEB_DIR / path.removeprefix("/web/"), WEB_DIR)
            return
        if path.startswith("/admin/"):
            self.send_file(ADMIN_DIR / path.removeprefix("/admin/"), ADMIN_DIR)
            return
        self.send_json(404, {"error": "Không tìm thấy trang."})

    def send_file(self, requested: Path, allowed_root: Path = ROOT) -> None:
        try:
            resolved = requested.resolve(strict=True)
            if not resolved.is_relative_to(allowed_root.resolve()) or not resolved.is_file():
                raise FileNotFoundError
            content_type = mimetypes.guess_type(resolved.name)[0] or "application/octet-stream"
            if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
                content_type += "; charset=utf-8"
            self.send_bytes(200, resolved.read_bytes(), content_type)
        except (OSError, RuntimeError):
            self.send_json(404, {"error": "Không tìm thấy trang."})

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if not self.request_is_same_origin():
            self.send_json(403, {"error": "Yêu cầu không cùng nguồn."})
            return
        if path == "/api/admin/login":
            self.login_admin()
        elif path == "/api/admin/logout":
            token = self.session_token()
            if token:
                SESSIONS.pop(token, None)
            self.send_json(200, {"ok": True}, {"Set-Cookie": self.session_cookie("", max_age=0)})
        elif path == "/api/admin/products":
            if self.require_admin():
                self.create_product()
        else:
            self.send_json(404, {"error": "Không tìm thấy API."})

    def login_admin(self) -> None:
        address = self.client_address[0]
        now = time.time()
        recent = [stamp for stamp in LOGIN_ATTEMPTS.get(address, []) if now - stamp < 900]
        if len(recent) >= 8:
            self.send_json(429, {"error": "Bạn thử đăng nhập quá nhiều lần. Hãy đợi 15 phút."})
            return
        try:
            payload = self.request_json()
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
            return
        password = str(payload.get("password", ""))
        with connect_db() as connection:
            row = connection.execute("SELECT salt, password_hash FROM admin WHERE id = 1").fetchone()
        if row is None:
            self.send_json(409, {"error": "Chưa khởi tạo tài khoản quản trị."})
            return
        candidate = password_digest(password, bytes.fromhex(row["salt"])).hex()
        if not hmac.compare_digest(candidate, row["password_hash"]):
            recent.append(now)
            LOGIN_ATTEMPTS[address] = recent
            self.send_json(401, {"error": "Mật khẩu không chính xác."})
            return
        LOGIN_ATTEMPTS.pop(address, None)
        token = self.new_session()
        self.send_json(200, {"ok": True}, {"Set-Cookie": self.session_cookie(token)})

    def new_session(self) -> str:
        token = secrets.token_urlsafe(32)
        SESSIONS[token] = time.time() + SESSION_SECONDS
        return token

    def session_cookie(self, token: str, max_age: int = SESSION_SECONDS) -> str:
        secure = "; Secure" if os.environ.get("SANPC_COOKIE_SECURE") == "1" else ""
        return f"sanpc_session={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={max_age}{secure}"

    def create_product(self) -> None:
        content_type = self.headers.get("Content-Type", "")
        try:
            body = self.read_body()
            if content_type.lower().startswith("multipart/form-data"):
                fields, image_file = parse_multipart(content_type, body)
            else:
                self.send_json(415, {"error": "Cần gửi biểu mẫu sản phẩm."})
                return
            title = fields.get("title", "").strip()
            category = fields.get("category", "")
            condition = fields.get("condition", "")
            location = fields.get("location", "")
            description = fields.get("description", "").strip()
            if not title or len(title) > 100:
                raise ValueError("Tên sản phẩm cần từ 1 đến 100 ký tự.")
            if category not in ALLOWED_CATEGORIES or condition not in ALLOWED_CONDITIONS or location not in ALLOWED_LOCATIONS:
                raise ValueError("Danh mục, tình trạng hoặc khu vực không hợp lệ.")
            try:
                price = int(fields.get("price", ""))
            except ValueError as error:
                raise ValueError("Giá bán cần là số nguyên dương.") from error
            if price <= 0:
                raise ValueError("Giá bán cần lớn hơn 0.")
            if len(description) > 600:
                raise ValueError("Mô tả tối đa 600 ký tự.")

            image = fields.get("image_url", "").strip()
            if image and not image.startswith(("https://", "http://")):
                raise ValueError("Đường dẫn ảnh cần bắt đầu bằng http:// hoặc https://.")
            if image_file:
                uploaded_type, image_data = image_file
                if len(image_data) > MAX_IMAGE_BYTES:
                    raise ValueError("Ảnh tải lên tối đa 7 MB.")
                extension = image_extension(uploaded_type, image_data)
                if not extension:
                    raise ValueError("Ảnh chỉ nhận định dạng JPG, PNG, GIF hoặc WEBP hợp lệ.")
                filename = f"{uuid.uuid4().hex}{extension}"
                (UPLOAD_DIR / filename).write_bytes(image_data)
                image = f"/uploads/{filename}"
            if not image:
                raise ValueError("Hãy tải ảnh sản phẩm lên hoặc nhập đường dẫn ảnh.")

            product_id = uuid.uuid4().hex
            created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            with connect_db() as connection:
                connection.execute(
                    "INSERT INTO products (id, title, category, price, condition, location, description, image, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (product_id, title, category, price, condition, location, description, image, created_at),
                )
            self.send_json(201, {"ok": True, "id": product_id})
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
        except (OSError, sqlite3.Error) as error:
            print(f"Lỗi lưu sản phẩm: {error}", file=sys.stderr)
            self.send_json(500, {"error": "Máy chủ chưa lưu được sản phẩm. Vui lòng thử lại."})

    def do_DELETE(self) -> None:
        path = urlsplit(self.path).path
        if not self.request_is_same_origin():
            self.send_json(403, {"error": "Yêu cầu không cùng nguồn."})
            return
        if not path.startswith("/api/admin/products/"):
            self.send_json(404, {"error": "Không tìm thấy API."})
            return
        if not self.require_admin():
            return
        product_id = path.rsplit("/", 1)[-1]
        with connect_db() as connection:
            row = connection.execute("SELECT image FROM products WHERE id = ?", (product_id,)).fetchone()
            if row is None:
                self.send_json(404, {"error": "Không tìm thấy sản phẩm."})
                return
            connection.execute("DELETE FROM products WHERE id = ?", (product_id,))
        image_path = row["image"]
        if image_path.startswith("/uploads/"):
            stored_image = (UPLOAD_DIR / Path(image_path).name).resolve()
            if stored_image.is_relative_to(UPLOAD_DIR):
                stored_image.unlink(missing_ok=True)
        self.send_json(200, {"ok": True})

    def do_HEAD(self) -> None:
        path = unquote(urlsplit(self.path).path)
        if path == "/":
            requested, allowed_root = WEB_DIR / "index.html", WEB_DIR
        elif path.startswith("/web/"):
            requested, allowed_root = WEB_DIR / path.removeprefix("/web/"), WEB_DIR
        elif path.startswith("/admin/"):
            requested, allowed_root = ADMIN_DIR / path.removeprefix("/admin/"), ADMIN_DIR
        elif path.startswith("/uploads/"):
            requested, allowed_root = UPLOAD_DIR / path.removeprefix("/uploads/"), UPLOAD_DIR
        else:
            self.send_error(404)
            return
        try:
            resolved = requested.resolve(strict=True)
            if not resolved.is_relative_to(allowed_root.resolve()) or not resolved.is_file():
                raise FileNotFoundError
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(resolved.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(resolved.stat().st_size))
            self.end_headers()
        except OSError:
            self.send_error(404)


def create_admin_from_console() -> int:
    if admin_is_configured():
        print("Tài khoản chủ đã tồn tại. Không thể tạo thêm tài khoản.")
        return 1
    print("Tạo tài khoản chủ SANPC. Mật khẩu được nhập ẩn và không in ra màn hình.")
    password = getpass.getpass("Mật khẩu mới (ít nhất 12 ký tự): ")
    if len(password) < 12:
        print("Mật khẩu cần có ít nhất 12 ký tự.")
        return 1
    confirmation = getpass.getpass("Nhập lại mật khẩu: ")
    if not hmac.compare_digest(password, confirmation):
        print("Hai mật khẩu không khớp.")
        return 1
    salt = secrets.token_bytes(16)
    digest = password_digest(password, salt)
    try:
        with connect_db() as connection:
            connection.execute(
                "INSERT INTO admin (id, salt, password_hash) VALUES (1, ?, ?)",
                (salt.hex(), digest.hex()),
            )
    except sqlite3.IntegrityError:
        print("Tài khoản chủ đã tồn tại. Không thể tạo thêm tài khoản.")
        return 1
    print("Đã tạo tài khoản chủ duy nhất. Có thể đăng nhập tại /admin.")
    return 0


def main() -> None:
    initialize_database()
    if len(sys.argv) == 2 and sys.argv[1] == "--create-admin":
        raise SystemExit(create_admin_from_console())
    if len(sys.argv) > 1:
        print("Tùy chọn không hợp lệ. Dùng --create-admin để tạo tài khoản chủ một lần.", file=sys.stderr)
        raise SystemExit(2)
    if not admin_is_configured():
        print("Chưa có tài khoản chủ. Tạo tài khoản bằng lệnh: python server.py --create-admin")
    host = os.environ.get("SANPC_HOST", "127.0.0.1")
    port = int(os.environ.get("SANPC_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), SanpcHandler)
    server.daemon_threads = True
    print(f"\nWebsite: http://{host}:{port}/")
    print(f"Quản trị: http://{host}:{port}/admin\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng máy chủ SANPC.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
