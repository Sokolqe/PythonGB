import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

import strings as st


# проверка на выигрыш
# проверяет нет ли победной комбинации в строчках, столбцах или по диагонали
# keys_values - массив
# who - кого надо проверить: нужно передать значение 'х' или '0'
def win_condition(keys_values, who):
    if (((keys_values[0] == who) and (keys_values[4] == who) and (keys_values[8] == who)) or
            ((keys_values[2] == who) and (keys_values[4] == who) and (keys_values[6] == who)) or
            ((keys_values[0] == who) and (keys_values[1] == who) and (keys_values[2] == who)) or
            ((keys_values[3] == who) and (keys_values[4] == who) and (keys_values[5] == who)) or
            ((keys_values[6] == who) and (keys_values[7] == who) and (keys_values[8] == who)) or
            ((keys_values[0] == who) and (keys_values[3] == who) and (keys_values[6] == who)) or
            ((keys_values[1] == who) and (keys_values[4] == who) and (keys_values[7] == who)) or
            ((keys_values[2] == who) and (keys_values[5] == who) and (keys_values[8] == who))):
        return True
    return False


# возвращает количество неопределенных ячеек (т.е. количество ячеек, в которые можно сходить)
# cell_data - массив данных из call_bck, полученных после нажатия на callBack-кнопку
def count_undef_cells(cell_data):
    counter = 0
    for i in cell_data:
        if i == st.SYMBOL_UNDEF:
            counter += 1
    return counter


# call_bck формат:
# n????????? - общее описание
# n - номер кнопки
# ? - один из вариантов значения клетки: смотри модуль strings, раздел "символы, которые используются"
# пример: 5❌❌⭕⭕❌❌◻◻❌
# означает, что была нажата пятая кнопка, и текущий вид поля:
# ❌❌⭕
# ⭕❌❌
# ◻◻❌
# данные обо всем состоянии поля необходимо помещать в кнопку, т.к. бот имеет доступ к информации только из текущего сообщения

# игра: проверка возможности хода крестиком, проверка победы крестика, ход бота (ноликом), проверка победы ботом
# возвращает:
# message - сообщение, которое надо отправить
# call_bck - данные для формирования callBack данных обновленного игрового поля
def game(call_bck):
    # -------------------------------------------------- global message  # использование глобальной переменной message
    message = st.ANSW_YOUR_TURN  # сообщение, которое вернется
    alert = None

    button_num = int(call_bck[0])  # считывание нажатой кнопки, преобразуя ее из строки в число
    if not button_num == 9:  # цифра 9 передается в первый раз в качестве заглушки. Т.е. если передана цифра 9, то клавиатура для сообщения создается впервые
        char_data = list(
            call_bck)  # строчка call_bck разбивается на посимвольный список "123" -> ['1', '2', '3']
        char_data.pop(0)  # удаление из списка первого элемента: который отвечает за выбор кнопки
        if char_data[
            button_num] == st.SYMBOL_UNDEF:  # проверка: если в нажатой кнопке не выбран крестик/нолик, то можно туда сходить крестику
            char_data[button_num] = st.SYMBOL_X  # эмуляция хода крестика
            if win_condition(char_data, st.SYMBOL_X):  # проверка: выиграл ли крестик после своего хода
                message = st.ANSW_YOU_WIN
            else:  # если крестик не выиграл, то может сходит бот, т.е. нолик
                if count_undef_cells(char_data) != 0:  # проверка: есть ли свободные ячейки для хода
                    # если есть, то ходит бот (нолик)
                    is_cycle_on = True
                    # запуск бесконечного цикла т.к. необходимо, чтобы бот походил в свободную клетку, а клетка выбирается случайным образом
                    while (is_cycle_on):
                        rand = random.randint(0, 8)  # генерация случайного числа - клетки, в которую сходит бот
                        if char_data[rand] == st.SYMBOL_UNDEF:  # если клетка неопределенна, то ходит бот
                            char_data[rand] = st.SYMBOL_O
                            is_cycle_on = False  # смена значения переменной для остановки цикла
                            if win_condition(char_data, st.SYMBOL_O):  # проверка: выиграл ли бот после своего кода
                                message = st.ANSW_BOT_WIN

        # если клетка, в которую хотел походить пользователь уже занята:
        else:
            alert = st.ALERT_CANNOT_MOVE_TO_THIS_CELL

        # проверка: остались ли свободные ячейки для хода и что изначальное сообщение не поменялось (означает, что победителя нет, и что это был не ошибочный ход)
        if count_undef_cells(char_data) == 0 and message == st.ANSW_YOUR_TURN:
            message = st.ANSW_DRAW

        # формирование новой строчки call_bck на основе сделанного хода
        call_bck = ''
        for c in char_data:
            call_bck += c

    # проверка, что игра закончилась (message равно одному из трех вариантов: победил Х, 0 или ничья):
    if message == st.ANSW_YOU_WIN or message == st.ANSW_BOT_WIN or message == st.ANSW_DRAW:
        message += '\n'
        for i in range(0, 3):
            message += '\n | '
            for j in range(0, 3):
                message += call_bck[j + i * 3] + ' | '
        call_bck = None  # обнуление call_bck

    return message, call_bck, alert


