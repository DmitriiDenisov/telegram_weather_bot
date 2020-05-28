import datetime

import pytz
import requests
from geopy.geocoders import Nominatim

from utils.constants import TOKENS

geolocator = Nominatim(user_agent='myapplication')
location = geolocator.geocode("Dubai")
lat = location.raw['lat']
lon = location.raw['lon']
print(location.raw)

url = "https://api.openweathermap.org/data/2.5/onecall"
querystring = {"lat": lat, "lon": lon, "appid": TOKENS['one_call'],
               "units": 'metric', "exclude": 'minutely,hourly'}
response = requests.request("GET", url, params=querystring)
print(response.url)

dict = response.json()
print(dict)

q = datetime.time(10, 58, 00, 000000, pytz.timezone(dict['timezone']))
q = datetime.time(10, 58, 00, 000000, pytz.timezone('Asia/Dubai'))
print(q)
print(q.tzinfo)
