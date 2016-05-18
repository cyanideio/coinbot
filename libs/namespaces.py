from socketIO_client import BaseNamespace
import json
class CoinNamespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

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
	if coin == 'ETH':
            print coin_msg
