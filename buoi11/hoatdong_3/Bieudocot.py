from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

csv_path = Path(__file__).parent.parent / "hoatdong_2" / "diem_sinh_vien.csv"
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

diem_trung_binh_mon = df.groupby("mon_hoc")["diem"].mean()
plt.figure(figsize=(6, 4))
plt.bar(diem_trung_binh_mon.index, diem_trung_binh_mon.values, color="skyblue")
plt.title("Diem trung binh theo mon hoc")
plt.xlabel("Mon hoc")
plt.ylabel("Diem trung binh")
plt.tight_layout()
output_path = Path(__file__).with_name("bieu_do_cot.png")
plt.savefig(output_path)
plt.show()

