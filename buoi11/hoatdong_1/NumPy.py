import numpy as np
diem_list = [8.5, 7.0, 9.2, 6.5, 5.5] # list Python thuan
diem_array = np.array(diem_list) # chuyen sang mang NumPy (ndarray)
print(type(diem_list), type(diem_array))
# Phep toan vector hoa: cong truc tiep 0.5 vao TOAN BO mang, khong can vong lap
diem_cong_them = diem_array + 0.5
print(diem_cong_them)
# So sanh voi cach lam bang list thuan (Buoi 3) - can dung list comprehension/vong lap
diem_cong_them_list = [diem + 0.5 for diem in diem_list]
print(diem_cong_them_list)
print("Trung binh:", np.mean(diem_array))
print("Lon nhat:", np.max(diem_array))
print("Nho nhat:", np.min(diem_array))
print("Do lech chuan:", round(np.std(diem_array), 2))
ma_tran = np.array([[1, 2, 3], [4, 5, 6]])
print("Ma tran:\n", ma_tran)
print("Kich thuoc (shape):", ma_tran.shape)
print("Ma tran nhan 2:\n", ma_tran * 2)

"""
Yêu cầu: giải thích vì sao diem_array + 0.5 cộng được trực tiếp cho cả mảng, trong khi diem_list + 0.5 sẽ báo lỗi (gợi ý: toán tử + trên list thường dùng để nối 2 list, không phải cộng từng phần tử).
Giai Thich: Toán tử + trên mảng NumPy thực hiện phép toán vector hóa, tức là cộng từng phần tử của hai mảng. Trong khi đó, toán tử + trên list Python thường được dùng để nối hai list, không phải cộng từng phần tử.

"""