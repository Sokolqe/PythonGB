# 2. Напишите программу, которая найдёт произведение пар чисел списка.
# Парой считаем первый и последний элемент, второй и предпоследний и т.д.

from gbfunctions import give_int, random_list
from typing import List


def pair_mult(data_list: List[int]) -> List[int]:
    '''
    Gives multiplication of elements on opposite indexes

    :param data_list: list with elements
    :return: list with multiplication of elements on opposite indexes
    '''

    return [data_list[i]*data_list[-1 - i] for i in range(len(data_list)//2 + len(data_list) % 2)]


dt_lst = random_list(4)
print(dt_lst)
res = pair_mult(dt_lst)
print(res)

dt_lst = random_list(5)
print(dt_lst)
res = pair_mult(dt_lst)
print(res)