# Формат объекта клавиатуры
# в этом примере описана клавиатура из трех строчек кнопок
# в первой строчке две кнопки
# во 2-ой и 3-ей строчке по одной
# keyboard = [
#     # строчка из кнопок:
#     [
#         # собственно кнопки
#         InlineKeyboardButton("Кнопка 1", callback_data='1'),
#         InlineKeyboardButton("Кнопка 2", callback_data='2'),
#     ],
#     [InlineKeyboardButton("Кнопка 3", callback_data='3')],
#     [InlineKeyboardButton("Кнопка 4", callback_data='4')],
# ]
# для формирования объекта клавиатуры, необходимо выполнить следующую команду:
# InlineKeyboardMarkup(keyboard)

# возвращает клавиатуру для бота
# на вход получает call_bck - данные с callBack-кнопки
def get_keys(call_bck):
    keyboard = [[], [], []]  # заготовка объекта клавиатуры, которая вернется

    if call_bck != None:  # если
        # формирование объекта клавиатуры
        for i in range(0, 3):
            for j in range(0, 3):
                keyboard[i].append(
                    InlineKeyboardButton(call_bck[j + i * 3], callback_data=str(j + i * 3) + call_bck))

    return keyboard


def new_game(update, _):
    # сформировать callBack данные для первой игры, то есть строку, состояющую из 9 неопределенных символов
    data = ''
    for i in range(0, 9):
        data += st.SYMBOL_UNDEF

    # отправить сообщение для начала игры
    update.message.reply_text(st.ANSW_YOUR_TURN, reply_markup=InlineKeyboardMarkup(get_keys(data)))


def button(update, _):
    query = update.callback_query
    call_bck = query.data  # получение call_bck, скрытых в кнопке

    message, call_bck, alert = game(call_bck)  # игра
    if alert is None:  # если не получен сигнал тревоги (alert==None), то редактируем сообщение и меняем клавиатуру
        query.answer()  # обязательно нужно что-то отправить в ответ, иначе могут возникнуть проблемы с ботом
        query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(get_keys(call_bck)))
    else:  # если получен сигнал тревоги (alert!=None), то отобразить сообщение о тревоге
        query.answer(text=alert, show_alert=True)


def help_command(update, _):
    update.message.reply_text(st.ANSW_HELP)


if __name__ == '__main__':
    updater = Updater()

    updater.dispatcher.add_handler(CommandHandler('start', new_game))
    updater.dispatcher.add_handler(CommandHandler('new_game', new_game))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, help_command))  # обработчик на любое текстовое сообщение
    updater.dispatcher.add_handler(CallbackQueryHandler(button))  # добавление обработчика на CallBack кнопки

    updater.start_polling()
    updater.idle()
