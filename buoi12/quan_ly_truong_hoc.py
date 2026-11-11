import html
import sqlite3
import tempfile
import tkinter as tk
import webbrowser
from datetime import date, datetime
from pathlib import Path
from tkinter import messagebox, ttk

import csdl_quan_ly_truong as db


MAU_NEN = "#f3f5f2"
MAU_CHU = "#24352d"
MAU_XANH = "#176b52"


def _lua_chon_id(gia_tri):
    if not gia_tri or gia_tri.startswith("("):
        return None
    return int(gia_tri.split(" · ", 1)[0])


def _nhan_lua_chon(danh_sach, id_can_tim, nhan_mac_dinh):
    if id_can_tim is None:
        return nhan_mac_dinh
    for dong in danh_sach:
        if dong[0] == id_can_tim:
            return f"{dong[0]} · {dong[1]}"
    return nhan_mac_dinh


class TrangQuanLy(ttk.Frame):
    def __init__(
        self, parent, tieu_de, cot, truong, tai_du_lieu, hien_thi,
        lay_bieu_mau, luu, xoa, on_change,
    ):
        super().__init__(parent, padding=16)
        self.tieu_de = tieu_de
        self.cot = cot
        self.truong = truong
        self.tai_du_lieu = tai_du_lieu
        self.hien_thi = hien_thi
        self.lay_bieu_mau = lay_bieu_mau
        self.luu = luu
        self.xoa_ban_ghi = xoa
        self.on_change = on_change
        self.ban_ghi = {}
        self.tu_khoa = tk.StringVar(self)

        thanh_cong_cu = ttk.Frame(self)
        thanh_cong_cu.pack(fill="x", pady=(0, 10))
        ttk.Label(thanh_cong_cu, text=tieu_de, style="Section.TLabel").pack(side="left")
        o_tim = ttk.Entry(thanh_cong_cu, textvariable=self.tu_khoa, width=28)
        o_tim.pack(side="right", padx=(8, 0))
        ttk.Label(thanh_cong_cu, text="Tìm kiếm").pack(side="right")
        self.tu_khoa.trace_add("write", self.tai_lai)

        khung_bang = ttk.Frame(self)
        khung_bang.pack(fill="both", expand=True)
        ma_cot = tuple(cot_khoa for cot_khoa, _, _ in cot)
        self.bang = ttk.Treeview(khung_bang, columns=ma_cot, show="headings", selectmode="browse")
        for ma, ten, rong in cot:
            self.bang.heading(ma, text=ten)
            self.bang.column(ma, width=rong, minwidth=75, anchor="w")
        thanh_cuon = ttk.Scrollbar(khung_bang, orient="vertical", command=self.bang.yview)
        self.bang.configure(yscrollcommand=thanh_cuon.set)
        self.bang.pack(side="left", fill="both", expand=True)
        thanh_cuon.pack(side="right", fill="y")
        self.bang.bind("<Double-1>", lambda _event: self.mo_bieu_mau(sua=True))

        nut = ttk.Frame(self)
        nut.pack(fill="x", pady=(10, 0))
        ttk.Button(nut, text="＋  Thêm", command=lambda: self.mo_bieu_mau()).pack(side="left", padx=(0, 7))
        ttk.Button(nut, text="Sửa", command=lambda: self.mo_bieu_mau(sua=True)).pack(side="left", padx=(0, 7))
        ttk.Button(nut, text="Xóa", command=self.xoa_dang_chon).pack(side="left", padx=(0, 7))
        ttk.Button(nut, text="Làm mới", command=self.tai_lai).pack(side="right")
        self.tai_lai()

    def tai_lai(self, *_):
        self.ban_ghi.clear()
        self.bang.delete(*self.bang.get_children())
        tu_khoa = self.tu_khoa.get().casefold()
        for dong in self.tai_du_lieu(self.tu_khoa.get()):
            if tu_khoa and not any(tu_khoa in str(gia_tri).casefold() for gia_tri in self.hien_thi(dong)):
                continue
            id_ban_ghi = dong[0]
            self.ban_ghi[id_ban_ghi] = dong
            self.bang.insert("", "end", iid=str(id_ban_ghi), values=self.hien_thi(dong))

    def mo_bieu_mau(self, sua=False):
        id_ban_ghi = None
        dong = None
        if sua:
            lua_chon = self.bang.selection()
            if not lua_chon:
                messagebox.showwarning("Chưa chọn", f"Vui lòng chọn {self.tieu_de.lower()} cần sửa.", parent=self)
                return
            id_ban_ghi = int(lua_chon[0])
            dong = self.ban_ghi[id_ban_ghi]

        cua_so = tk.Toplevel(self)
        cua_so.title(f"{'Sửa' if sua else 'Thêm'} {self.tieu_de.lower()}")
        cua_so.transient(self.winfo_toplevel())
        cua_so.grab_set()
        cua_so.resizable(False, False)
        noi_dung = ttk.Frame(cua_so, padding=18)
        noi_dung.pack(fill="both", expand=True)
        gia_tri = {}
        o_dau = None
        truong = self.truong()

        for vi_tri, (khoa, nhan, lua_chon, mac_dinh) in enumerate(truong):
            hang, cot = divmod(vi_tri, 2)
            khung_truong = ttk.Frame(noi_dung)
            khung_truong.grid(row=hang, column=cot, sticky="ew", padx=7, pady=6)
            ttk.Label(khung_truong, text=nhan).pack(anchor="w", pady=(0, 4))
            bien = tk.StringVar(cua_so, value=mac_dinh)
            if lua_chon is None:
                o_nhap = ttk.Entry(khung_truong, textvariable=bien, width=31)
            else:
                o_nhap = ttk.Combobox(
                    khung_truong, textvariable=bien, values=lua_chon, state="readonly", width=28
                )
                if mac_dinh and mac_dinh not in lua_chon:
                    bien.set(lua_chon[0] if lua_chon else "")
            o_nhap.pack(fill="x")
            if o_dau is None:
                o_dau = o_nhap
            gia_tri[khoa] = bien
        if o_dau is not None and not sua:
            o_dau.focus_set()

        hang_nut = (len(truong) + 1) // 2
        nut = ttk.Frame(noi_dung)
        nut.grid(row=hang_nut, column=0, columnspan=2, sticky="e", padx=7, pady=(12, 0))

        def luu_bieu_mau():
            du_lieu = {khoa: bien.get().strip() for khoa, bien in gia_tri.items()}
            try:
                self.luu(du_lieu, id_ban_ghi)
            except (ValueError, sqlite3.IntegrityError) as loi:
                messagebox.showerror("Không lưu được", str(loi), parent=cua_so)
                return
            except Exception as loi:
                messagebox.showerror("Lỗi cơ sở dữ liệu", str(loi), parent=cua_so)
                return
            cua_so.destroy()
            self.tai_lai()
            self.on_change()

        ttk.Button(nut, text="Hủy", command=cua_so.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(nut, text="Lưu", style="Accent.TButton", command=luu_bieu_mau).pack(side="right")
        cua_so.bind("<Return>", lambda _event: luu_bieu_mau())
        cua_so.bind("<Escape>", lambda _event: cua_so.destroy())
        if dong is not None:
            for khoa, bien_gia_tri in gia_tri.items():
                bien_gia_tri.set(self.lay_bieu_mau(dong).get(khoa, ""))

    def xoa_dang_chon(self):
        lua_chon = self.bang.selection()
        if not lua_chon:
            messagebox.showwarning("Chưa chọn", f"Vui lòng chọn {self.tieu_de.lower()} cần xóa.", parent=self)
            return
        if not messagebox.askyesno(
            "Xác nhận xóa",
            f"Xóa {self.tieu_de.lower()} đã chọn? Dữ liệu liên quan có thể bị ảnh hưởng.",
            parent=self,
        ):
            return
        try:
            self.xoa_ban_ghi(int(lua_chon[0]))
        except Exception as loi:
            messagebox.showerror("Lỗi cơ sở dữ liệu", str(loi), parent=self)
            return
        self.tai_lai()
        self.on_change()


class UngDungQuanLyTruong(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý trường học")
        self.geometry("1180x760")
        self.minsize(900, 620)
        self.configure(background=MAU_NEN)
        db.tao_bang_neu_chua_co()
        self._tao_giao_dien()
        self.cap_nhat_tong_quan()

    def _tao_giao_dien(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=MAU_NEN)
        style.configure("TLabel", background=MAU_NEN, foreground=MAU_CHU, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 21, "bold"), foreground=MAU_XANH)
        style.configure("Section.TLabel", font=("Segoe UI", 13, "bold"), foreground=MAU_CHU)
        style.configure("TButton", padding=(11, 7))
        style.configure("Accent.TButton", background=MAU_XANH, foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#0f543f")])
        style.configure("Treeview", rowheight=31, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background=MAU_NEN, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(15, 9), font=("Segoe UI", 10, "bold"))

        khung = ttk.Frame(self, padding=18)
        khung.pack(fill="both", expand=True)
        ttk.Label(khung, text="QUẢN LÝ TRƯỜNG HỌC", style="Title.TLabel").pack(anchor="w")
        ttk.Label(khung, text="Hồ sơ học sinh · lớp học · giáo viên · học tập").pack(anchor="w", pady=(3, 14))
        self.notebook = ttk.Notebook(khung)
        self.notebook.pack(fill="both", expand=True)

        self.trang_tong_quan = ttk.Frame(self.notebook, padding=18)
        self.notebook.add(self.trang_tong_quan, text="Tổng quan")
        self._tao_tong_quan()

        def them_trang(ten, trang):
            self.notebook.add(trang, text=ten)

        self._tao_trang_giao_vien(them_trang)
        self._tao_trang_lop(them_trang)
        self._tao_trang_hoc_sinh(them_trang)
        self._tao_trang_diem(them_trang)
        self._tao_trang_chuyen_can(them_trang)
        self._tao_trang_thong_ke(them_trang)

    def _tao_tong_quan(self):
        ttk.Label(self.trang_tong_quan, text="Bảng điều hành", style="Section.TLabel").pack(anchor="w", pady=(0, 14))
        self.the_tong_quan = {}
        danh_sach_the = [
            ("hoc_sinh", "Học sinh", "#176b52"),
            ("lop", "Lớp học", "#315d85"),
            ("giao_vien", "Giáo viên", "#a05a2c"),
            ("diem", "Đầu điểm", "#6e5945"),
            ("vang_hom_nay", "Học sinh vắng hôm nay", "#9b3d3d"),
        ]
        khung_the = ttk.Frame(self.trang_tong_quan)
        khung_the.pack(fill="x")
        for cot, (khoa, nhan, mau) in enumerate(danh_sach_the):
            khung_the.columnconfigure(cot, weight=1, uniform="stat")
            the = tk.Frame(khung_the, background=mau, padx=16, pady=14)
            the.grid(row=0, column=cot, sticky="ew", padx=(0 if cot == 0 else 8, 0), pady=2)
            tk.Label(the, text=nhan, background=mau, foreground="#ffffff", font=("Segoe UI", 10)).pack(anchor="w")
            gia_tri = tk.Label(the, text="0", background=mau, foreground="#ffffff", font=("Segoe UI", 24, "bold"))
            gia_tri.pack(anchor="w", pady=(8, 0))
            self.the_tong_quan[khoa] = gia_tri

        ttk.Label(self.trang_tong_quan, text="Dữ liệu được lưu cục bộ trên máy tính này.").pack(anchor="w", pady=(20, 0))

    def cap_nhat_tong_quan(self):
        for khoa, so_luong in db.lay_tong_quan().items():
            if khoa in getattr(self, "the_tong_quan", {}):
                self.the_tong_quan[khoa].configure(text=str(so_luong))

    def _tao_trang_giao_vien(self, them_trang):
        cot = [("ho_ten", "Họ tên", 210), ("chuyen_mon", "Chuyên môn", 170), ("dien_thoai", "Điện thoại", 145), ("email", "Email", 230)]
        truong = lambda: [
            ("ho_ten", "Họ tên *", None, ""),
            ("chuyen_mon", "Chuyên môn", None, ""),
            ("dien_thoai", "Điện thoại", None, ""),
            ("email", "Email", None, ""),
        ]

        def luu(v, rid):
            if not v["ho_ten"]:
                raise ValueError("Họ tên giáo viên là bắt buộc.")
            if rid is None:
                db.them_giao_vien(v["ho_ten"], v["chuyen_mon"], v["dien_thoai"], v["email"])
            else:
                db.sua_giao_vien(rid, v["ho_ten"], v["chuyen_mon"], v["dien_thoai"], v["email"])

        them_trang("Giáo viên", TrangQuanLy(
            self.notebook, "Giáo viên", cot, truong, lambda _q: db.lay_giao_vien(),
            lambda r: r[1:5], lambda r: dict(zip(("ho_ten", "chuyen_mon", "dien_thoai", "email"), r[1:5])),
            luu, db.xoa_giao_vien, self.cap_nhat_tong_quan,
        ))

    def _tao_trang_lop(self, them_trang):
        nhan_khong = "(Chưa phân công)"

        def danh_sach_giao_vien():
            return [nhan_khong, *[f"{r[0]} · {r[1]}" for r in db.lay_giao_vien()]]

        def truong():
            return [
                ("ten_lop", "Tên lớp *", None, ""),
                ("khoi", "Khối *", None, ""),
                ("nam_hoc", "Năm học *", None, "2026-2027"),
                ("giao_vien", "Giáo viên chủ nhiệm", danh_sach_giao_vien(), nhan_khong),
            ]

        def luu(v, rid):
            if not all(v[k] for k in ("ten_lop", "khoi", "nam_hoc")):
                raise ValueError("Tên lớp, khối và năm học là bắt buộc.")
            giao_vien_id = _lua_chon_id(v["giao_vien"])
            if rid is None:
                db.them_lop(v["ten_lop"], v["khoi"], v["nam_hoc"], giao_vien_id)
            else:
                db.sua_lop(rid, v["ten_lop"], v["khoi"], v["nam_hoc"], giao_vien_id)

        def bieu_mau(r):
            return {"ten_lop": r[1], "khoi": r[2], "nam_hoc": r[3], "giao_vien": _nhan_lua_chon(db.lay_giao_vien(), r[4], nhan_khong)}

        them_trang("Lớp học", TrangQuanLy(
            self.notebook, "Lớp học", [("ten", "Lớp", 130), ("khoi", "Khối", 90), ("nam", "Năm học", 140), ("gv", "Giáo viên chủ nhiệm", 220)],
            truong, lambda _q: db.lay_lop(), lambda r: (r[1], r[2], r[3], r[5]), bieu_mau,
            luu, db.xoa_lop, self.cap_nhat_tong_quan,
        ))

    def _tao_trang_hoc_sinh(self, them_trang):
        nhan_khong = "(Chưa xếp lớp)"

        def danh_sach_lop():
            return [nhan_khong, *[f"{r[0]} · {r[1]}" for r in db.lay_lop()]]

        def truong():
            return [
                ("ma", "Mã học sinh *", None, ""),
                ("ho_ten", "Họ và tên *", None, ""),
                ("ngay_sinh", "Ngày sinh (YYYY-MM-DD)", None, ""),
                ("gioi_tinh", "Giới tính", ["", "Nam", "Nữ", "Khác"], ""),
                ("nguoi_giam_ho", "Người giám hộ", None, ""),
                ("dien_thoai", "Điện thoại phụ huynh", None, ""),
                ("dia_chi", "Địa chỉ", None, ""),
                ("lop", "Lớp", danh_sach_lop(), nhan_khong),
            ]

        def luu(v, rid):
            if not v["ma"] or not v["ho_ten"]:
                raise ValueError("Mã học sinh và họ tên là bắt buộc.")
            if v["ngay_sinh"]:
                try:
                    date.fromisoformat(v["ngay_sinh"])
                except ValueError as loi:
                    raise ValueError("Ngày sinh cần đúng định dạng YYYY-MM-DD.") from loi
            lop_id = _lua_chon_id(v["lop"])
            if rid is None:
                db.them_hoc_sinh(v["ma"], v["ho_ten"], v["ngay_sinh"], v["gioi_tinh"], v["nguoi_giam_ho"], v["dien_thoai"], v["dia_chi"], lop_id)
            else:
                db.sua_hoc_sinh(rid, v["ma"], v["ho_ten"], v["ngay_sinh"], v["gioi_tinh"], v["nguoi_giam_ho"], v["dien_thoai"], v["dia_chi"], lop_id)

        def bieu_mau(r):
            return {
                "ma": r[1], "ho_ten": r[2], "ngay_sinh": r[3], "gioi_tinh": r[4],
                "nguoi_giam_ho": r[5], "dien_thoai": r[6], "dia_chi": r[7],
                "lop": _nhan_lua_chon(db.lay_lop(), r[8], nhan_khong),
            }

        them_trang("Học sinh", TrangQuanLy(
            self.notebook, "Học sinh",
            [("ma", "Mã HS", 100), ("ten", "Họ và tên", 190), ("ns", "Ngày sinh", 110), ("gt", "Giới tính", 90), ("lop", "Lớp", 100), ("sdt", "Điện thoại PH", 140)],
            truong, lambda q: db.lay_hoc_sinh(q), lambda r: (r[1], r[2], r[3], r[4], r[9], r[6]),
            bieu_mau, luu, db.xoa_hoc_sinh, self.cap_nhat_tong_quan,
        ))

    def _tao_trang_diem(self, them_trang):
        nhan_khong = "(Chọn học sinh)"

        def danh_sach_hoc_sinh():
            return [nhan_khong, *[f"{r[0]} · {r[1]}" for r in db.lay_hoc_sinh()]]

        def truong():
            return [
                ("hoc_sinh", "Học sinh *", danh_sach_hoc_sinh(), nhan_khong),
                ("mon_hoc", "Môn học *", None, ""),
                ("hoc_ky", "Học kỳ *", ["HK1", "HK2", "Cả năm"], "HK1"),
                ("diem", "Điểm (0-10) *", None, ""),
            ]

        def luu(v, _rid):
            hoc_sinh_id = _lua_chon_id(v["hoc_sinh"])
            if hoc_sinh_id is None or not v["mon_hoc"] or not v["hoc_ky"] or not v["diem"]:
                raise ValueError("Vui lòng nhập đủ học sinh, môn học, học kỳ và điểm.")
            diem = float(v["diem"].replace(",", "."))
            if not 0 <= diem <= 10:
                raise ValueError("Điểm phải nằm trong khoảng 0 đến 10.")
            db.them_hoac_sua_diem(hoc_sinh_id, v["mon_hoc"], v["hoc_ky"], diem)

        def bieu_mau(r):
            return {"hoc_sinh": _nhan_lua_chon(db.lay_hoc_sinh(), r[1], nhan_khong), "mon_hoc": r[4], "hoc_ky": r[5], "diem": str(r[6])}

        them_trang("Điểm", TrangQuanLy(
            self.notebook, "Điểm", [("ma", "Mã HS", 100), ("ten", "Học sinh", 190), ("mon", "Môn học", 150), ("ky", "Học kỳ", 100), ("diem", "Điểm", 90)],
            truong, lambda _q: db.lay_diem(), lambda r: (r[2], r[3], r[4], r[5], f"{r[6]:g}"),
            bieu_mau, luu, db.xoa_diem, self.cap_nhat_tong_quan,
        ))

    def _tao_trang_chuyen_can(self, them_trang):
        nhan_khong = "(Chọn học sinh)"

        def danh_sach_hoc_sinh():
            return [nhan_khong, *[f"{r[0]} · {r[1]}" for r in db.lay_hoc_sinh()]]

        def truong():
            return [
                ("hoc_sinh", "Học sinh *", danh_sach_hoc_sinh(), nhan_khong),
                ("ngay", "Ngày (YYYY-MM-DD) *", None, date.today().isoformat()),
                ("trang_thai", "Trạng thái", ["Có mặt", "Vắng", "Muộn"], "Có mặt"),
                ("ghi_chu", "Ghi chú", None, ""),
            ]

        def luu(v, _rid):
            hoc_sinh_id = _lua_chon_id(v["hoc_sinh"])
            if hoc_sinh_id is None or not v["ngay"]:
                raise ValueError("Vui lòng chọn học sinh và nhập ngày.")
            try:
                date.fromisoformat(v["ngay"])
            except ValueError as loi:
                raise ValueError("Ngày cần đúng định dạng YYYY-MM-DD.") from loi
            db.them_hoac_sua_chuyen_can(hoc_sinh_id, v["ngay"], v["trang_thai"], v["ghi_chu"])

        def bieu_mau(r):
            return {
                "hoc_sinh": _nhan_lua_chon(db.lay_hoc_sinh(), r[1], nhan_khong),
                "ngay": r[4], "trang_thai": r[5], "ghi_chu": r[6],
            }

        them_trang("Chuyên cần", TrangQuanLy(
            self.notebook, "Chuyên cần", [("ma", "Mã HS", 100), ("ten", "Học sinh", 190), ("ngay", "Ngày", 120), ("tt", "Trạng thái", 110), ("gc", "Ghi chú", 260)],
            truong, lambda _q: db.lay_chuyen_can(), lambda r: (r[2], r[3], r[4], r[5], r[6]),
            bieu_mau, luu, db.xoa_chuyen_can, self.cap_nhat_tong_quan,
        ))

    def _tao_trang_thong_ke(self, them_trang):
        trang = ttk.Frame(self.notebook, padding=16)
        them_trang("Thống kê", trang)
        thanh_dieu_khien = ttk.Frame(trang)
        thanh_dieu_khien.pack(fill="x", pady=(0, 10))
        ttk.Label(thanh_dieu_khien, text="Báo cáo tổng hợp", style="Section.TLabel").pack(side="left")
        ttk.Button(
            thanh_dieu_khien, text="In / Xuất báo cáo", style="Accent.TButton",
            command=self.mo_bao_cao_in,
        ).pack(side="right")
        ttk.Button(thanh_dieu_khien, text="Làm mới", command=self.cap_nhat_thong_ke).pack(
            side="right", padx=(0, 8)
        )
        self.nhan_tong_hop = ttk.Label(trang, text="")
        self.nhan_tong_hop.pack(anchor="w", pady=(0, 10))

        self.bang_thong_ke = {}
        cau_hinh_bang = [
            ("lop", "Theo lớp", [("lop", "Lớp", 160), ("si_so", "Sĩ số", 100), ("diem_tb", "Điểm trung bình", 150), ("vang", "Lượt vắng", 110)]),
            ("mon", "Theo môn học và học kỳ", [("mon", "Môn học", 180), ("hoc_ky", "Học kỳ", 100), ("so_diem", "Số điểm", 100), ("trung_binh", "Trung bình", 110), ("thap", "Thấp nhất", 100), ("cao", "Cao nhất", 100)]),
            ("chuyen_can", "Theo chuyên cần", [("trang_thai", "Trạng thái", 180), ("so_luot", "Số lượt", 100)]),
        ]
        for khoa, tieu_de, cot in cau_hinh_bang:
            khung = ttk.LabelFrame(trang, text=tieu_de, padding=8)
            khung.pack(fill="both", expand=True, pady=(0, 8))
            ma_cot = tuple(cot_khoa for cot_khoa, _, _ in cot)
            bang = ttk.Treeview(khung, columns=ma_cot, show="headings", height=4)
            for ma, nhan, rong in cot:
                bang.heading(ma, text=nhan)
                bang.column(ma, width=rong, minwidth=75, anchor="center")
            bang.pack(fill="both", expand=True)
            self.bang_thong_ke[khoa] = bang
        self.cap_nhat_thong_ke()

    def cap_nhat_thong_ke(self):
        thong_ke = db.lay_thong_ke()
        tong = thong_ke["tong_quan"]
        self.nhan_tong_hop.configure(
            text=(
                f"{tong['hoc_sinh']} học sinh  ·  {tong['lop']} lớp  ·  "
                f"{tong['giao_vien']} giáo viên  ·  {tong['diem']} đầu điểm  ·  "
                f"{tong['ban_ghi_chuyen_can']} lượt chuyên cần"
            )
        )
        du_lieu = {
            "lop": [
                (lop, si_so, "—" if diem_tb is None else f"{diem_tb:.2f}", vang)
                for lop, si_so, diem_tb, vang in thong_ke["theo_lop"]
            ],
            "mon": [
                (mon, hoc_ky, so_diem, f"{trung_binh:.2f}", f"{thap:.2f}", f"{cao:.2f}")
                for mon, hoc_ky, so_diem, trung_binh, thap, cao in thong_ke["theo_mon_hoc"]
            ],
            "chuyen_can": thong_ke["theo_chuyen_can"],
        }
        for khoa, bang in self.bang_thong_ke.items():
            bang.delete(*bang.get_children())
            for dong in du_lieu[khoa]:
                bang.insert("", "end", values=dong)

    def mo_bao_cao_in(self):
        thong_ke = db.lay_thong_ke()
        tong = thong_ke["tong_quan"]

        def bang_html(tieu_de, tieu_de_cot, cac_dong):
            dau_bang = "".join(f"<th>{html.escape(str(nhan))}</th>" for nhan in tieu_de_cot)
            if cac_dong:
                than_bang = "".join(
                    "<tr>" + "".join(f"<td>{html.escape(str(o))}</td>" for o in dong) + "</tr>"
                    for dong in cac_dong
                )
            else:
                than_bang = f'<tr><td colspan="{len(tieu_de_cot)}">Chưa có dữ liệu</td></tr>'
            return f"<h2>{html.escape(tieu_de)}</h2><table><thead><tr>{dau_bang}</tr></thead><tbody>{than_bang}</tbody></table>"

        cac_bang = [
            bang_html("Thống kê theo lớp", ["Lớp", "Sĩ số", "Điểm trung bình", "Lượt vắng"], [
                (lop, si_so, "—" if diem_tb is None else f"{diem_tb:.2f}", vang)
                for lop, si_so, diem_tb, vang in thong_ke["theo_lop"]
            ]),
            bang_html("Thống kê theo môn học và học kỳ", ["Môn học", "Học kỳ", "Số điểm", "Trung bình", "Thấp nhất", "Cao nhất"], [
                (mon, hoc_ky, so_diem, f"{trung_binh:.2f}", f"{thap:.2f}", f"{cao:.2f}")
                for mon, hoc_ky, so_diem, trung_binh, thap, cao in thong_ke["theo_mon_hoc"]
            ]),
            bang_html("Thống kê chuyên cần", ["Trạng thái", "Số lượt"], thong_ke["theo_chuyen_can"]),
        ]
        noi_dung = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><title>Báo cáo thống kê trường học</title>
<style>
body{{font-family:Arial,sans-serif;color:#24352d;margin:32px;}}
h1{{color:#176b52;margin-bottom:6px;}} .meta{{color:#56645d;margin-bottom:22px;}}
.summary{{padding:14px;background:#edf3ef;border-left:4px solid #176b52;margin-bottom:24px;}}
table{{border-collapse:collapse;width:100%;margin-bottom:24px;}} th,td{{border:1px solid #cbd4ce;padding:8px;text-align:left;}}
th{{background:#edf3ef;}} .print{{position:fixed;right:24px;top:20px;padding:10px 16px;background:#176b52;color:white;border:0;cursor:pointer;}}
@media print{{body{{margin:12mm;}} .print{{display:none;}} h2{{break-after:avoid;}} table{{break-inside:avoid;}}}}
</style></head><body>
<button class="print" onclick="window.print()">In báo cáo</button>
<h1>BÁO CÁO THỐNG KÊ TRƯỜNG HỌC</h1>
<div class="meta">Thời điểm lập: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
<div class="summary">Học sinh: {tong['hoc_sinh']} &nbsp; | &nbsp; Lớp: {tong['lop']} &nbsp; | &nbsp; Giáo viên: {tong['giao_vien']} &nbsp; | &nbsp; Đầu điểm: {tong['diem']} &nbsp; | &nbsp; Lượt chuyên cần: {tong['ban_ghi_chuyen_can']}</div>
{''.join(cac_bang)}
</body></html>"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", suffix=".html", prefix="bao_cao_truong_", delete=False
            ) as tep:
                tep.write(noi_dung)
                duong_dan = Path(tep.name).resolve()
            webbrowser.open_new_tab(duong_dan.as_uri())
        except OSError as loi:
            messagebox.showerror("Không tạo được báo cáo", str(loi), parent=self)


if __name__ == "__main__":
    UngDungQuanLyTruong().mainloop()