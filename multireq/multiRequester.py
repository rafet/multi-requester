import requests
import random
from concurrent.futures import ThreadPoolExecutor
import threading
import concurrent


class useragentManager:
    def __init__(self):
        with open('multireq/useragents.txt', 'r') as f:
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


class Proxy:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.working = True
        self.used = 0

    def __str__(self):
        return f"{self.ip}:{self.port}"

    def setWorking(self, working):
        self.working = working

    def incUsed(self):
        self.used += 1


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
        if copy:
            self.proxies = self.proxies_copy.copy()
        else:
            self.fetchProxiesFromAPI()

    def getRandomProxy(self):
        random_proxy = random.choice(self.proxies)
        while not random_proxy:
            random_proxy = random.choice(self.proxies)
        return random_proxy


class multiRequester:
    def __init__(self, use_proxy=False, max_workers=100):
        self.use_proxy = use_proxy
        self.proxy_manager = proxyManager()
        self.useragent_manager = useragentManager()
        self.timeout = 3
        self.max_workers = max_workers

    def get(self, url):
        while True:
            try:
                headers = self.useragent_manager.getRandomHeaders()
                if self.use_proxy:
                    rand_proxy = self.proxy_manager.getRandomProxy()
                    proxies = {
                        "http": str(rand_proxy),
                        "https": str(rand_proxy)
                    }
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
            except Exception as e:
                pass

    def get_many(self, urls):
        tasks = []
        executor = ThreadPoolExecutor(max_workers=self.max_workers)
        for url in urls:
            future = executor.submit(self.get, url)
            tasks.append(future)
        for task in concurrent.futures.as_completed(tasks):
            yield task.result()