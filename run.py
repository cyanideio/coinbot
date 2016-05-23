#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
from colorama import init
from socketIO_client import SocketIO
from settings import COIN_CAP_HOST, COIN_CAP_PORT
from libs.namespaces import CoinNamespace

# Initialize Color Library
init()

coin_socketIO = SocketIO(COIN_CAP_HOST, COIN_CAP_PORT, CoinNamespace)
coin_socketIO.wait()
