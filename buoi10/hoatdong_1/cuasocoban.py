import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class CuaSoDauTien(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cua so PyQt dau tien")
        self.resize(300, 200)

        layout = QVBoxLayout()
        nhan = QLabel("Xin chao PyQt!")
        layout.addWidget(nhan)
        self.setLayout(layout)

app = QApplication(sys.argv)
cua_so = CuaSoDauTien()
cua_so.show()
sys.exit(app.exec_())

"""
Yêu cầu: so sánh nhanh cấu trúc trên với cua_so = tk.Tk() + mainloop() của Tkinter —
app.exec_() đóng vai trò tương tự mainloop() như thế nào?
Giải thích Cấu trúc của PyQt và Tkinter có những điểm tương đồng nhưng cũng có những khác biệt quan trọng.
Cấu trúc của PyQt và Tkinter đều phục vụ mục đích tạo giao diện người dùng đồ họa (GUI) trong Python, nhưng chúng có những điểm tương đồng và khác biệt quan trọng.

"""