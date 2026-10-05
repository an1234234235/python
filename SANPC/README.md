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

## Dữ liệu

- Sản phẩm, phiên đăng nhập quản trị và cấu hình được lưu trong `data/sanpc.sqlite3`.
- Ảnh tải lên nằm trong `data/uploads/` (JPG, PNG, GIF, WEBP, tối đa 7 MB).
- Sao lưu định kỳ toàn bộ thư mục `data/`.
- Mặc định server chỉ nghe trên máy đang chạy. Để dùng trong cùng mạng nội bộ, chạy `./run_server.ps1 -Network` rồi truy cập bằng IP nội bộ của máy chủ.

## Đưa website lên tên miền công khai

Tên miền chỉ là địa chỉ. Để mọi người truy cập được, website cần chạy liên tục trên một VPS/hosting có Docker, có địa chỉ IP công khai; máy tính cá nhân tắt hoặc mất mạng thì website sẽ không truy cập được. Cấu hình dưới đây dùng Caddy làm HTTPS reverse proxy và không mở cổng ứng dụng Python trực tiếp ra Internet.

1. Thuê một VPS Linux có Docker Compose, rồi tải thư mục dự án lên VPS. Cài Docker Engine và Docker Compose plugin theo hướng dẫn của nhà cung cấp VPS.
2. Trong trang quản lý tên miền, tạo bản ghi DNS `A` cho `sanpchoangdung.com` trỏ tới IP công khai của VPS. Tạo thêm bản ghi `A` cho `www` trỏ cùng IP, hoặc bản ghi `CNAME` `www` trỏ về tên miền gốc. Chờ DNS cập nhật.
3. Mở cổng TCP `80` và `443` trong firewall của VPS/nhà cung cấp. Caddy cần các cổng này để phục vụ website và tự cấp/gia hạn chứng chỉ HTTPS.
4. Trong thư mục dự án trên VPS, chạy `cp .env.example .env`. File mẫu đã đặt `DOMAIN=sanpchoangdung.com`, không cần thêm `https://` hay đường dẫn. Nếu đã có sản phẩm trên máy hiện tại và muốn mang sang VPS, hãy sao chép cả thư mục `data/` lên trước khi khởi động.
5. Khởi động website: `docker compose up -d --build`.
6. Tạo mật khẩu quản trị một lần bằng `docker compose exec app python server.py --create-admin`. Dùng mật khẩu dài ít nhất 12 ký tự.
7. Truy cập `https://sanpchoangdung.com/admin` để đăng nhập và `https://sanpchoangdung.com/` để xem cửa hàng; `https://www.sanpchoangdung.com` cũng hoạt động nếu đã tạo DNS ở bước 2.

Docker Compose giữ database và ảnh trong `data/` trên VPS; tất cả khách truy cập cùng xem kho sản phẩm đó. Caddy tự cấu hình HTTPS, còn cookie quản trị chỉ được gửi qua HTTPS. Sao lưu `data/` định kỳ và không xóa thư mục này khi cập nhật website. DNS, VPS và website là các dịch vụ riêng: cần duy trì VPS hoạt động và tên miền trỏ đúng IP.

Để cập nhật phiên bản sau này, chạy `docker compose up -d --build` tại thư mục dự án. Không cần tạo lại tài khoản quản trị khi database trong `data/` còn nguyên.

Server chỉ dùng thư viện Python tiêu chuẩn; Docker image không cần cài package ngoài.
