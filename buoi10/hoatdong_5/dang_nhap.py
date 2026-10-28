
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox


class CuaSoDangNhap(QDialog):
    def __init__(self):
        super().__init__()

        # Lay duong dan file giao dien
        thu_muc = os.path.dirname(os.path.abspath(__file__))
        duong_dan_ui = os.path.join(
            thu_muc, "form_dang_nhap.ui"
        )

        # Kiem tra file giao dien co ton tai khong
        if not os.path.exists(duong_dan_ui):
            raise FileNotFoundError(
                f"Khong tim thay file giao dien: {duong_dan_ui}"
            )

        # Nap giao dien
        uic.loadUi(duong_dan_ui, self)

        # Dat tieu de cua so
        self.setWindowTitle("Dang nhap")

        # Ket noi nut dang nhap
        self.nut_dang_nhap.clicked.connect(
            self.xu_ly_dang_nhap
        )

    def xu_ly_dang_nhap(self):
        tai_khoan = self.o_nhap_tai_khoan.text().strip()
        mat_khau = self.o_nhap_mat_khau.text()

        if not tai_khoan or not mat_khau:
            QMessageBox.critical(
                self,
                "Loi",
                "Vui long nhap day du tai khoan va mat khau!"
            )
            return

        QMessageBox.information(
            self,
            "Thanh cong",
            f"Xin chao {tai_khoan}, dang nhap thanh cong!"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cua_so = CuaSoDangNhap()
    cua_so.show()
    sys.exit(app.exec_())
