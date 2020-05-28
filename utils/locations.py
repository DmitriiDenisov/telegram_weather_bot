import requests
from geopy import Nominatim
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from API.get_request import get_request
from utils.constants import LOCATION, URL_GOOGLE_GEO, querystring_goog, TOKENS
from utils.notifications import notif_func_forecast
from utils.queue import update_queue
from utils.utils import get_timezone, send_keyboard
import reverse_geocoder as rg

geolocator = Nominatim(user_agent='myapplication')


def location_typing(update, context):
    user = update.message.from_user
    city = update.message.text
    chat_id = update.message.chat_id

    geolocator_ans = geolocator.geocode(city)
    if not geolocator_ans or not get_request(city):
        update.message.reply_text('Not found this city. Please type the name again:')
        return LOCATION

    location = geolocator_ans
    context.user_data['lat'] = location.raw['lat']
    context.user_data['lon'] = location.raw['lon']
    context.user_data['location'] = city
    context.user_data['timezone'] = get_timezone(location.raw['lat'], location.raw['lon'])

    # logger.info(f"Location of {user.first_name}: {city}")
    update_queue(chat_id, context, notif_func_forecast)  # in case 'change location'
    update.message.reply_text('Done!')
    send_keyboard(update, context)
    return ConversationHandler.END


def call_change_location(update, context):
    location_keyboard = KeyboardButton(text="📍 Send Location", request_location=True)
    custom_keyboard = [[location_keyboard], ['Cancel']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Write your new location or send your location",
                             reply_markup=reply_markup)
    return LOCATION


def location_lat_lon(update, context):
    lat = update.effective_message.effective_attachment.latitude
    lon = update.effective_message.effective_attachment.longitude

    city = 'Default'
    # Google geocoding API:
    querystring_goog['latlng'] = f'{lat},{lon}'
    querystring_goog['key'] = TOKENS['google']
    results = requests.request("GET", URL_GOOGLE_GEO, params=querystring_goog).json()['results']
    for el in results[0]['address_components']:
        if 'locality' in el['types'] and 'political' in el['types']:
            city = el['short_name']
            break
    # Offline solution: (source https://github.com/thampiman/reverse-geocoder)
    # coordinates = (lat, lon)
    # results = rg.search(coordinates, verbose=False)
    # city = results[0]['admin1']

    context.user_data['lat'] = lat
    context.user_data['lon'] = lon
    context.user_data['location'] = city
    context.user_data['timezone'] = get_timezone(lat, lon)
    # Update notifications:
    update_queue(update.message.chat_id, context, notif_func_forecast)
    update.message.reply_text(f'Done! Your new location: {city}')
    send_keyboard(update, context)
    return ConversationHandler.END


def cancel(update, context):
    send_keyboard(update, context)
    return ConversationHandler.END
