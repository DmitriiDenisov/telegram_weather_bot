from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

REQUEST_KWARGS = {
    'proxy_url': 'socks5://80.211.195.141:1488',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'kurwaproxy',
        'password': 'x555abr',
    }
}


def start(update, context):
    # update.message.reply_text(context)
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


def start_func(update, context):
    first_name = update.effective_user.first_name
    update.message.reply_text('Hi {}!'.format(first_name))
    # self.all_users[update.message.chat_id] = {'first_name': first_name}

    custom_keyboard = [['English'], ['Russian']]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Custom Keyboard Test",
                             reply_markup=reply_markup)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


import os, sys

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_PATH)
f = open(os.path.join(PROJECT_PATH, 'token.txt'), 'r')
token = f.read(100)

updater = Updater(token, use_context=True, request_kwargs=REQUEST_KWARGS)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start_func))
dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

# dp.add_handler(MessageHandler(Filters.text, start_func))

updater.start_polling()
updater.idle()
