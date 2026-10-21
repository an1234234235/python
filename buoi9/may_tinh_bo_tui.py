import tkinter as tk

def bam_nut(ky_tu):
    hien_tai = entry_hien_thi.get()
    entry_hien_thi.delete(0, tk.END)
    entry_hien_thi.insert(tk.END, hien_tai + str(ky_tu))

def xoa_man_hinh():
    entry_hien_thi.delete(0, tk.END)

def tinh_ket_qua():
    try:
        ket_qua = eval(entry_hien_thi.get())
        entry_hien_thi.delete(0, tk.END)
        entry_hien_thi.insert(tk.END, str(ket_qua))
    except Exception:
        entry_hien_thi.delete(0, tk.END)
        entry_hien_thi.insert(tk.END, "Loi")

cua_so = tk.Tk()
cua_so.title("May tinh bo tui")
cua_so.geometry("300x350")
cua_so.resizable(False, False)

entry_hien_thi = tk.Entry(cua_so, font=("Arial", 18), justify="right")
entry_hien_thi.grid(row=0, column=0, columnspan=4, padx=10, pady=15, ipady=8)

cac_nut = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

for (text, row, col) in cac_nut:
    if text == '=':
        btn = tk.Button(cua_so, text=text, width=5, height=2, font=("Arial", 12), command=tinh_ket_qua)
    else:
        btn = tk.Button(cua_so, text=text, width=5, height=2, font=("Arial", 12), command=lambda t=text: bam_nut(t))
    btn.grid(row=row, column=col, padx=5, pady=5)

btn_xoa = tk.Button(cua_so, text="C", width=24, height=2, font=("Arial", 12), command=xoa_man_hinh)
btn_xoa.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

cua_so.mainloop()