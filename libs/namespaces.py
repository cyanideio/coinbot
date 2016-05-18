from socketIO_client import BaseNamespace
class CoinNamespace(BaseNamespace):
    def on_connect(self):
        print('[Connected]')
    def on_global(self, *args):
        print('on_global', args)
    def on_trades(self, *args):
        print('on_trade', args)
