from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, CallbackQueryHandler, ConversationHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE = range(9)


def start(update, _):
    """Вызывается по команде `/start`."""
    # Получаем пользователя, который запустил команду `/start`
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    # Создаем `InlineKeyboard`, где каждая кнопка имеет
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка,
    # в свою очередь, является списком `[[...]]`
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ], [
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            InlineKeyboardButton("5", callback_data=str(FIVE)),
            InlineKeyboardButton("6", callback_data=str(SIX)),
        ], [
            InlineKeyboardButton("7", callback_data=str(SEVEN)),
            InlineKeyboardButton("8", callback_data=str(EIGHT)),
            InlineKeyboardButton("9", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
    update.message.reply_text(
        text="Выберите клетку", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
    return FIRST


def start_over(update, _):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    # На запросы обратного вызова необходимо ответить,
    # даже если уведомление для пользователя не требуется.
    # В противном случае у некоторых клиентов могут возникнуть проблемы.
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ], [
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            InlineKeyboardButton("5", callback_data=str(FIVE)),
            InlineKeyboardButton("6", callback_data=str(SIX)),
        ], [
            InlineKeyboardButton("7", callback_data=str(SEVEN)),
            InlineKeyboardButton("8", callback_data=str(EIGHT)),
            InlineKeyboardButton("9", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   # Отредактируем сообщение, вызвавшее обратный вызов.
   # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text="Выберите клетку", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
    return FIRST


def one(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    choice_index = query.data
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("X", callback_data=str(None)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ], [
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            InlineKeyboardButton("5", callback_data=str(FIVE)),
            InlineKeyboardButton("6", callback_data=str(SIX)),
        ], [
            InlineKeyboardButton("7", callback_data=str(SEVEN)),
            InlineKeyboardButton("8", callback_data=str(EIGHT)),
            InlineKeyboardButton("9", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Выберите клетку", reply_markup=reply_markup
    )
    return FIRST


def two(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    print(query.data)
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("X", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ], [
            InlineKeyboardButton("4", callback_data=str(FOUR)),
            InlineKeyboardButton("5", callback_data=str(FIVE)),
            InlineKeyboardButton("6", callback_data=str(SIX)),
        ], [
            InlineKeyboardButton("7", callback_data=str(SEVEN)),
            InlineKeyboardButton("8", callback_data=str(EIGHT)),
            InlineKeyboardButton("9", callback_data=str(NINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Второй CallbackQueryHandler", reply_markup=reply_markup
    )
    return FIRST


def three(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да, сделаем это снова!", callback_data=str(ONE)),
            InlineKeyboardButton("Нет, с меня хватит ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Третий CallbackQueryHandler. Начать сначала?", reply_markup=reply_markup
    )
    # Переход в состояние разговора `SECOND`
    return SECOND


def four(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Четвертый CallbackQueryHandler, выберите маршрут", reply_markup=reply_markup
    )
    return FIRST


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


updater = Updater('5841761129:AAGWzrUYTccSd75_v837_qqiblVAsTQKm4w')
dispatcher = updater.dispatcher

# Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
# Используем параметр `pattern` для передачи `CallbackQueries` с
# определенным шаблоном данных соответствующим обработчикам
# ^ - означает "начало строки"
# $ - означает "конец строки"
# Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={ # словарь состояний разговора, возвращаемых callback функциями
        FIRST: [
            CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
            CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
            CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
            CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            CallbackQueryHandler(one, pattern='^' + str(FIVE) + '$'),
            CallbackQueryHandler(two, pattern='^' + str(SIX) + '$'),
            CallbackQueryHandler(three, pattern='^' + str(SEVEN) + '$'),
            CallbackQueryHandler(four, pattern='^' + str(EIGHT) + '$'),
            CallbackQueryHandler(four, pattern='^' + str(NINE) + '$'),
        ],
        SECOND: [
            CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
            CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
        ],
    },
    fallbacks=[CommandHandler('start', start)],
    )
message_handler = MessageHandler(Filters.text, catch_message)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()