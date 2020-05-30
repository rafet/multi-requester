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
