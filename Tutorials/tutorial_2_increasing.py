import telegram.ext
from telegram.ext import Updater
import os, sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
f = open(os.path.join(PROJECT_PATH, 'token.txt'), 'r')
token = f.read(100)

u = Updater(token, use_context=True)
j = u.job_queue


def callback_increasing(context: telegram.ext.CallbackContext):
    job = context.job
    context.bot.send_message(chat_id=304640198,
                             text='Sending messages with increasing delay up to 10s, then stops.')
    job.interval += 1.0
    if job.interval > 10.0:
        job.schedule_removal()


j.run_repeating(callback_increasing, 1)

u.start_polling()
