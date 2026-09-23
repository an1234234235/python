n = 20
so_hien_tai = n + 1
while True:
    la_so_nguyen_to = True
    for i in range(2, so_hien_tai):
        if so_hien_tai % i == 0:
            la_so_nguyen_to = False
            break
    if la_so_nguyen_to:
        break
    so_hien_tai += 1
print(f"So nguyen to dau tien lon hon {n} la: {so_hien_tai}")