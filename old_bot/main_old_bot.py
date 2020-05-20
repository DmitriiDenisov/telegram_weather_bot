from old_bot.old_bot_py import AutoSelfieBot

import os, sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)
f = open(os.path.join(PROJECT_PATH, 'token.txt'), 'r')
token = f.read(100)

REQUEST_KWARGS = {
    'proxy_url': 'socks5://80.211.195.141:1488',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'kurwaproxy',
        'password': 'x555abr',
    }
}


def main():
    AutoSelfieBot(token=token, request_kwargs=REQUEST_KWARGS, model_name='resnet_weights.17--0.95.hdf5.model')


if __name__ == '__main__':
    main()
