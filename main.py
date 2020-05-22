import os

from WeatherBot import WeatherBot

f = open('token.txt', 'r')
token = f.read(100)


def main():
    WeatherBot(token=token)


if __name__ == '__main__':
    main()
