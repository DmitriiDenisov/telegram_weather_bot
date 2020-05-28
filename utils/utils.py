from datetime import datetime

import pytz
import requests
from telegram import InlineKeyboardButton

from utils.constants import REPLY_MARKUP, TOKENS

url = " https://api.openweathermap.org/data/2.5/weather"
querystring = \
    {
        "appid": TOKENS['curr_weather'],
        "units": 'metric'
    }

url_one_call = "https://api.openweathermap.org/data/2.5/onecall"
querystring_one_call = \
    {
        "appid": TOKENS['one_call'],
        "units": 'metric',
        "exclude": 'minutely,hourly'
    }


def get_forecast(num_days, chat_id, context):
    querystring_one_call['lat'] = context.user_data['lat']
    querystring_one_call['lon'] = context.user_data['lon']

    response = requests.request("GET", url_one_call, params=querystring_one_call)

    response = response.json()
    ans = ''
    for i in range(1, num_days + 1):
        day = datetime.utcfromtimestamp(response["daily"][i]["dt"]).strftime('%Y-%m-%d')
        ans += f'{day}: Temp: {response["daily"][i]["temp"]["day"]}, Feels like {response["daily"][i]["feels_like"]["day"]}\n'

    # ans += f'Humidity: {response["daily"][0]["humidity"]}\n'

    context.bot.send_message(chat_id=chat_id, text=ans)


def get_current_weather(update, city: str):
    querystring['q'] = city
    response = requests.request("GET", url, params=querystring)
    main = response.json()['main']
    update.message.reply_text(
        f'Current temp: {main["temp"]}, feels like: {main["feels_like"]}, humidity: {main["humidity"]}')


def get_current_weather_inline(city: str):
    querystring['q'] = city
    response = requests.request("GET", url, params=querystring)
    try:
        a = response.json()["main"]["temp"]
        # return 'HALLO!'
        return f'Current temp in {city}: {a}'
    except:
        return 'ERROR'


def get_inline_keyboard():
    inline_keyboard = [[] for x in range(6)]
    for k, i in enumerate(range(24)):
        inline_keyboard[k // 4].append(InlineKeyboardButton(f'🛑{f"{i}".zfill(2)}:00', callback_data=k))
    return inline_keyboard


def get_timezone(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/onecall"
    querystring = {"lat": lat, "lon": lon, "appid": TOKENS['one_call'],
                   "units": 'metric', "exclude": 'minutely,hourly,daily'}
    response = requests.request("GET", url, params=querystring)

    user_tz = pytz.timezone(response.json()['timezone'])
    return user_tz


def send_keyboard(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="You can choose an action:",
                             reply_markup=REPLY_MARKUP)
