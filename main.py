
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import *
import argparse

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
    update.message.reply_text('Hello, World!')

def stop(bot, update):
    pass

def main():
    parser = argparse.ArgumentParser(description='A Telegram task manager bot.')
    parser.add_argument('token', metavar='TOKEN', help='The Bot Token to work with the Telegram Bot API')

    args = parser.parse_args()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(args.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("about", about))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stop", stop))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
