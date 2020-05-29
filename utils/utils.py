from datetime import datetime

import pytz
import requests
from telegram import InlineKeyboardButton

from utils.constants import URL_CURR_WEATHER, URL_ONE_CALL, PARAMS_ONE_CALL, PARAMS_CURR_WATHER, REPLY_MARKUP


def get_forecast(num_days, chat_id, context):
    PARAMS_ONE_CALL['lat'] = context.user_data['lat']
    PARAMS_ONE_CALL['lon'] = context.user_data['lon']
    PARAMS_ONE_CALL["exclude"] = 'minutely,hourly'
    response = requests.request("GET", URL_ONE_CALL, params=PARAMS_ONE_CALL)
    response = response.json()
    ans = ''
    for i in range(1, num_days + 1):
        day = datetime.utcfromtimestamp(response["daily"][i]["dt"]).strftime('%Y-%m-%d')
        ans += f'{day}: Temp: {response["daily"][i]["temp"]["day"]}, Feels like {response["daily"][i]["feels_like"]["day"]}\n'

    # ans += f'Humidity: {response["daily"][0]["humidity"]}\n'
    context.bot.send_message(chat_id=chat_id, text=ans)


def get_current_weather(update, user_data):
    # PARAMS_CURR_WATHER['q'] = city
    PARAMS_CURR_WATHER['lat'] = user_data['lat']
    PARAMS_CURR_WATHER['lon'] = user_data['lon']
    response = requests.request("GET", URL_CURR_WEATHER, params=PARAMS_CURR_WATHER)
    main = response.json()['main']
    update.message.reply_text(
        f'Current temp: {main["temp"]}, feels like: {main["feels_like"]}, humidity: {main["humidity"]}')


def get_current_weather_inline(city: str):
    PARAMS_CURR_WATHER['q'] = city
    response = requests.request("GET", URL_CURR_WEATHER, params=PARAMS_CURR_WATHER)
    try:
        a = response.json()["main"]["temp"]
        # return 'HALLO!'
        return f'Current temp in {city}: {a}'
    except:
        return 'ERROR'


def get_timezone(lat, lon):
    PARAMS_ONE_CALL['lat'] = lat
    PARAMS_ONE_CALL['lon'] = lon
    PARAMS_ONE_CALL['exclude'] = 'minutely,hourly,daily'
    response = requests.request("GET", URL_ONE_CALL, params=PARAMS_ONE_CALL)

    user_tz = pytz.timezone(response.json()['timezone'])
    return user_tz


def get_minutes_keyboard(num):
    minutes_keyboard = [[] for x in range(6)]
    minutes = [str(3 * el) for el in list(range(20))]
    hour = f"{num}".zfill(2)
    for k in range(20):
        minutes_keyboard[k // 4].append(InlineKeyboardButton(f"🛑{hour}:{minutes[k].zfill(2)}", callback_data=k))
    minutes_keyboard[-1].append(InlineKeyboardButton(f'Back', callback_data=-1))
    return minutes_keyboard


def send_keyboard(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="You can choose an action:",
                             reply_markup=REPLY_MARKUP)
