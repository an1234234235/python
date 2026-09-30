def gioi_thieu(ten, tuoi=18, lop="Chua ro"):
    print(f"Ten: {ten} - Tuoi: {tuoi} - Lop: {lop}")
gioi_thieu("An") # dung het gia tri mac dinh
gioi_thieu("Binh", 20) # ghi de tuoi
gioi_thieu("Chi", lop="CNTT01") # dung tham so tu khoa, bo qua tuoi
gioi_thieu(ten="Dung", lop="CNTT02", tuoi=19) # thu tu tham so tu khoa co the dao lon