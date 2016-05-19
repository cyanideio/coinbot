from socketIO_client import BaseNamespace
from settings import WATCH_LIST, PARAMS, ALT_TEMPLATE, BTC_TEMPLATE
from colorama import Fore, Back, Style

class CoinNamespace(BaseNamespace):

    def on_connect(self):
        print('[CONNECTED]')

    def on_global(self, *args):
        self.parse_args(args, 'global')

    def on_trades(self, *args):
        self.parse_args(args, 'trade')

    def parse_args(self, args, msg_type):
        if msg_type == 'trade':
            msg = args[0]['message']
            detail = msg['msg']
            coin = msg['coin']
            self.parse_coin(detail, coin)

    def parse_coin(self, coin_msg, coin):
        if coin in WATCH_LIST:
            perc = float(coin_msg['perc'])
            vwapData = coin_msg['vwapData']
            cap24hrChange = float(coin_msg['cap24hrChange'])
            supply = int(coin_msg['supply'])
            vwapDataBTC = float(coin_msg['vwapDataBTC'])
            price = coin_msg['price']
            volume = float(coin_msg['volume'])
            usdVolume = float(coin_msg['usdVolume'])
            mktcap = float(coin_msg['mktcap'])
            TEMPLATE = BTC_TEMPLATE
            SET =  (Fore.RED, coin, Fore.BLUE, price, Fore.GREEN, vwapData)
            if coin != 'BTC':
                delta = float(coin_msg['delta'])
                cap24hrChangePercent = float(coin_msg['cap24hrChangePercent'])
                capPercent = float(coin_msg['capPercent'])
                TEMPLATE = ALT_TEMPLATE
                SET = (Fore.RED, coin, capPercent, Fore.BLUE, price, Fore.GREEN, vwapData, Fore.YELLOW, delta)
            print TEMPLATE % SET
