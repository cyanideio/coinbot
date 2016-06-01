import requests

class BaseTicker(object):
    """docstring for ClassName"""
    def __init__(self, HOST):
        super(BaseTicker, self).__init__()
        self.HOST = HOST

    def get_info(self, name):
        url = "%s%s.json" % (self.HOST, name)
        r = requests.get(url)
        return r.json()

    def init(self):
        markets = self.get_info('markets')
        self.get_info('tickers')
        print markets
