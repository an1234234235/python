import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path


THU_MUC_UNG_DUNG = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
TEN_FILE_CSDL = THU_MUC_UNG_DUNG / "truong_hoc.db"


@contextmanager
def ket_noi_csdl():
    ket_noi = sqlite3.connect(TEN_FILE_CSDL)
    ket_noi.execute("PRAGMA foreign_keys = ON")
    try:
        yield ket_noi
        ket_noi.commit()
    except Exception:
        ket_noi.rollback()
        raise
    finally:
        ket_noi.close()


def tao_bang_neu_chua_co():
    with ket_noi_csdl() as ket_noi:
        ket_noi.executescript(
            """CREATE TABLE IF NOT EXISTS giao_vien (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ho_ten TEXT NOT NULL,
                chuyen_mon TEXT NOT NULL DEFAULT '',
                dien_thoai TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS lop (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ten_lop TEXT NOT NULL UNIQUE,
                khoi TEXT NOT NULL,
                nam_hoc TEXT NOT NULL,
                giao_vien_id INTEGER REFERENCES giao_vien(id) ON DELETE SET NULL
            );
            CREATE TABLE IF NOT EXISTS hoc_sinh (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_hoc_sinh TEXT NOT NULL UNIQUE,
                ho_ten TEXT NOT NULL,
                ngay_sinh TEXT NOT NULL DEFAULT '',
                gioi_tinh TEXT NOT NULL DEFAULT '',
                nguoi_giam_ho TEXT NOT NULL DEFAULT '',
                dien_thoai_phu_huynh TEXT NOT NULL DEFAULT '',
                dia_chi TEXT NOT NULL DEFAULT '',
                lop_id INTEGER REFERENCES lop(id) ON DELETE SET NULL
            );
            CREATE TABLE IF NOT EXISTS diem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hoc_sinh_id INTEGER NOT NULL REFERENCES hoc_sinh(id) ON DELETE CASCADE,
                mon_hoc TEXT NOT NULL,
                hoc_ky TEXT NOT NULL,
                diem REAL NOT NULL CHECK (diem >= 0 AND diem <= 10),
                UNIQUE(hoc_sinh_id, mon_hoc, hoc_ky)
            );
            CREATE TABLE IF NOT EXISTS chuyen_can (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hoc_sinh_id INTEGER NOT NULL REFERENCES hoc_sinh(id) ON DELETE CASCADE,
                ngay TEXT NOT NULL,
                trang_thai TEXT NOT NULL CHECK (trang_thai IN ('Có mặt', 'Vắng', 'Muộn')),
                ghi_chu TEXT NOT NULL DEFAULT '',
                UNIQUE(hoc_sinh_id, ngay)
            );"""
        )


def them_giao_vien(ho_ten, chuyen_mon="", dien_thoai="", email=""):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            "INSERT INTO giao_vien (ho_ten, chuyen_mon, dien_thoai, email) VALUES (?, ?, ?, ?)",
            (ho_ten.strip(), chuyen_mon.strip(), dien_thoai.strip(), email.strip()),
        ).lastrowid


def sua_giao_vien(id_giao_vien, ho_ten, chuyen_mon="", dien_thoai="", email=""):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            "UPDATE giao_vien SET ho_ten = ?, chuyen_mon = ?, dien_thoai = ?, email = ? WHERE id = ?",
            (ho_ten.strip(), chuyen_mon.strip(), dien_thoai.strip(), email.strip(), id_giao_vien),
        ).rowcount


def lay_giao_vien():
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            "SELECT id, ho_ten, chuyen_mon, dien_thoai, email FROM giao_vien ORDER BY ho_ten COLLATE NOCASE"
        ).fetchall()


def xoa_giao_vien(id_giao_vien):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute("DELETE FROM giao_vien WHERE id = ?", (id_giao_vien,)).rowcount


def them_lop(ten_lop, khoi, nam_hoc, giao_vien_id=None):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            "INSERT INTO lop (ten_lop, khoi, nam_hoc, giao_vien_id) VALUES (?, ?, ?, ?)",
            (ten_lop.strip(), khoi.strip(), nam_hoc.strip(), giao_vien_id),
        ).lastrowid


def sua_lop(id_lop, ten_lop, khoi, nam_hoc, giao_vien_id=None):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            "UPDATE lop SET ten_lop = ?, khoi = ?, nam_hoc = ?, giao_vien_id = ? WHERE id = ?",
            (ten_lop.strip(), khoi.strip(), nam_hoc.strip(), giao_vien_id, id_lop),
        ).rowcount


