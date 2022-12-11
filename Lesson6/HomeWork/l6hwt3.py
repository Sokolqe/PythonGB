# 3-Сформировать список из N членов последовательности.
# Для N = 5: 1, -3, 9, -27, 81 и т.д.

from gbfunctions import give_int

result = [(-3)**i for i in range(give_int('Type amount of numbers: '))]
print(result)