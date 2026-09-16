#bài 1-1
sinh_vien = { 
 "ho_ten": "Nguyen Van A", 
 "nam_sinh": 2004, 
 "diem_tb": 8.5 
} 
print(sinh_vien["ho_ten"]) # truy xuat theo khoa 
print(sinh_vien.get("diem_tb")) # truy xuat an toan bang get() 
print(sinh_vien.get("lop", "Chua co")) # get() voi gia tri mac dinh neu khong co khoa

"""
Yêu cầu: Giải thích vì sao dùng sinh_vien["lop"] (khi "lop" chưa tồn tại) sẽ gây lỗi KeyError, còn  sinh_vien.get("lop", "Chua co") thì không. 
Trả lời: Khi bạn sử dụng sinh_vien["lop"], Python sẽ cố gắng truy cập giá trị của khóa "lop" trong từ điển sinh_vien. Nếu khóa này không tồn tại, Python sẽ ném ra một lỗi KeyError, vì nó không tìm thấy khóa đó trong từ điển.
"""
#bài 1-2
sinh_vien["lop"] = "CNTT01" # them khoa moi 
sinh_vien["diem_tb"] = 9.0 # sua gia tri khoa da co 
print(sinh_vien) 
diem_cu = sinh_vien.pop("diem_tb") # xoa theo khoa, tra ve gia tri vua xoa

print(sinh_vien, "- diem da xoa:", diem_cu) 
sinh_vien.update({"nam_sinh": 2003, "email": "a@example.com"}) # cap nhat/them nhieu  khoa cung luc 
print(sinh_vien)