def lay_lop():
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            """SELECT lop.id, lop.ten_lop, lop.khoi, lop.nam_hoc,
                      lop.giao_vien_id, COALESCE(giao_vien.ho_ten, '')
               FROM lop LEFT JOIN giao_vien ON giao_vien.id = lop.giao_vien_id
               ORDER BY lop.ten_lop COLLATE NOCASE"""
        ).fetchall()


def xoa_lop(id_lop):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute("DELETE FROM lop WHERE id = ?", (id_lop,)).rowcount


def them_hoc_sinh(ma_hoc_sinh, ho_ten, ngay_sinh="", gioi_tinh="", nguoi_giam_ho="", dien_thoai_phu_huynh="", dia_chi="", lop_id=None):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            """INSERT INTO hoc_sinh
               (ma_hoc_sinh, ho_ten, ngay_sinh, gioi_tinh, nguoi_giam_ho, dien_thoai_phu_huynh, dia_chi, lop_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (ma_hoc_sinh.strip(), ho_ten.strip(), ngay_sinh.strip(), gioi_tinh.strip(), nguoi_giam_ho.strip(), dien_thoai_phu_huynh.strip(), dia_chi.strip(), lop_id),
        ).lastrowid


def sua_hoc_sinh(id_hoc_sinh, ma_hoc_sinh, ho_ten, ngay_sinh="", gioi_tinh="", nguoi_giam_ho="", dien_thoai_phu_huynh="", dia_chi="", lop_id=None):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            """UPDATE hoc_sinh SET ma_hoc_sinh = ?, ho_ten = ?, ngay_sinh = ?, gioi_tinh = ?,
               nguoi_giam_ho = ?, dien_thoai_phu_huynh = ?, dia_chi = ?, lop_id = ? WHERE id = ?""",
            (ma_hoc_sinh.strip(), ho_ten.strip(), ngay_sinh.strip(), gioi_tinh.strip(), nguoi_giam_ho.strip(), dien_thoai_phu_huynh.strip(), dia_chi.strip(), lop_id, id_hoc_sinh),
        ).rowcount


def lay_hoc_sinh(tu_khoa="", lop_id=None):
    tu_khoa = f"%{tu_khoa.strip()}%"
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            """SELECT hoc_sinh.id, hoc_sinh.ma_hoc_sinh, hoc_sinh.ho_ten, hoc_sinh.ngay_sinh,
                      hoc_sinh.gioi_tinh, hoc_sinh.nguoi_giam_ho, hoc_sinh.dien_thoai_phu_huynh,
                      hoc_sinh.dia_chi, hoc_sinh.lop_id, COALESCE(lop.ten_lop, '')
               FROM hoc_sinh LEFT JOIN lop ON lop.id = hoc_sinh.lop_id
               WHERE (hoc_sinh.ma_hoc_sinh LIKE ? COLLATE NOCASE OR hoc_sinh.ho_ten LIKE ? COLLATE NOCASE)
                 AND (? IS NULL OR hoc_sinh.lop_id = ?)
               ORDER BY hoc_sinh.ho_ten COLLATE NOCASE""",
            (tu_khoa, tu_khoa, lop_id, lop_id),
        ).fetchall()


def xoa_hoc_sinh(id_hoc_sinh):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute("DELETE FROM hoc_sinh WHERE id = ?", (id_hoc_sinh,)).rowcount


def them_hoac_sua_diem(hoc_sinh_id, mon_hoc, hoc_ky, diem):
    with ket_noi_csdl() as ket_noi:
        ket_noi.execute(
            """INSERT INTO diem (hoc_sinh_id, mon_hoc, hoc_ky, diem) VALUES (?, ?, ?, ?)
               ON CONFLICT(hoc_sinh_id, mon_hoc, hoc_ky) DO UPDATE SET diem = excluded.diem""",
            (hoc_sinh_id, mon_hoc.strip(), hoc_ky.strip(), float(diem)),
        )


def lay_diem():
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            """SELECT diem.id, diem.hoc_sinh_id, hoc_sinh.ma_hoc_sinh, hoc_sinh.ho_ten,
                      diem.mon_hoc, diem.hoc_ky, diem.diem
               FROM diem JOIN hoc_sinh ON hoc_sinh.id = diem.hoc_sinh_id
               ORDER BY diem.hoc_ky, hoc_sinh.ho_ten COLLATE NOCASE, diem.mon_hoc"""
        ).fetchall()


def xoa_diem(id_diem):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute("DELETE FROM diem WHERE id = ?", (id_diem,)).rowcount


def them_hoac_sua_chuyen_can(hoc_sinh_id, ngay, trang_thai, ghi_chu=""):
    with ket_noi_csdl() as ket_noi:
        ket_noi.execute(
            """INSERT INTO chuyen_can (hoc_sinh_id, ngay, trang_thai, ghi_chu) VALUES (?, ?, ?, ?)
               ON CONFLICT(hoc_sinh_id, ngay) DO UPDATE
               SET trang_thai = excluded.trang_thai, ghi_chu = excluded.ghi_chu""",
            (hoc_sinh_id, ngay.strip(), trang_thai, ghi_chu.strip()),
        )


def lay_chuyen_can():
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute(
            """SELECT chuyen_can.id, chuyen_can.hoc_sinh_id, hoc_sinh.ma_hoc_sinh,
                      hoc_sinh.ho_ten, chuyen_can.ngay, chuyen_can.trang_thai, chuyen_can.ghi_chu
               FROM chuyen_can JOIN hoc_sinh ON hoc_sinh.id = chuyen_can.hoc_sinh_id
               ORDER BY chuyen_can.ngay DESC, hoc_sinh.ho_ten COLLATE NOCASE"""
        ).fetchall()


def xoa_chuyen_can(id_chuyen_can):
    with ket_noi_csdl() as ket_noi:
        return ket_noi.execute("DELETE FROM chuyen_can WHERE id = ?", (id_chuyen_can,)).rowcount


def lay_tong_quan():
    with ket_noi_csdl() as ket_noi:
        return {
            "hoc_sinh": ket_noi.execute("SELECT COUNT(*) FROM hoc_sinh").fetchone()[0],
            "lop": ket_noi.execute("SELECT COUNT(*) FROM lop").fetchone()[0],
            "giao_vien": ket_noi.execute("SELECT COUNT(*) FROM giao_vien").fetchone()[0],
            "diem": ket_noi.execute("SELECT COUNT(*) FROM diem").fetchone()[0],
            "vang_hom_nay": ket_noi.execute(
                "SELECT COUNT(*) FROM chuyen_can WHERE ngay = date('now', 'localtime') AND trang_thai = 'Vắng'"
            ).fetchone()[0],
        }

def lay_thong_ke():
    with ket_noi_csdl() as ket_noi:
        theo_lop = ket_noi.execute(
            """SELECT lop.ten_lop,
                      (SELECT COUNT(*) FROM hoc_sinh WHERE hoc_sinh.lop_id = lop.id),
                      (SELECT ROUND(AVG(diem.diem), 2)
                       FROM diem JOIN hoc_sinh ON hoc_sinh.id = diem.hoc_sinh_id
                       WHERE hoc_sinh.lop_id = lop.id),
                      (SELECT COUNT(*) FROM chuyen_can
                       JOIN hoc_sinh ON hoc_sinh.id = chuyen_can.hoc_sinh_id
                       WHERE hoc_sinh.lop_id = lop.id AND chuyen_can.trang_thai = 'Vắng')
               FROM lop ORDER BY lop.ten_lop COLLATE NOCASE"""
        ).fetchall()
        theo_mon_hoc = ket_noi.execute(
            """SELECT mon_hoc, hoc_ky, COUNT(*), ROUND(AVG(diem), 2), MIN(diem), MAX(diem)
               FROM diem GROUP BY mon_hoc, hoc_ky
               ORDER BY hoc_ky, mon_hoc COLLATE NOCASE"""
        ).fetchall()
        theo_chuyen_can = ket_noi.execute(
            "SELECT trang_thai, COUNT(*) FROM chuyen_can GROUP BY trang_thai ORDER BY trang_thai"
        ).fetchall()
        return {
            "tong_quan": {
                "hoc_sinh": ket_noi.execute("SELECT COUNT(*) FROM hoc_sinh").fetchone()[0],
                "lop": ket_noi.execute("SELECT COUNT(*) FROM lop").fetchone()[0],
                "giao_vien": ket_noi.execute("SELECT COUNT(*) FROM giao_vien").fetchone()[0],
                "diem": ket_noi.execute("SELECT COUNT(*) FROM diem").fetchone()[0],
                "ban_ghi_chuyen_can": ket_noi.execute("SELECT COUNT(*) FROM chuyen_can").fetchone()[0],
            },
            "theo_lop": theo_lop,
            "theo_mon_hoc": theo_mon_hoc,
            "theo_chuyen_can": theo_chuyen_can,
        }