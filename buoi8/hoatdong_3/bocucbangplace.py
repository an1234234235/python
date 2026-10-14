import tkinter as tk
cua_so = tk.Tk()
cua_so.title("Bo cuc bang place()")
cua_so.geometry("300x250")
tk.Label(cua_so, text="Ho ten:").place(x=20, y=20)
tk.Label(cua_so, text="Tuoi:").place(x=20, y=60)
tk.Label(cua_so, text="Email:").place(x=20, y=100)
tk.Button(cua_so, text="Dong y").place(x=40, y=160)
tk.Button(cua_so, text="Huy").place(x=150, y=160)
cua_so.mainloop()

"""
Câu hỏi:
• pack() sắp xếp widget theo nguyên tắc nào (trên-dưới hay trái-phải)? Tham số side dùng để làm gì?
• grid() phù hợp nhất với loại giao diện nào (gợi ý: form nhiều dòng nhãn + ô nhập)?
• place() có ưu điểm và nhược điểm gì so với pack()/grid() khi cửa sổ bị thay đổi kích thước?

Giai thích:
• pack() sắp xếp widget theo nguyên tắc trên-dưới hoặc trái-phải, tùy thuộc vào tham số side. Tham số side xác định hướng sắp xếp của widget (top, bottom, left, right).
• grid() phù hợp nhất với loại giao diện có nhiều dòng nhãn và ô nhập,
vì nó cho phép sắp xếp các widget theo dạng lưới (grid) với hàng và cột.
• place() có ưu điểm là cho phép đặt widget ở vị trí chính xác theo tọa độ x, y, nhưng nhược điểm là khi cửa sổ bị thay đổi kích thước, các widget sẽ không tự động điều chỉnh vị trí và kích thước, dẫn đến giao diện không linh hoạt.
"""