# file: hello.py
# bài 1-1
ten = "SinhVien"
print("Xin chao",ten)  
print("Day la chuong trinh python dau tien cua toi.")
"""
Yêu cầu: giải thích vì sao phải ép kiểu int()/float() cho nam_sinh và diem_tb, trong khi ho_ten thì không
cần.
Trả lời Trong Python, khi bạn nhập dữ liệu từ người dùng bằng hàm `input()`, dữ liệu đó luôn được trả về dưới dạng chuỗi (string). Vì vậy, nếu bạn muốn sử dụng dữ liệu đó cho các phép toán số học hoặc so sánh số học, bạn cần phải ép kiểu dữ liệu từ chuỗi sang kiểu số tương ứng. 
"""

# bài 1-2
print("Python", "la", "ngon", "ngu", "lap trinh", sep="-")
print("Dong 1", end=" |\n")
print("Dong 2\n")

"""
Yêu cầu: thử đổi sep thành nhiều ký tự khác nhau (", ", "\n") và quan sát kết quả rồi giải thích.
Trả lời: Tham số `sep` trong hàm `print()` xác định ký tự hoặc chuỗi ký tự được sử dụng để phân tách các đối số khi in ra. Khi bạn thay đổi giá trị của `sep`, kết quả in ra sẽ thay đổi theo ký tự hoặc chuỗi bạn đã chỉ định. Ví dụ, nếu bạn đặt `sep=", "`, các từ sẽ được phân tách bằng dấu phẩy và khoảng trắng; nếu bạn đặt `sep="\n"`, mỗi từ sẽ được in trên một dòng mới. Điều này giúp bạn kiểm soát cách dữ liệu được trình bày khi in ra màn hình.
"""

# bài 1-3
ho_ten = input("Nhap ho ten: ")
nam_sinh = int(input("Nhap nam sinh: "))
diem_tb = float(input("Nhap diem trung binh: "))
# f-string
print(f"Ho ten: {ho_ten} - Nam sinh: {nam_sinh} - DTB: {diem_tb:.2f}")
# str.format()
print("Ho ten: {} - Nam sinh: {} - DTB: {:.2f}".format(ho_ten, nam_sinh, diem_tb))
# toán tử %
print("Ho ten: %s - Nam sinh: %d - DTB: %.2f" % (ho_ten, nam_sinh, diem_tb))
"""
Thảo luận: 3 cách trên cho kết quả giống nhau, vậy vì sao Python hiện nay khuyến khích dùng f-string
hơn?
Trả lời: Python hiện nay khuyến khích sử dụng f-string vì nó cung cấp cú pháp ngắn gọn, dễ đọc và trực quan hơn so với các phương pháp khác như `str.format()` hoặc toán tử `%`. F-string cho phép bạn nhúng trực tiếp các biểu thức Python vào trong chuỗi bằng cách sử dụng dấu ngoặc nhọn `{}`, giúp mã nguồn trở nên rõ ràng và dễ hiểu hơn. Ngoài ra, f-string cũng có hiệu suất tốt hơn, đặc biệt khi xử lý nhiều biến hoặc biểu thức phức tạp.
"""
