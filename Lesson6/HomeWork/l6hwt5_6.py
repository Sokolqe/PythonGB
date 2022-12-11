from gbfunctions import random_list

lst_start = random_list(200)
lst_tuple = [i for i in enumerate(lst_start) if i[0] != i[1]]  # Task5
print(lst_tuple)
lst_div = [i for i in lst_tuple if not (i[0]+i[1]) % 5]  # Task6
print(lst_div)
