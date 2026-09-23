so = 4527
so_tam = so
tong_chu_so = 0
while so_tam > 0:
    chu_so = so_tam % 10
    tong_chu_so += chu_so
    so_tam = so_tam // 10
    print(f"Tong cac chu so cua {so} la: {tong_chu_so}")