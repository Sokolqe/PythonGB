from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram import Update
from config import TOKEN


def get_ccgame_start(update: Update, context: CallbackContext):
    after_command = context.args
    update.message.reply_text('Начнем игру...')
    print(after_command)


def catch_message(update: Update):
    message = update.message.text
    if 'прив' in message.lower:
        update.message.reply_text(f'Добрейший вечерочек, смотри что умею!')

    else:
        update.message.reply_text(f'Перейдем сразу к делу...')


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

ccgame_handler = CommandHandler('cross-circles')
message_handler = MessageHandler(filters=, catch_message)

dispatcher.add_handler(ccgame_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()