danh_sach = [5, -3, 8, 0, -1, 12, 7, -9]
danh_sach_hop_le = []
for so in danh_sach:
    if so <= 0:
        continue # bo qua cac so khong duong, khong them vao danh sach ket qua
    danh_sach_hop_le.append(so)
print("Cac so hop le (duong):", danh_sach_hop_le)