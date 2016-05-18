#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
from colorama import init
from socketIO_client import SocketIO
from libs.namespaces import CoinNamespace

HOST = 'http://socket.coincap.io'
PORT = 80
init()
socketIO = SocketIO(HOST, PORT, CoinNamespace)
socketIO.wait()
