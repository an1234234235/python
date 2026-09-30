def fibonacci_de_quy(n):
    if n <= 1: # dieu kien dung
        return n
    return fibonacci_de_quy(n - 1) + fibonacci_de_quy(n - 2)
for i in range(10):
    print(fibonacci_de_quy(i), end=" ")
print()

"""
Yêu cầu: Thử tính fibonacci_de_quy(30), quan sát thời gian chạy chậm hơn hẳn so với
giai_thua_de_quy(30), trả lời vì sao đệ quy Fibonacci "tốn kém" hơn (gợi ý: số lần gọi hàm tăng theo cấp số
nhân do tính lại nhiều lần các giá trị trùng nhau).
Giải thích: Đệ quy Fibonacci tốn kém hơn vì nó tính toán lại nhiều giá trị trùng nhau. Khi tính fibonacci_de_quy(n), hàm sẽ gọi lại chính nó để tính fibonacci_de_quy(n-1) và fibonacci_de_quy(n-2). Điều này dẫn đến việc nhiều giá trị được tính lại nhiều lần, tạo ra một số lượng lớn các lời gọi hàm, làm tăng thời gian chạy của chương trình theo cấp số nhân. Trong khi đó, giai_thua_de_quy chỉ tính toán một lần cho mỗi giá trị, do đó nhanh hơn nhiều.
"""