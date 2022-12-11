# 1- Определить, позицию второго вхождения строки в списке либо сообщить, что её нет.
# Примеры
# список: ["qwe", "asd", "zxc", "qwe", "ertqwe"], ищем: "qwe", ответ: 3
# список: ["йцу", "фыв", "ячс", "цук", "йцукен", "йцу"], ищем: "йцу", ответ: 5
# список: ["йцу", "фыв", "ячс", "цук", "йцукен"], ищем: "йцу", ответ: -1
# список: ["123", "234", 123, "567"], ищем: "123", ответ: -1
# список: [], ищем: "123", ответ: -1

from typing import List


def str_enc(lst: List[str], enc: int):
    what_find = input("What you want to find?:\n>> ")
    lst = [i[0] for i in enumerate(lst) if type(i[1]) == str and i[1] in what_find]
    return f"Position of {enc} encounter of {what_find} string:\n{lst[enc-1]}" \
           if len(lst) >= enc else -1


input_lst = ["qwe", "asd", "zxc", "qwe", "ertqwe"]
res = str_enc(input_lst, 2)
print(res)

input_lst = ["йцу", "фыв", "ячс", "цук", "йцукен", "йцу"]
res = str_enc(input_lst, 2)
print(res)

input_lst = ["йцу", "фыв", "ячс", "цук", "йцукен"]
res = str_enc(input_lst, 2)
print(res)

input_lst = ["123", "234", 123, "567"]
res = str_enc(input_lst, 2)
print(res)

input_lst = []
res = str_enc(input_lst, 2)
print(res)
