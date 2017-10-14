
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import *
from chat import *
import argparse
import logging

chats = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def get_chatname(chat):
    if chat.title is not None:
        return chat.title
    elif chat.first_name is not None:
        if chat.last_name is not None:
            return chat.first_name + " " + chat.last_name
        else:
            return chat.first_name
    else:
        return ""
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
    update.message.reply_text('Hello there!')

def help(bot, update):
    message = 'The task must be stated like this:\n'
    message += '/new repeat hour day/month/year\n\n'
    message += 'where __repeat__ is how many days are between each repetition, '
    message += '__year__ is optional, __month__ is optional, and __day__ is '
    message += 'optional if month is omitted (but the slashes aren\'t)'
    update.message.reply_text(message)

def addTask(bot, update, args):
    global chats
    tchat = update.message.chat
    ident = str(tchat.id)
    if not ident in chats:
        title = get_chatname(tchat)
        chat = Chat(tchat.id, title)
    else:
        chat = chats[ident]

    # Args: name repeat hour day/month/year
    if len(args) > 2:
        args[2] = args[2].strip('h')
        if len(args) > 3:
            date = args[3].split('/')
            for i in range(len(date)):
                if date[i] == '':
                    date[i] = '0'
            t = chat.addTask(args[0],int(args[1]),int(args[2]),int(date[0]),int(date[1]),int(date[2]))
        else:
            t = chat.addTask(args[0],int(args[1]),int(args[2]))
    elif len(args) > 1:
        t = chat.addTask(args[0],int(args[1]))
    else:
        t = chat.addTask(args[0])
    update.message.reply_text('Task ' + t.name + ' added')
    chats[ident] = chat

#    except:
#        update.message.reply_text('Wrong format')

def getTasksToday(bot,update):
    global chats
    tchat = update.message.chat
    ident = str(tchat.id)
    if not ident in chats:
        title = get_chatname(tchat)
        chat = Chat(tchat.id, title)
    else:
        chat = chats[ident]
    update.message.reply_text('Today\'s tasks:')
    dateNow = datetime.now()
    tasks = chat.getTasks()
    for task in tasks:
        update.message.reply_text(t)
    chats[ident] = chat

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
    dp.add_handler(CommandHandler("today", getTasksToday))
    dp.add_handler(CommandHandler("new", addTask, pass_args=True))
    #dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("help", help))
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
