import os
import random


class useragentManager:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f'{dir_path}/useragents.txt', 'r') as f:
            self.useragents = f.read().split('\n')

    def getRandomUseragent(self):
        return random.choice(self.useragents)

    def getRandomHeaders(self):
        headers = {
            "Connection": "close",
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': self.getRandomUseragent()
        }
        return headers
