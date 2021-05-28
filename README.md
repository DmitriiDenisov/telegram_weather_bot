# telegram_weather_bot

## Bot:
@weather_fcst_bot

### Direct link:
https://t.me/weather_fcst_bot

## How to Run:

1. Clone repo 

2. `pip install -r requirements.txt` (everything was developed under python 3.7.7 )

3. Go to Bot Father and get your Token for Telegram bot

4. Go to `https://console.cloud.google.com/apis/credentials` and find your Google API key

5. Go to `https://home.openweathermap.org/api_keys` and find your token for Open Weather provider

6. In root directory create file `tokens.json`, put there json with four fileds: telegram, one_call, google, curr_weather (token for one_call and curr_weather will be equal). In format like here: 
```
{
  "telegram": "ABC", // Telegram Bot Token
  "one_call": "ABC", // Token from https://openweathermap.org/. It does not provide current weather that's why need separate for current weather
  "curr_weather": "ABC", // token for weather
  "google": "ABC" // token for Google location identifier 
}
```

7. `python3 WeatherBot.py`

## Screenshots:

<p align="center">
  <img src="https://i.ibb.co/kGH6d6k/Screen-Shot-2020-06-02-at-10-56-28-PM.png" width="800" alt="accessibility text">
</p>

<p align="center">
  <img src="https://i.ibb.co/9twLTsw/Screen-Shot-2020-06-02-at-10-57-02-PM.png" width="800" alt="accessibility text">
</p>

<p align="center">
  <img src="https://i.ibb.co/DLT5D0p/Screen-Shot-2020-06-02-at-10-57-13-PM.png" width="800" alt="accessibility text">
</p>

<p align="center">
  <img src="https://i.ibb.co/8Mt6jKG/Screen-Shot-2020-06-02-at-10-57-27-PM.png" width="800" alt="accessibility text">
</p>

<p align="center">
  <img src="https://i.ibb.co/wWgMPHY/Screen-Shot-2020-06-02-at-10-57-41-PM.png" width="800" alt="accessibility text">
</p>
