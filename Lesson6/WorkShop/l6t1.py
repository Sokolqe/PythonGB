# Напишите программу вычисления арифметического выражения заданного строкой.
# Используйте операции +,-,/,*. приоритет операций стандартный.

def find_hooks(data):
    try:
        last_hook = data.index(')')
    except ValueError:
        last_hook = '-1'
    if last_hook != '-1':
        try:
            first_hook = list(reversed(data))
            first_hook = len(first_hook) - 1 - first_hook.index('(')
        except ValueError:
            first_hook = 0
        print(data)
        print(last_hook, first_hook)
        print(data[first_hook + 1:last_hook])
        data[first_hook] = priority(data[first_hook + 1:last_hook], '/', '*')
        data[first_hook] = priority(data[first_hook], '-', '+')
        data[first_hook] = data[first_hook][0]
        for i in range(last_hook, first_hook, -1):
            data.pop(i)
        return data
    else:
        return data


def priority(data, arg1, arg2):
    for i in range(len(data)):
        try:
            ind1 = data.index(arg1)
        except ValueError:
            ind1 = -1
        try:
            ind2 = data.index(arg2)
        except ValueError:
            ind2 = -1
        min_ind = min(ind1, ind2)
        max_ind = max(ind1, ind2)
        if min_ind != -1:
            data[min_ind - 1] = op(data[min_ind], data[min_ind - 1], data[min_ind + 1])
            data.pop(min_ind)
            data.pop(min_ind)
        elif min_ind == -1 and max_ind != -1:
            data[max_ind - 1] = op(data[max_ind], data[max_ind - 1], data[max_ind + 1])
            data.pop(max_ind)
            data.pop(max_ind)
        elif min_ind == max_ind == -1:
            break
    return data


def op(operation: str, arg1: str, arg2: str):
    if operation == '*':
        return int(arg1) * int(arg2)
    elif operation == '/':
        return int(arg1) / int(arg2)
    elif operation == '+':
        return int(arg1) + int(arg2)
    elif operation == '-':
        return int(arg1) - int(arg2)


lst = input().split()
iterations = lst.count(')')
for i in range(iterations):
    lst = find_hooks(lst)
    print(lst)
lst = priority(lst, '/', '*')
print(lst)
lst = priority(lst, '-', '+')
print(f'Result = {lst[0]}')
