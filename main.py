import os

from WeatherBot import WeatherBot


f = open('tokens.json', 'r')
token = f.read(100)


def main():
    WeatherBot(token=token)


if __name__ == '__main__':
    main()
