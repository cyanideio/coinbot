#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
HOST = 'http://socket.coincap.io'
PORT = 80
from socketIO_client import SocketIO
from libs.namespaces import CoinNamespace
socketIO = SocketIO(HOST, PORT, CoinNamespace)
socketIO.wait()
