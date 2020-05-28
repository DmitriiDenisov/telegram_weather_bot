import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from utils.constants import d_symbols, URL_ONE_CALL, PARAMS_ONE_CALL
from utils.queue import rem_notif, set_notif


def call_notifications_menu(update, context):
    """
    Returns inline keyboard to user
    :param update:
    :param context:
    :param jobQueue:
    :return:
    """
    inline_keyboard = context.user_data['inline_keyboard']
    for notif in context.user_data['notifs']:
        inline_keyboard[notif.hour // 4][notif.hour % 4].text = '✅' + inline_keyboard[notif.hour // 4][
                                                                          notif.hour % 4].text[1:]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(f'I will send you daily weather info based on chosen time', reply_markup=reply_markup)


def notifications_menu(update, context):
    """
    Gets response from user and either removes notification from jobQueue or sets new notification
    Replies to user with updated inline keyboard
    :param update:
    :param context:
    :param jobQueue:
    :param callback_daily:
    :return:
    """
    query = update.callback_query
    query.answer()
    chat_id = update.effective_chat.id
    inline_keyboard = context.user_data['inline_keyboard']
    num = int(query.data)
    new_s = d_symbols[inline_keyboard[num // 4][num % 4].text[0]]
    if new_s == '🛑':
        rem_notif(chat_id, f"{num}:00".zfill(2), context)
    else:
        set_notif(chat_id, f"{num}:00".zfill(2), context, notif_func_forecast)

    inline_keyboard[num // 4][num % 4] = InlineKeyboardButton(f'{new_s}{f"{num}:00".zfill(2)}',
                                                              callback_data=num)

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    query.edit_message_text(
        text="I will send you daily weather info based on chosen time",
        reply_markup=reply_markup
    )


def notif_func_forecast(context: CallbackContext):
    chat_id = context.job.context['chat_id']
    lat = context.job.context['lat']
    lon = context.job.context['lon']

    PARAMS_ONE_CALL['lat'] = lat
    PARAMS_ONE_CALL['lon'] = lon

    response = requests.request("GET", URL_ONE_CALL, params=PARAMS_ONE_CALL)
    modes = ['temp', 'feels_like']

    response = response.json()
    ans = 'Hey! Here is your forecast for today: \n'
    for mode in modes:
        if mode == 'temp':
            ans += f'Temp: {response["daily"][0][mode]["day"]}\n'
        else:
            ans += f'Feels like: {response["daily"][0][mode]["day"]}\n'
    ans += f'Humidity: {response["daily"][0]["humidity"]}\n'
    context.bot.send_message(chat_id=chat_id, text=ans)
