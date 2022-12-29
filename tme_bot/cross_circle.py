import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from typing import List
import strings as st


def win_condition(keys_values: List, who: str) -> bool:
    """
    Проверка условия выигрыша. Ищет комбинации в строках, стлобцах, по диагонали.
    :param keys_values: список со значениями
    :param who: само значение, "X" или "O"
    :return: булевое значение
    """
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


def count_undef_cells(cell_data: List) -> int:
    """
    Возращает количество пустых ячеек, доступных для хода.
    :param cell_data: список с данными из call_bck, полученные после нажатия на кнопку
    :return: количество ячеек
    """
    counter = 0
    for i in cell_data:
        if i == st.SYMBOL_UNDEF:
            counter += 1
    return counter


def game(call_bck: str):
    """
    Проверка возможности хода крестиком (человеком), затем проверяет условие выигрыша,
    после чего передает ход нолику (боту)
    :param call_bck: возвращаемые данные из кнопки, имеет формат строки, вида
    "1XXOO--XX" - где, 1 - номер кнопки, а следующие символы - текущее состояние поля
    :return: message - сообщение, которое нужно отправить,
    call_bck - данные кнопок для обновленного игрового поля
    alert - используется для проверки возможности хода
    """
    message = st.ANSW_YOUR_TURN
    alert = None
    button_num = int(call_bck[0])
    if not button_num == 9:
        char_data = list(call_bck)
        char_data.pop(0)
        if char_data[button_num] == st.SYMBOL_UNDEF:
            char_data[button_num] = st.SYMBOL_X
            if win_condition(char_data, st.SYMBOL_X):
                message = st.ANSW_YOU_WIN
            else:
                if count_undef_cells(char_data) != 0:
                    is_cycle_on = True
                    while is_cycle_on:
                        rand = random.randint(0, 8)
                        if char_data[rand] == st.SYMBOL_UNDEF:
                            char_data[rand] = st.SYMBOL_O
                            is_cycle_on = False
                            if win_condition(char_data, st.SYMBOL_O):
                                message = st.ANSW_BOT_WIN
        else:
            alert = st.ALERT_CANNOT_MOVE_TO_THIS_CELL

        if count_undef_cells(char_data) == 0 and message == st.ANSW_YOUR_TURN:
            message = st.ANSW_DRAW

        call_bck = ''
        for c in char_data:
            call_bck += c

    if message == st.ANSW_YOU_WIN or message == st.ANSW_BOT_WIN or message == st.ANSW_DRAW:
        message += '\n'
        for i in range(0, 3):
            message += '\n | '
            for j in range(0, 3):
                message += call_bck[j + i * 3] + ' | '
        call_bck = None

    return message, call_bck, alert


def get_keys(call_bck: str) -> List:
    """
    Формат клавиатуры, где в одной строке расположено 3 кнопки.
    Всего таких строк - тоже три
    :param call_bck: данные с кнопки
    :return: клавиатуру
    """
    keyboard = [[], [], []]
    if call_bck != None:
        for i in range(0, 3):
            for j in range(0, 3):
                keyboard[i].append(
                    InlineKeyboardButton(call_bck[j + i * 3], callback_data=str(j + i * 3) + call_bck))
    return keyboard


def crs_crcl_strt(update, _):
    """
    Формирует данные для кнопок для первой игры, а именно строку,
    состоящую из 9 неопределенных символов.
    Затем отправляет приглашение для следующего хода
    :param update:
    :param _:
    :return:
    """
    data = ''
    for i in range(0, 9):
        data += st.SYMBOL_UNDEF
    update.message.reply_text(st.ANSW_YOUR_TURN, reply_markup=InlineKeyboardMarkup(get_keys(data)))


def button(update, _):
    """
    Метод для работы с кнопками. Считывает последнее нажатие,
    получает данные и запускает/продолжает игру, меняя игровое поле.
    :param update: данные о событии на сервере
    :param _:
    :return:
    """
    query = update.callback_query
    call_bck = query.data

    message, call_bck, alert = game(call_bck)
    if alert is None:
        query.answer()
        query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(get_keys(call_bck)))
    else:
        query.answer(text=alert, show_alert=True)


def help_command(update, _):
    """
    Команда /help для бота, показывает его возможности
    :param update: данные о событии на сервере
    :param _:
    :return:
    """
    update.message.reply_text(st.ANSW_HELP)


if __name__ == '__main__':
    updater = Updater()

    updater.dispatcher.add_handler(CommandHandler('start', crs_crcl_strt))
    updater.dispatcher.add_handler(CommandHandler('cross&circle', crs_crcl_strt))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, help_command))

    updater.start_polling()
    updater.idle()
    print("Server is started")
