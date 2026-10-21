#Hoạt động 3: Listbox & Combobox
#Bài tập 3.1 – Listbox
import tkinter as tk

cua_so = tk.Tk()
cua_so.title("Vi du Listbox")
cua_so.geometry("300x250")

listbox_mon_hoc = tk.Listbox(cua_so, selectmode="single")
for mon in ["Toan", "Ly", "Hoa", "Van", "Anh"]:
    listbox_mon_hoc.insert(tk.END, mon)
listbox_mon_hoc.pack(pady=10)

def xem_mon_da_chon():
    lua_chon = listbox_mon_hoc.curselection()
    if lua_chon:
        nhan_ket_qua.config(text=f"Mon da chon: {listbox_mon_hoc.get(lua_chon[0])}")

tk.Button(cua_so, text="Xem mon da chon", command=xem_mon_da_chon).pack(pady=5)
nhan_ket_qua = tk.Label(cua_so, text="")
nhan_ket_qua.pack()

cua_so.mainloop()
#Bài tập 3.2 – Combobox (ttk)
import tkinter as tk
from tkinter import ttk

cua_so = tk.Tk()
cua_so.title("Vi du Combobox")
cua_so.geometry("300x180")

tk.Label(cua_so, text="Chon thanh pho:").pack(pady=10)

combobox_thanh_pho = ttk.Combobox(cua_so, values=["Ha Noi", "Da Nang", "TP.HCM", "Hue"])
combobox_thanh_pho.current(0) # Chon gia tri dau tien lam mac dinh
combobox_thanh_pho.pack(pady=5)

def xem_thanh_pho():
    nhan_ket_qua.config(text=f"Ban chon: {combobox_thanh_pho.get()}")

tk.Button(cua_so, text="Xac nhan", command=xem_thanh_pho).pack(pady=10)
nhan_ket_qua = tk.Label(cua_so, text="")
nhan_ket_qua.pack()

cua_so.mainloop()
#Hoạt động 4: Scale – Thanh trượt chọn giá trị
import tkinter as tk

cua_so = tk.Tk()
cua_so.title("Vi du Scale")
cua_so.geometry("300x180")

def khi_keo_thanh_truot(gia_tri):
    nhan_gia_tri.config(text=f"Gia tri hien tai: {gia_tri}")

thanh_truot = tk.Scale(cua_so, from_=0, to=100, orient="horizontal", command=khi_keo_thanh_truot)
thanh_truot.pack(pady=20, padx=20, fill="x")

nhan_gia_tri = tk.Label(cua_so, text="Gia tri hien tai: 0")
nhan_gia_tri.pack()

cua_so.mainloop()