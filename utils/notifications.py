import requests
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from utils.constants import URL_ONE_CALL, PARAMS_ONE_CALL, D_SYMBOLS
from utils.queue import rem_notif, set_notif
from utils.utils import get_minutes_keyboard


def call_notifications_menu(update, context):
    """
    Returns inline keyboard to user
    :param update:
    :param context:
    :param jobQueue:
    :return:
    """
    inline_keyboard = context.user_data['inline_keyboard']
    for hour in context.user_data['notifs'].keys():
        hour_int = int(hour)
        inline_keyboard[hour_int // 4][hour_int % 4].text = '✅' + inline_keyboard[hour_int // 4][
                                                                      hour_int % 4].text[1:]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text(f'I will send you daily weather info based on chosen time', reply_markup=reply_markup)
    return 0


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
    t = f"{query.data.zfill(2)}:00"

    minutes_keyboard = get_minutes_keyboard(num)

    for idx in context.user_data['notifs'][query.data]:
        minutes_keyboard[idx // 4][idx % 4].text = '✅' + minutes_keyboard[idx // 4][idx % 4].text[1:]

    reply_markup = InlineKeyboardMarkup(minutes_keyboard)
    query.edit_message_text(
        text="I will send you daily weather info based on chosen time",
        reply_markup=reply_markup
    )
    return 1


def test_func(update, context):
    query = update.callback_query
    minutes = query.message.reply_markup.inline_keyboard
    query.answer()
    chat_id = update.effective_chat.id
    data_str = query.data

    if data_str == '-1':
        inline_keyboard = context.user_data['inline_keyboard']
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        query.edit_message_text(f'I will send you daily weather info based on chosen time', reply_markup=reply_markup)
        return 0
    idx = int(data_str)

    prev = minutes[idx // 4][idx % 4].text
    hour = str(int(prev[1:3]))  # берем ток час
    new_s = D_SYMBOLS[prev[0]]

    if new_s == '🛑':
        context.user_data['notifs'][hour].remove(idx)
        if not context.user_data['notifs'][hour]:
            # Remove from main_keyboard
            hour_int = int(hour)
            temp = context.user_data['inline_keyboard'][hour_int // 4][hour_int % 4]
            context.user_data['inline_keyboard'][hour_int // 4][hour_int % 4].text = new_s + temp.text[1:]
        # rem_notif(chat_id, t, context)
    else:
        hour_int = int(hour)
        temp = context.user_data['inline_keyboard'][hour_int // 4][hour_int % 4]
        context.user_data['inline_keyboard'][hour_int // 4][hour_int % 4].text = new_s + temp.text[1:]
        # set_notif(chat_id, t, context, notif_func_forecast, hour)
        context.user_data['notifs'][hour].add(idx)  # внимание! хранятся индексы!!!

    minutes[idx // 4][idx % 4] = InlineKeyboardButton(new_s + prev[1:], callback_data=data_str)

    reply_markup = InlineKeyboardMarkup(minutes)
    query.edit_message_text(
        text="I will send you daily weather info based on chosen time",
        reply_markup=reply_markup
    )
    return 1


def notif_func_forecast(context: CallbackContext):
    chat_id = context.job.context['chat_id']
    lat = context.job.context['lat']
    lon = context.job.context['lon']

    PARAMS_ONE_CALL['lat'] = lat
    PARAMS_ONE_CALL['lon'] = lon
    PARAMS_ONE_CALL['exclude'] = 'minutely,hourly'

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
