# SANPC storefront

Website bán PC và linh kiện cũ với khu quản trị riêng. Khách chỉ xem sản phẩm và liên hệ SANPC; chỉ người có mật khẩu quản trị mới được đăng hoặc gỡ sản phẩm.

## Cấu trúc thư mục

- `web/`: giao diện khách (`index.html`, `app.js`, `styles.css`).
- `admin/`: giao diện quản trị (`admin.html`, `admin.js`, `admin.css`).
- `server.py`: máy chủ API, xác thực và phục vụ hai giao diện.
- `data/`: database sản phẩm và ảnh upload; thư mục này không nằm trong `web/` hay `admin/`.

## Chạy trên máy Windows

1. Mở PowerShell tại thư mục dự án.
2. Tạo tài khoản chủ đúng một lần bằng `./.venv/Scripts/python.exe server.py --create-admin`. Nhập mật khẩu dài ít nhất 12 ký tự; ký tự sẽ được ẩn khi nhập.
3. Chạy `./run_server.ps1` (nếu Windows chặn script, chạy `powershell -ExecutionPolicy Bypass -File .\run_server.ps1`).
4. Mở `http://127.0.0.1:8000/admin` và đăng nhập bằng mật khẩu vừa tạo.
5. Đăng sản phẩm trong trang quản trị. Sản phẩm sẽ xuất hiện ngay ở `http://127.0.0.1:8000/`.

Trang `/admin` chỉ có đăng nhập, không có chức năng đăng ký hoặc tạo thêm tài khoản. Cơ sở dữ liệu chỉ cho phép một tài khoản chủ; lệnh khởi tạo sẽ từ chối nếu tài khoản đó đã tồn tại. Mật khẩu được lưu dạng băm, không nằm trong mã nguồn. Không chia sẻ mật khẩu quản trị.

## Dữ liệu và triển khai

- Sản phẩm, phiên đăng nhập quản trị và cấu hình được lưu trong `data/sanpc.sqlite3`.
- Ảnh tải lên nằm trong `data/uploads/` (JPG, PNG, GIF, WEBP, tối đa 7 MB).
- Sao lưu định kỳ toàn bộ thư mục `data/`.
- Mặc định server chỉ nghe trên máy đang chạy. Để dùng trong cùng mạng nội bộ, chạy `./run_server.ps1 -Network` rồi truy cập bằng IP nội bộ của máy chủ.
- Để khách ngoài Internet truy cập, cần đưa dự án lên hosting/VPS và cấu hình domain cùng HTTPS qua reverse proxy. Không nên mở trực tiếp server phát triển này ra Internet; khi chạy sau HTTPS proxy, đặt biến môi trường `SANPC_COOKIE_SECURE=1`.

Server chỉ dùng thư viện Python tiêu chuẩn, không cần cài package ngoài.
