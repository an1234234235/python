#bai 1
ho_ten = "Nguyen Van A"
diem_toan, diem_ly, diem_hoa = 8.0, 7.5, 9.0
dtb = round((diem_toan + diem_ly + diem_hoa) / 3, 2)
if dtb >= 8.0:
    xep_loai = "Gioi"
elif dtb >= 6.5:
    xep_loai = "Kha"
elif dtb >= 5.0:
    xep_loai = "Trung binh"
else:
    xep_loai = "Yeu"
print(f"{ho_ten} - DTB: {dtb} - Xep loai: {xep_loai}")