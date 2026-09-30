import utils
print(utils.dao_nguoc_chuoi("Python"))
print(utils.kiem_tra_palindrome("madam"))
print(utils.chuan_hoa_ho_ten(" nguyen van an "))
print(utils.uscln(24, 36))
print(utils.kiem_tra_nguyen_to(29))

"""
Yêu cầu: Giải thích vì sao utils.py và main.py cần đặt trong cùng một thư mục để lệnh import utils hoạt động
đúng.
Giải thích: Khi bạn sử dụng lệnh import utils trong main.py, Python sẽ tìm kiếm module utils trong cùng thư mục với main.py. Nếu utils.py không nằm trong cùng thư mục, Python sẽ không thể tìm thấy module đó và sẽ báo lỗi ImportError. Do đó, để lệnh import utils hoạt động đúng, cả hai file cần được đặt trong cùng một thư mục.
"""