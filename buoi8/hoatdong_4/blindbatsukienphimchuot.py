import tkinter as tk
def khi_go_phim(event):
    nhan_thong_bao.config(text=f"Ban vua nhan phim: {event.char}")
def khi_click_chuot(event):
    nhan_thong_bao.config(text=f"Ban vua click tai toa do: ({event.x}, {event.y})")
cua_so = tk.Tk()
cua_so.title("Vi du bind()")

cua_so.geometry("400x250")
nhan_thong_bao = tk.Label(cua_so, text="Hay go phim hoac click chuot", font=("Arial",
12))
nhan_thong_bao.pack(pady=30)
cua_so.bind("<Key>", khi_go_phim)
cua_so.bind("<Button-1>", khi_click_chuot)
cua_so.mainloop()

"""
Yêu cầu: giải thích khác nhau giữa cách gắn sự kiện qua tham số command (chỉ dùng cho widget như
Button) và qua bind() (dùng được cho nhiều loại sự kiện và nhiều widget, kể cả cửa sổ chính).
Giai thích: Cách gắn sự kiện qua tham số command chỉ áp dụng cho các widget như Button, nơi bạn chỉ có thể gắn một hàm xử lý sự kiện duy nhất. Trong khi đó, bind() cho phép bạn gắn nhiều loại sự kiện khác nhau (như nhấn phím, click chuột) và có thể áp dụng cho nhiều widget khác nhau, kể cả cửa sổ chính. Điều này mang lại sự linh hoạt hơn trong việc xử lý các tương tác của người dùng với giao diện.
"""