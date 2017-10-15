
from telegram import ParseMode
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
    message += '/new name repeat hour day/month/year\n\n'
    message += 'where _repeat_ is how many days are between each repetition, '
    message += '_year_ is optional, _month_ is optional, and _day_ is '
    message += 'optional if month is omitted (but the slashes aren\'t)'
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def addTask(bot, update, args):
    global chats
    tchat = update.message.chat
    ident = str(tchat.id)
    if not ident in chats:
        title = get_chatname(tchat)
        chat = Chat(tchat.id, title)
    else:
        chat = chats[ident]
    try:
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
    except ValueError as ve:
        update.message.reply_text('A task already exists under this name')
    except Exception as e:
        update.message.reply_text('Wrong format. Send /help for more details')
    chats[ident] = chat

#    except:
#        update.message.reply_text('Wrong format')

def getTasks(bot, update, time):
    global chats
    tchat = update.message.chat
    ident = str(tchat.id)
    if not ident in chats:
        title = get_chatname(tchat)
        chat = Chat(tchat.id, title)
    else:
        chat = chats[ident]

    dateNow = datetime.now()
    if time is 'today':
        tasks = chat.getTasksRange()
    elif time == 'all':
        tasks = chat.getTasks()
    elif time == 'week':
        now = datetime.now()
        week = now + timedelta(7)
        tasks = chat.getTasksRange(now.day, now.month, now.year, week.day, week.month, week.year)
    elif time == 'month':
        now = datetime.now()
        _, delta = monthrange(now.year, now.month)
        month = now + timedelta(delta)
        tasks = chat.getTasksRange(now.day, now.month, now.year, month.day, month.month, month.year)
    elif time == 'fortnight':
        now = datetime.now()
        fort = now + timedelta(14)
        tasks = chat.getTasksRange(now.day, now.month, now.year, fort.day, fort.month, fort.year)

    if len(tasks) == 0:
        update.message.reply_text('There are no tasks under this criteria.')
    else:
        for t in tasks:
            update.message.reply_text(str(t))
    chats[ident] = chat

def getTasksToday(bot,update):
    update.message.reply_text('Today\'s tasks:')
    getTasks(bot, update, 'today')

def getTasksAll(bot,update):
    update.message.reply_text('All tasks:')
    getTasks(bot, update, 'all')

def getTasksWeek(bot, update):
    update.message.reply_text('Tasks on a week from now:')
    getTasks(bot, update, 'week')

def getTasksMonth(bot, update):
    update.message.reply_text('Tasks on a month from now:')
    getTasks(bot, update, 'month')

def getTasksFort(bot, update):
    update.message.reply_text('Tasks on 2 weeks from now:')
    getTasks(bot, update, 'fortnight')

def stop(bot, update):
    pass

def deleteTask(bot, update, args):
    global chats
    tchat = update.message.chat
    ident = str(tchat.id)
    if not ident in chats:
        title = get_chatname(tchat)
        chat = Chat(tchat.id, title)
    else:
        chat = chats[ident]

    for name in args:
        if chat.deleteTask(name):
            update.message.reply_text('Task ' + name + ' deleted succesfully.')
        else:
            update.message.reply_text('There is no task with name ' + name + '.')
    chats[ident] = chat

def checkTask(bot, update, args):
    global chats
    tchat = update.message.chat
    ident = str(tchat.id)
    if not ident in chats:
        title = get_chatname(tchat)
        chat = Chat(tchat.id, title)
    else:
        chat = chats[ident]

    for name in args:
        if chat.markDone(name):
            update.message.reply_text('Task ' + name + ' checked out.')
        else:
            update.message.reply_text('There is no task with name ' + name + '.')
    chats[ident] = chat

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
    dp.add_handler(CommandHandler("all", getTasksAll))
    dp.add_handler(CommandHandler("month", getTasksMonth))
    dp.add_handler(CommandHandler("week", getTasksWeek))
    dp.add_handler(CommandHandler("fortnight", getTasksFort))
    dp.add_handler(CommandHandler("new", addTask, pass_args=True))
    dp.add_handler(CommandHandler("delete", deleteTask, pass_args=True))
    dp.add_handler(CommandHandler("check", checkTask, pass_args=True))
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
