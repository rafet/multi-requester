import requests
import urllib3
import Proxy
import random
from useragentManager import useragentManager as um
from concurrent.futures import ThreadPoolExecutor
import threading
import concurrent


class proxyManager:
    def __init__(self, use_proxy=True):
        self.use_proxy = use_proxy
        self.proxies = []
        self.fetchProxiesFromAPI()
        self.proxies_copy = self.proxies.copy()
        self.useragent_manager = um()
        self.timeout = 1

    def fetchProxiesFromAPI(self):
        url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=2000&ssl=yes'
        data = requests.get(url).text.split('\r\n')
        for i in data:
            if i:
                x = i.split(':')
                self.proxies.append(Proxy.Proxy(x[0], x[1]))

    def proxyCount(self):
        return len(self.proxies)

    def renewProxies(self, copy=True):
        if copy:
            self.proxies = self.proxies_copy.copy()
        else:
            self.fetchProxiesFromAPI()

    def getRandomProxy(self):
        random_proxy = random.choice(self.proxies)
        while not random_proxy:
            random_proxy = random.choice(self.proxies)
        return random_proxy

    def get(self, url):
        while True:
            try:
                headers = self.useragent_manager.getRandomHeaders()
                if self.use_proxy:
                    rand_proxy = self.getRandomProxy()
                    proxies = {"http": str(rand_proxy), "https": str(rand_proxy)}
                    res = requests.get(url,
                                       timeout=self.timeout,
                                       proxies=proxies,
                                       headers=headers)
                else:
                    res = requests.get(url,
                                       timeout=self.timeout,
                                       headers=headers)

                if res.status_code in [200, 404]:
                    return res
            except:
                pass

    def get_many(self, urls):
        tasks = []
        obj = {}
        results = []
        executor = ThreadPoolExecutor(max_workers=100)
        for url in urls:
            future = executor.submit(self.get, url)
            obj[future] = url
            tasks.append(future)

        for task in concurrent.futures.as_completed(tasks):
            yield task.result(), obj[task]
