import random


class useragentManager:
    def __init__(self):
        with open('useragents.txt', 'r') as f:
            self.useragents = []
            for row in f:
                self.useragents.append(row)

    def getRandomUseragent(self):
        random_useragent = random.choice(self.useragents)
        while not random_useragent:
            random_useragent = random.choice(self.useragents)
        useragent = random_useragent.replace('\n', '')

    def getRandomHeaders(self):
        headers = {
            "Connection": "close",
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': self.getRandomUseragent()
        }
        return headers
