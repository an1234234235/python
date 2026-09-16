doan_van = "python la ngon ngu lap trinh python de hoc python de dung" 
danh_sach_tu = doan_van.split() 
tan_suat = {} 
for tu in danh_sach_tu: 
 tan_suat[tu] = tan_suat.get(tu, 0) + 1 
print("Tan suat xuat hien cac tu:") 
for tu, so_lan in tan_suat.items(): 
 print(f"{tu}: {so_lan}")
"""
Yêu cầu: Giải thích cách hoạt động của tan_suat.get(tu, 0) + 1 - vì sao chỉ một dòng này đã  thay thế được việc phải kiểm tra "từ đã xuất hiện hay chưa"
Câu lệnh `tan_suat.get(tu, 0) + 1` thực hiện hai bước chính:1. **Lấy giá trị hiện tại của từ khóa `tu` trong từ điển `tan_suat`**: 
   - Phương thức `get()` của từ điển được sử dụng để truy xuất giá trị của một khóa (key) trong từ điển. Nếu khóa tồn tại, nó sẽ trả về giá trị tương ứng; nếu không tồn tại, nó sẽ trả về giá trị mặc định mà bạn cung cấp (trong trường hợp này là `0`).
   - Ví dụ: Nếu từ khóa `tu` là "python" và nó đã xuất hiện trong từ điển với giá trị là `3`, thì `tan_suat.get("python", 0)` sẽ trả về `3`. Nếu từ khóa "python" chưa xuất hiện, nó sẽ trả về `0`.
2. **Cộng thêm 1 vào giá trị hiện tại**:
    - Sau khi lấy giá trị hiện tại (hoặc `0` nếu từ khóa chưa tồn tại), câu lệnh sẽ cộng thêm `1` vào giá trị đó. Điều này có nghĩa là bạn đang tăng số lần xuất hiện của từ khóa `tu` lên một đơn vị.
    - Ví dụ: Nếu từ khóa "python" đã xuất hiện 3 lần, thì `tan_suat.get("python", 0) + 1` sẽ trở thành `3 + 1 = 4`. Nếu từ khóa "python" chưa xuất hiện, thì nó sẽ trở thành `0 + 1 = 1`.
"""