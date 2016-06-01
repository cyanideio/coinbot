import requests
import time
from utils.db.models import YunbiTick

TICKER_KEYS = ['sell', 'buy', 'last', 'vol', 'high', 'low']

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
        self.markets = [str(m['id']) for m in self.get_info('markets')]

    def tick(self, market='all'):
        tick = self.get_info('tickers')
        if tick:
            for market in self.markets:
                print tick[market]['ticker']
                .create(
                    coinType = coin,
                    percent = perc,
                    vWAP = vwapData,
                    vWAPBTC = vwapDataBTC,
                    marketCap = mktcap,
                    volume = volume,
                    price = price,
                    cap24hrChange = cap24hrChange,  
                    supply = supply,
                    delta = delta,
                    cap24hrChangePercent = cap24hrChangePercent,
                    capPercent = capPercent
                )
        else:
            print "Network Error"
	time.sleep(1)
	self.tick()
