
# Hoạt động 1: Dictionary cơ bản
# Bài tập 1.2 - Quản lý điểm sinh viên

# 1. Khai báo Dictionary
# Khóa là họ tên, giá trị là list điểm các môn học
quan_ly_diem = {
    "Nguyen Van A": [8.0, 7.5, 9.0],
    "Tran Thi B": [6.0, 6.5, 5.5],
    "Le Van C": [9.0, 9.5, 8.5]
}

# 2. Thêm sinh viên mới
quan_ly_diem["Pham Thi D"] = [7.0, 8.0, 7.5]

# 3. Sửa điểm môn đầu tiên của một sinh viên
quan_ly_diem["Tran Thi B"][0] = 7.0

# 4. Tạo Dictionary lưu điểm trung bình
diem_trung_binh = {}

# 5. Duyệt từng sinh viên để tính DTB
for ho_ten, danh_sach_diem in quan_ly_diem.items():

    # Tính điểm trung bình
    dtb = sum(danh_sach_diem) / len(danh_sach_diem)

    # Làm tròn 2 chữ số thập phân
    dtb = round(dtb, 2)

    # Lưu vào Dictionary điểm trung bình
    diem_trung_binh[ho_ten] = dtb

# 6. In bảng điểm trung bình
print("BANG DIEM TRUNG BINH:")
print("-" * 55)

for ho_ten, dtb in diem_trung_binh.items():

    # Kiểm tra điều kiện đạt loại Giỏi
    dat_loai_gioi = dtb >= 8.0

    # In kết quả
    print(f"{ho_ten:<15} - DTB: {dtb:<5} - Dat loai Gioi? {dat_loai_gioi}")