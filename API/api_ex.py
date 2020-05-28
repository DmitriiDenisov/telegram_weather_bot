# https://openweathermap.org/city/292223
import requests
import numpy as np
import pandas as pd

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': ""
}

url = "https://community-open-weather-map.p.rapidapi.com/forecast"
querystring = {"units": "metric", "mode": "",
               "q": "Dubai", "cnt": 10}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.url)

dict = response.json()
COLS = ['temp', 'feels_like', 'humidity', 'weather_main', 'weather_desc', 'dt_txt']
all_val = [[el['main']['temp'], el['main']['feels_like'], el['main']['humidity'], el['weather'][0]['main'],
            el['weather'][0]['description'], el['dt_txt']] for el in dict['list']]
df = pd.DataFrame(all_val, columns=COLS)
df['dt'] = pd.to_datetime(df.dt_txt, format='%Y-%m-%d %H:%M:%S')
df = df.drop('dt_txt', axis=1)
a = 3
print(f'timezone:{dict["city"]["timezone"]}')
# походу есть timesetoffset
