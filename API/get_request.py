# https://openweathermap.org/city/292223
import requests

# headers = {
#    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
#    'x-rapidapi-key': ""
# }
from utils.constants import TOKENS

querystring = {"appid": TOKENS['curr_weather'],
               "units": 'metric'}

# url = "https://community-open-weather-map.p.rapidapi.com/forecast"
url = " https://api.openweathermap.org/data/2.5/weather"


def get_request(city: str):
    querystring['q'] = city
    response = requests.request("GET", url, params=querystring)
    # return response.json()['main']
    if response.status_code == 404:
        return False
    else:
        return True
