import requests
import time
from utils.db.models import YunbiTrans

TICKER_KEYS = ['sell', 'buy', 'last', 'vol', 'high', 'low']
DEPED = ['notecny']

class BaseTicker(object):
    """docstring for ClassName"""
    def __init__(self, HOST):
        super(BaseTicker, self).__init__()
        self.HOST = HOST

    def get_info(self, name):
        url = "%s%s.json" % (self.HOST, name)
        try:
                r = requests.get(url)
                return r.json()
        except Exception:
                return False

    def init(self):
        self.markets = [[str(m['id']),str(m['name'])] for m in self.get_info('markets')]

    def tick(self, market='all'):
        tick = self.get_info('tickers')
        if tick:
            for market in self.markets:
                if market not in DEPED:
                    try:
                        info = tick[market[0]]['ticker']
                    except Exception:
                        continue
                    YunbiTrans.create(
                        coinType = market[1].lower(),
                        price = info['last'],
                        volume = info['vol'], 
                        sell = info['sell'],
                        buy = info['buy'],
                        high = info['high'],
                        low = info['low']
                    )
                #    print self.markets
                #    print "YunBi Error"
        else:
            print "Network Error"
        time.sleep(1)

    def tickforever(self):
        while True:
            self.tick()
