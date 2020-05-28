import telegram.ext
from telegram.ext import Updater
import os, sys
from telegram.ext import CommandHandler

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
f = open(os.path.join(PROJECT_PATH, 'tokens.json'), 'r')
token = f.read(100)

u = Updater(token, use_context=True)
j = u.job_queue


def callback_alarm(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='BEEP')


def callback_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Setting a timer for 10 secs!')

    context.job_queue.run_once(callback_alarm, 10, context=update.message.chat_id)


timer_handler = CommandHandler('timer', callback_timer)
u.dispatcher.add_handler(timer_handler)

u.start_polling()
# u.idle()

# ##u.stop()
# # j.stop()
