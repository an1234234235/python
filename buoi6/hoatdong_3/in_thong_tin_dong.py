def in_thong_tin(ho_ten, tuoi, **kwargs):
    print(f"Ho ten: {ho_ten} - Tuoi: {tuoi}")
    for khoa, gia_tri in kwargs.items():
        print(f" {khoa}: {gia_tri}")
in_thong_tin("Nguyen Van A", 20, lop="CNTT01", que_quan="Ha Noi")
in_thong_tin("Tran Thi B", 21, email="b@example.com")