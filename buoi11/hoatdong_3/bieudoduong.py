from pathlib import Path

import matplotlib.pyplot as plt

lan_kiem_tra = [1, 2, 3]
diem_qua_cac_lan = [6.5, 7.5, 8.5]
plt.figure(figsize=(6, 4))
plt.plot(lan_kiem_tra, diem_qua_cac_lan, marker="o", color="green")
plt.title("Xu huong diem qua cac lan kiem tra")
plt.xlabel("Lan kiem tra")
plt.ylabel("Diem")
plt.tight_layout()
output_path = Path(__file__).with_name("bieu_do_duong.png")
plt.savefig(output_path)
plt.show()
