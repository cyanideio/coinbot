#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)

HOST = 'http://socket.coincap.io'
PORT = 80

from socketIO_client import SocketIO, BaseNamespace
class CoinNamespace(BaseNamespace):
    def on_connect(self):
        print('[Connected]')
    def on_global(self, *args):
        print('on_global', args)
    def on_trades(self, *args):
        print('on_trade', args)

socketIO = SocketIO(HOST, PORT, CoinNamespace)
socketIO.wait()
