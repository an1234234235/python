so_luot_truy_cap = 0 # bien global
def tang_luot_truy_cap():
    global so_luot_truy_cap
    so_luot_truy_cap += 1
def vi_du_bien_local():
    so_luot_truy_cap = 100 # day la bien LOCAL, khac voi bien global cung ten
    print("Ben trong ham, bien local =", so_luot_truy_cap)
tang_luot_truy_cap()
tang_luot_truy_cap()
print("So luot truy cap (global):", so_luot_truy_cap)
vi_du_bien_local()
print("Sau khi goi ham, bien global van la:", so_luot_truy_cap)