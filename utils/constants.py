from telegram import ReplyKeyboardMarkup

d_symbols = {'✅': '🛑', '🛑': '✅'}
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

main_keyboard = [[CURRENT_WEATHER], [FORECASTS_3_DAYS, FORECASTS_5_DAYS], [NOTIFICATIONS], [CHANGE_LOC]]
REPLY_MARKUP = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=False)
