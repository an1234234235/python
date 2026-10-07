# ==========================================
# CHƯƠNG TRÌNH QUẢN LÝ MÁY TÍNH QUÁN NET
# ==========================================

# 1. Danh sách các loại máy và đơn giá
danh_sach_loai_may = [
    {"ten_loai": "Thuong", "gia_gio": 8000},
    {"ten_loai": "VIP", "gia_gio": 15000},
    {"ten_loai": "Stream", "gia_gio": 22000},
]

# 2. Danh sách máy tính ban đầu
danh_sach_may = [
    {"ma_may": "NET01", "loai_may": "Thuong", "gia_gio": 8000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_may": "NET02", "loai_may": "Thuong", "gia_gio": 8000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_may": "VIP01", "loai_may": "VIP", "gia_gio": 15000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_may": "VIP02", "loai_may": "VIP", "gia_gio": 15000, "trang_thai": "Trong", "ten_khach": ""},
    {"ma_may": "STR01", "loai_may": "Stream", "gia_gio": 22000, "trang_thai": "Trong", "ten_khach": ""},
]

lich_su_doanh_thu = []

# ==========================================
# HÀM BẮT LỖI NHẬP LIỆU (TRY-EXCEPT)
# ==========================================
def nhap_so_nguyen(loi_nhac):
    while True:
        try:
            return int(input(loi_nhac))
        except ValueError:
            print("-> Du lieu khong hop le! Vui long nhap mot so nguyen.")

def nhap_so_thuc_duong(loi_nhac):
    while True:
        try:
            val = float(input(loi_nhac))
            if val > 0:
                return val
            print("-> Gia tri phai lon hon 0, vui long nhap lai!")
        except ValueError:
            print("-> Du lieu khong hop le! Vui long nhap mot so.")

# ==========================================
# HÀM HIỂN THỊ & TÌM KIẾM BỔ TRỢ
# ==========================================
def hien_thi_danh_sach_loai_may():
    print("\n--- DANH SÁCH LOẠI MÁY ---")
    for idx, lm in enumerate(danh_sach_loai_may, start=1):
        print(f"{idx}. Loai: {lm['ten_loai']:<10} | Gia: {lm['gia_gio']:,} VND/gio")

def chon_hoac_them_loai_may():
    hien_thi_danh_sach_loai_may()
    print(f"{len(danh_sach_loai_may) + 1}. [Thêm loại máy mới]")
    
    while True:
        chon = nhap_so_nguyen(f"Chon loại máy (1-{len(danh_sach_loai_may) + 1}): ")
        if 1 <= chon <= len(danh_sach_loai_may):
            return danh_sach_loai_may[chon - 1]
        elif chon == len(danh_sach_loai_may) + 1:
            ten_moi = input("Nhap ten loai may moi: ").strip().title()
            for lm in danh_sach_loai_may:
                if lm["ten_loai"].lower() == ten_moi.lower():
                    print(f"-> Loai may '{ten_moi}' da ton tai trong he thong.")
                    return lm
            gia_moi = nhap_so_nguyen("Nhap gia tien/gio cho loai may nay (VND): ")
            loai_moi = {"ten_loai": ten_moi, "gia_gio": gia_moi}
            danh_sach_loai_may.append(loai_moi)
            print(f"-> Da them loai may '{ten_moi}' vao danh sach he thong!")
            return loai_moi
        else:
            print("-> Luot chon khong hop le, vui long chon lai!")

def tim_may_theo_ma(ma_may):
    for may in danh_sach_may:
        if may["ma_may"] == ma_may:
            return may
    return None

def hien_thi_danh_sach_may():
    print("\n" + "=" * 65)
    print(f"{'Ma may':<10}{'Loai may':<12}{'Gia/Gio (VND)':<18}{'Trang thai':<15}{'Tai khoan':<10}")
    print("-" * 65)
    for may in danh_sach_may:
        print(f"{may['ma_may']:<10}{may['loai_may']:<12}{may['gia_gio']:>12,}       {may['trang_thai']:<15}{may['ten_khach']:<10}")
    print("=" * 65)

def xem_may_trong():
    may_trong = [may for may in danh_sach_may if may["trang_thai"] == "Trong"]
    if len(may_trong) == 0:
        print("-> Hien tai tat ca cac may deu dang co nguoi choi!")
        return
    print("\nDANH SÁCH MÁY ĐANG TRỐNG:")
    for may in may_trong:
        print(f" + {may['ma_may']} - Loai: {may['loai_may']} - Gia: {may['gia_gio']:,} VND/gio")

# ==========================================
# CÁC HÀM CHỨC NĂNG CHÍNH
# ==========================================
def them_may_moi():
    print("\n--- THÊM MÁY TÍNH MỚI ---")
    ma_may = input("Nhap ma may moi (vd: NET03, VIP03): ").strip().upper()
    if tim_may_theo_ma(ma_may) is not None:
        print(f"-> Ma may '{ma_may}' da ton tai trong he thong!")
        return
    
    print("\nChon loai may cho may moi nay:")
    loai_duoc_chon = chon_hoac_them_loai_may()
    
    danh_sach_may.append({
        "ma_may": ma_may,
        "loai_may": loai_duoc_chon["ten_loai"],
        "gia_gio": loai_duoc_chon["gia_gio"],
        "trang_thai": "Trong",
        "ten_khach": ""
    })
    print(f"-> Da them may {ma_may} ({loai_duoc_chon['ten_loai']} - {loai_duoc_chon['gia_gio']:,} VND/gio) thanh cong.")

def mo_may_cho_khach():
    print("\n===== MỞ MÁY CHO KHÁCH CHƠI =====")
    
    may_trong_all = [may for may in danh_sach_may if may["trang_thai"] == "Trong"]
    if len(may_trong_all) == 0:
        print("-> Rất tiếc, hiện tại tất cả các máy đều đang có người chơi!")
        return

    # Buoc 1: Hien thi danh sach cac loai may
    print("\nCHỌN LOẠI MÁY KHÁCH MUỐN CHƠI:")
    for idx, lm in enumerate(danh_sach_loai_may, start=1):
        so_may_trong = sum(1 for m in danh_sach_may if m["loai_may"] == lm["ten_loai"] and m["trang_thai"] == "Trong")
        print(f"{idx}. Loai: {lm['ten_loai']:<10} | Gia: {lm['gia_gio']:,} VND/gio | (Con trong: {so_may_trong} may)")

    while True:
        chon_loai = nhap_so_nguyen(f"Chon loai may (1-{len(danh_sach_loai_may)}): ")
        if 1 <= chon_loai <= len(danh_sach_loai_may):
            loai_chon = danh_sach_loai_may[chon_loai - 1]
            break
        print("-> Luot chon khong hop le, vui long chon lai!")

    # Buoc 2: Loc ra danh sach may trong thuoc loai da chon
    danh_sach_trong_loai = [m for m in danh_sach_may if m["loai_may"] == loai_chon["ten_loai"] and m["trang_thai"] == "Trong"]
    
    if len(danh_sach_trong_loai) == 0:
        print(f"-> Loai may '{loai_chon['ten_loai']}' hien da HET MAY TRONG. Vui long chon loai may khac.")
        return

    # Buoc 3: Hien thi va chon may bang so thu tu
    print(f"\nCÁC MÁY TRỐNG THUỘC LOẠI '{loai_chon['ten_loai']}':")
    for idx, may in enumerate(danh_sach_trong_loai, start=1):
        print(f" {idx}. May {may['ma_may']}")

    while True:
        chon_may = nhap_so_nguyen(f"Chon may can mo (1-{len(danh_sach_trong_loai)}): ")
        if 1 <= chon_may <= len(danh_sach_trong_loai):
            may_duoc_chon = danh_sach_trong_loai[chon_may - 1]
            break
        print("-> Luot chon khong hop le, vui long chon lai!")

    ten_khach = input("Nhap ten/tai khoan khach hang: ").strip()
    if not ten_khach:
        ten_khach = "Khach_Vang_Lai"

    may_duoc_chon["trang_thai"] = "Dang su dung"
    may_duoc_chon["ten_khach"] = ten_khach
    print(f"-> Da mo may {may_duoc_chon['ma_may']} cho tai khoan '{ten_khach}' thanh cong.")

def tat_may_thanh_toan():
    print("\n===== TẮT MÁY VÀ THANH TOÁN =====")
    
    # Loc ra cac may dang co nguoi dung
    danh_sach_dang_dung = [m for m in danh_sach_may if m["trang_thai"] == "Dang su dung"]
    
    if len(danh_sach_dang_dung) == 0:
        print("-> Hiện tại không có máy nào đang hoạt động để thanh toán!")
        return

    # Hien thi danh sach cac may dang su dung
    print("\nDANH SÁCH MÁY ĐANG HOẠT ĐỘNG:")
    for idx, may in enumerate(danh_sach_dang_dung, start=1):
        print(f" {idx}. Máy {may['ma_may']:<8} | Tài khoản: {may['ten_khach']:<15} | Loại: {may['loai_may']} ({may['gia_gio']:,} VND/h)")

    # Chon may can tat theo so thu tu (1, 2, 3...)
    while True:
        chon = nhap_so_nguyen(f"\nChon máy cần tắt/thanh toán (1-{len(danh_sach_dang_dung)}): ")
        if 1 <= chon <= len(danh_sach_dang_dung):
            may_duoc_chon = danh_sach_dang_dung[chon - 1]
            break
        print("-> Luot chon khong hop le, vui long chon lai!")

    so_gio = nhap_so_thuc_duong(f"Nhap so gio tai khoan '{may_duoc_chon['ten_khach']}' da choi (vd: 1.5): ")
    thanh_tien = round(may_duoc_chon["gia_gio"] * so_gio)
    
    # Luu lich su doanh thu
    lich_su_doanh_thu.append({
        "ma_may": may_duoc_chon["ma_may"],
        "ten_khach": may_duoc_chon["ten_khach"],
        "so_gio": so_gio,
        "thanh_tien": thanh_tien
    })
    
    print(f"\n======================================")
    print(f"         HÓA ĐƠN THANH TOÁN          ")
    print(f"Mã máy        : {may_duoc_chon['ma_may']}")
    print(f"Tài khoản     : {may_duoc_chon['ten_khach']}")
    print(f"Thời gian chơi: {so_gio} giờ")
    print(f"Đơn giá       : {may_duoc_chon['gia_gio']:,} VND/giờ")
    print(f"--------------------------------------")
    print(f"TỔNG TIỀN     : {thanh_tien:,} VND")
    print(f"======================================\n")
    
    # Reset trang thai may ve Trong
    may_duoc_chon["trang_thai"] = "Trong"
    may_duoc_chon["ten_khach"] = ""
    print(f"-> Đã tắt máy {may_duoc_chon['ma_may']} và chuyển về trạng thái TRỐNG.")

def thong_ke_doanh_thu():
    if len(lich_su_doanh_thu) == 0:
        print("-> Chua co giao dich thanh toan nao trong phien lam viec.")
        return
    
    tong_doanh_thu = 0
    print("\nLỊCH SỬ GIAO DỊCH ĐÃ THANH TOÁN:")
    print(f"{'STT':<5}{'Ma may':<10}{'Tai khoan':<15}{'So gio':<10}{'Thanh tien (VND)':<15}")
    print("-" * 55)
    for idx, gd in enumerate(lich_su_doanh_thu, start=1):
        print(f"{idx:<5}{gd['ma_may']:<10}{gd['ten_khach']:<15}{gd['so_gio']:<10}{gd['thanh_tien']:>12,}")
        tong_doanh_thu += gd["thanh_tien"]
    print("-" * 55)
    print(f">>> TỔNG DOANH THU THU ĐƯỢC: {tong_doanh_thu:,} VND")

# ==========================================
# MENU CHÍNH & VÒNG LẶP CHƯƠNG TRÌNH
# ==========================================
def hien_thi_menu():
    print("\n===== QUẢN LÝ MÁY TÍNH QUẢN NET =====")
    print("1. Hien thi danh sach tat ca cac may")
    print("2. Xem danh sach may dang trong")
    print("3. Them may tinh moi")
    print("4. Mo may cho khach choi")
    print("5. Tat may va Thanh toan")
    print("6. Thong ke doanh thu")
    print("0. Thoat chuong trinh")

def chay_chuong_trinh():
    while True:
        hien_thi_menu()
        lua_chon = input("Nhap lua chon cua ban (0-6): ").strip()
        
        if lua_chon == "1":
            hien_thi_danh_sach_may()
        elif lua_chon == "2":
            xem_may_trong()
        elif lua_chon == "3":
            them_may_moi()
        elif lua_chon == "4":
            mo_may_cho_khach()
        elif lua_chon == "5":
            tat_may_thanh_toan()
        elif lua_chon == "6":
            thong_ke_doanh_thu()
        elif lua_chon == "0":
            print("Cam on ban da su dung phan mem quan ly quan net! Tam biet.")
            break
        else:
            print("-> Lua chon khong hop le, vui long nhap lai tu 0 den 6.")

if __name__ == "__main__":
    chay_chuong_trinh()