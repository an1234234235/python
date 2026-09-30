def giai_thua_de_quy(n):
    if n <= 1: # dieu kien dung
        return 1
    return n * giai_thua_de_quy(n - 1)

def giai_thua_lap(n):
    ket_qua = 1
    for i in range(1, n + 1):
        ket_qua *= i
    return ket_qua

print(giai_thua_de_quy(5), "-", giai_thua_lap(5))