from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, CallbackQueryHandler, ConversationHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from random import randint
import logging


def catch_message(update: Update):
    message = update.message.text
    if 'прив' in message.lower:
        update.message.reply_text(f'Добрейший вечерочек, смотри что умею!')

    else:
        update.message.reply_text(f'Перейдем сразу к делу...')


# Ведение журнала логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Этапы/состояния разговора
FIRST, SECOND = range(2)
# Данные обратного вызова
ONE, TWO = range(2)


def keys(key_tuples):
    return [
        [
            InlineKeyboardButton(key_tuples[0][0], callback_data=key_tuples[0][1]),
            InlineKeyboardButton(key_tuples[1][0], callback_data=key_tuples[1][1]),
            InlineKeyboardButton(key_tuples[2][0], callback_data=key_tuples[2][1]),
        ], [
            InlineKeyboardButton(key_tuples[3][0], callback_data=key_tuples[3][1]),
            InlineKeyboardButton(key_tuples[4][0], callback_data=key_tuples[4][1]),
            InlineKeyboardButton(key_tuples[5][0], callback_data=key_tuples[5][1]),
        ], [
            InlineKeyboardButton(key_tuples[6][0], callback_data=key_tuples[6][1]),
            InlineKeyboardButton(key_tuples[7][0], callback_data=key_tuples[7][1]),
            InlineKeyboardButton(key_tuples[8][0], callback_data=key_tuples[8][1]),
        ]
    ]


def start(update, key_tuples):
    """Вызывается по команде `/start`."""
    # Получаем пользователя, который запустил команду `/start`
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    # Создаем `InlineKeyboard`, где каждая кнопка имеет
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка,
    # в свою очередь, является списком `[[...]]`
    keyboard = keys(key_tuples)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
    update.message.reply_text(
        text=f"{user.first_name}, сделайте Ваш ход", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
    return FIRST


def start_over(update, key_tuples):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    # На запросы обратного вызова необходимо ответить,
    # даже если уведомление для пользователя не требуется.
    # В противном случае у некоторых клиентов могут возникнуть проблемы.
    query.answer()
    keyboard = keys(key_tuples)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отредактируем сообщение, вызвавшее обратный вызов.
    # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text=f"{user.first_name}, сделайте Ваш ход", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
    return FIRST


def turn(update, key_tuples):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    choice_index = query.data
    key_tuples[choice_index + 1][0], key_tuples[choice_index + 1][1] = "X", str(None)
    query.answer()
    keyboard = keys(key_tuples)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отредактируем сообщение, вызвавшее обратный вызов.
    # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text=f"{user.first_name}, сделайте Ваш ход", reply_markup=reply_markup
    )
    return FIRST


def win_condition(key_tuples):
    """
    Checks win condition and returns info about success

    :param key_tuples: list with field's cells
    :param player: list with players number and name
    :return:
    """

    if key_tuples[0][0] == key_tuples[1][0] == key_tuples[2][0] \
            or key_tuples[3][0] == key_tuples[4][0] == key_tuples[5][0] \
            or key_tuples[6][0] == key_tuples[7][0] == key_tuples[8][0] \
            or key_tuples[0][0] == key_tuples[3][0] == key_tuples[6][0] \
            or key_tuples[1][0] == key_tuples[4][0] == key_tuples[7][0] \
            or key_tuples[2][0] == key_tuples[5][0] == key_tuples[8][0] \
            or key_tuples[0][0] == key_tuples[4][0] == key_tuples[8][0] \
            or key_tuples[2][0] == key_tuples[4][0] == key_tuples[6][0]:
        return False
    else:
        return True


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def turn_maker(update, key_tuples):
    while win_condition(key_tuples):
        turn(update, key_tuples=key_tuples)
        query = update.callback_query
        query.answer()
        choice_bot = randint(0, 8)
        while key_tuples[choice_bot + 1][0].isdigit():
            choice_bot = randint(0, 8)
        key_tuples[choice_bot + 1][0], key_tuples[choice_bot + 1][1] = "O", str(None)
        query.edit_message_text(text=f"Я выбрал {choice_bot+1}")
    return end(Update, None)


updater = Updater()
dispatcher = updater.dispatcher

# Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
# Используем параметр `pattern` для передачи `CallbackQueries` с
# определенным шаблоном данных соответствующим обработчикам
# ^ - означает "начало строки"
# $ - означает "конец строки"
# Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={  # словарь состояний разговора, возвращаемых callback функциями
        FIRST: [
            CallbackQueryHandler(turn_maker, pattern='^' + str(ONE) + '$'),
        ],
        SECOND: [
            CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
            CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
        ],
    },
    fallbacks=[CommandHandler('start', start)],
)

key_tuples = [
    ("1", str(ONE)), ("2", str(ONE)), ("3", str(ONE)),
    ("4", str(ONE)), ("5", str(ONE)), ("6", str(ONE)),
    ("7", str(ONE)), ("8", str(ONE)), ("9", str(ONE)),
]

message_handler = MessageHandler(Filters.text, catch_message)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
