from telegram.ext import Updater, MessageHandler, Filters

def handler(update, context):
    update.message.reply_text("You said: '{}'".format(update.message.text))


def main():
    updater = Updater('MY_SECRET_TELEGRAM_API_TOKEN_GOES_HERE')
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()