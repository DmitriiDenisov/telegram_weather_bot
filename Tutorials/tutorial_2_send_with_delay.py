import telegram.ext
from telegram.ext import Updater
import os, sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
f = open(os.path.join(PROJECT_PATH, 'token.txt'), 'r')
token = f.read(100)

u = Updater(token, use_context=True)
j = u.job_queue


def callback_30(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=304640198,
                             text='A single message with 3s delay')

# delay of 3 seconds
j.run_once(callback_30, 3)

# j.run_once(callback_30, 30)

u.start_polling()
u.idle()