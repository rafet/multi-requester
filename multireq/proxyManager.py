import requests
import random
from multireq.Proxy import Proxy


class proxyManager:
    def __init__(self):
        self.proxies = []
        self.fetchProxiesFromAPI()
        self.proxies_copy = self.proxies.copy()

    def fetchProxiesFromAPI(self):
        url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=2000&ssl=yes'
        data = requests.get(url).text.split('\r\n')
        for i in data:
            if i:
                x = i.split(':')
                self.proxies.append(Proxy(x[0], x[1]))

    def proxyCount(self):
        return len(self.proxies)

    def renewProxies(self, copy=True):
        self.proxies = []
        if copy:
            self.proxies = self.proxies_copy.copy()
        else:
            self.fetchProxiesFromAPI()

    def getRandomProxy(self):
        random_proxy = random.choice(self.proxies)
        while not random_proxy or random_proxy.working == False:
            random_proxy = random.choice(self.proxies)
        return random_proxy
