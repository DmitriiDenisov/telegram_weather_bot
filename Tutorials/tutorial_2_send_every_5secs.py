# Send message to a particular user every 5 secs

import telegram.ext
from telegram.ext import Updater
import os, sys
import time

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
f = open(os.path.join(PROJECT_PATH, 'token.txt'), 'r')
token = f.read(100)

updater = Updater(token, use_context=True)
jobQueue = updater.job_queue


def callback_minute(context: telegram.ext.CallbackContext):
    # 304640198 - id of user, you can know your id with @userinfobot bot in Telegram
    # bot.send_message(chat_id=304640198, text='One message every 5 secs')
    context.bot.send_message(chat_id=304640198, text='One message every minute')


job_minute = jobQueue.run_repeating(callback_minute, interval=5, first=0)

updater.start_polling()

# job_minute.enabled = False  # Temporarily disable this job
# job_minute.schedule_removal()  # Remove this job completely
# Note: schedule_removal does not immediately remove the job from the queue.
# Instead, it is marked for removal and will be removed as soon as its current interval is over
# (it will not run again after being marked for removal)
# job_minute.enabled = True # Enables back

# updater.idle()

jobQueue.stop()  # we can stop job
time.sleep(10)
jobQueue.start()  # and start again

# updater.stop()  # or we can stop polling
# updater.start_polling()  # and then start again
