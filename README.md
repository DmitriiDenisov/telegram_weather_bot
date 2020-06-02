# telegram_weather_bot

## How to Run:

1. Clone repo 

2. `pip install -r requirements.txt` (everything was developed under python 3.7.7 )

3. Go to Bot Father and get your Token for Telegram bot

4. Go to `https://console.cloud.google.com/apis/credentials` and find your Google API key

5. Go to `https://home.openweathermap.org/api_keys` and find your token for Open Weather provider

6. In root directory create file `tokens.json`, put there json with four fileds: telegram, one_call, google, curr_weather (token for one_call and curr_weather will be equal)

7. `python3 WeatherBot.py`
