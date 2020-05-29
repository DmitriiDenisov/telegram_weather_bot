from telegram import ReplyKeyboardMarkup, InlineKeyboardButton
import json


def get_inline_main_keyboard():
    inline_keyboard = [[] for x in range(6)]
    for k, i in enumerate(range(24)):
        inline_keyboard[k // 4].append(InlineKeyboardButton(f'🛑{f"{i}".zfill(2)}:00', callback_data=k))
    return inline_keyboard




tokens_path = 'tokens.json'

with open(tokens_path) as json_file:
    TOKENS = json.load(json_file)

D_SYMBOLS = {'✅': '🛑', '🛑': '✅'}
CHOOSING = 0
LOCATION = 1
NOTIFICATION = 2
NEW_NOTIF = 3

CANCEL = 'Cancel'
CHANGE_LOC = '📍 Change location'
NOTIFICATIONS = '🛎️ Notifications'
CURRENT_WEATHER = '☀️ Current weather'
FORECASTS_3_DAYS = '☂️ Forecast 3 days'
FORECASTS_5_DAYS = '☂️ Forecast 5 days'

querystring_goog = {"language": 'en', "sensor": "false",
                    "units": 'metric', "exclude": 'minutely,hourly'}
PARAMS_ONE_CALL = \
    {
        "appid": TOKENS['one_call'],
        "units": 'metric',
        "exclude": 'minutely,hourly'
    }
PARAMS_CURR_WATHER = \
    {
        "appid": TOKENS['curr_weather'],
        "units": 'metric'
    }

URL_GOOGLE_GEO = "https://maps.googleapis.com/maps/api/geocode/json?"
URL_ONE_CALL = "https://api.openweathermap.org/data/2.5/onecall"
URL_CURR_WEATHER = " https://api.openweathermap.org/data/2.5/weather"

main_keyboard = [[CURRENT_WEATHER], [FORECASTS_3_DAYS, FORECASTS_5_DAYS], [NOTIFICATIONS], [CHANGE_LOC]]
REPLY_MARKUP = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=False)

INLINE_MAIN_KEYBOARD = get_inline_main_keyboard()
