import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent
from multireq.Proxy import Proxy
from multireq.proxyManager import proxyManager
from multireq.useragentManager import useragentManager


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
                return res
            except Exception as e:
                if rand_proxy:
                    rand_proxy.setWorking(False)

    def get_many(self, urls):
        tasks = []
        executor = ThreadPoolExecutor(max_workers=self.max_workers)
        for url in urls:
            future = executor.submit(self.get, url)
            tasks.append(future)
        for task in concurrent.futures.as_completed(tasks):
            yield task.result()
