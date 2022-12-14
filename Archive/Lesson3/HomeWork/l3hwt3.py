# 3. Напишите программу, которая будет преобразовывать десятичное число в двоичное.
# Без использования встроенной функции преобразования, без строк.
# in
# 88
# out
# 1011000

def int_to_binary(number):
    binary = []
    while number // 2 != 0:
        binary.insert(0, number % 2)
        number //= 2
    binary.insert(0, number)
    return binary


num = int(input('Enter natural number: '))
print("".join(map(str, int_to_binary(num))))
