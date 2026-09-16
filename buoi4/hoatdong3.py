#bài 3.1
diem_mon_hoc = {"Toan": 8.0, "Ly": 7.5, "Hoa": 9.0, "Van": 6.5} 
diem_cong_diem = {mon: round(diem + 0.5, 2) for mon, diem in diem_mon_hoc.items()}
print(diem_cong_diem)
ten_mon_viet_hoa = {mon.upper(): diem for mon, diem in diem_mon_hoc.items()}
print(ten_mon_viet_hoa)
#bài 3.2
mon_hoc_ky1 = {"Toan", "Ly", "Hoa", "Van"} 
mon_hoc_ky2 = {"Toan", "Anh", "Tin", "Van"} 
print(mon_hoc_ky1 & mon_hoc_ky2) # giao: mon hoc chung 2 hoc ky 
print(mon_hoc_ky1 | mon_hoc_ky2) # hop: tat ca mon hoc ca 2 hoc ky
print(mon_hoc_ky1 - mon_hoc_ky2) # mon chi co o hoc ky 1    
"""
Yêu cầu: So sánh Set với Dictionary - Set có lưu cặp khóa-giá trị không? Vì sao Set không cho  phép phần tử trùng lặp?
Giải thích: Set là một tập hợp các phần tử duy nhất, không lưu trữ cặp khóa-giá trị như Dictionary. Set không cho phép phần tử trùng lặp vì nó được thiết kế để đảm bảo rằng mỗi phần tử chỉ xuất hiện một lần, giúp dễ dàng kiểm tra sự tồn tại của phần tử và thực hiện các phép toán tập hợp như giao, hợp, hiệu.
"""