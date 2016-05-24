#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
from colorama import init as color_init
from socketIO_client import SocketIO
from settings import COIN_CAP_HOST, COIN_CAP_PORT
from libs.namespaces import CoinNamespace
from utils.db.models import db, CoinCapBTCTrans, CoinCapAltTrans

# Initialize Color Library
color_init()
db.connect()
db.create_tables([CoinCapBTCTrans, CoinCapAltTrans])

coin_socketIO = SocketIO(COIN_CAP_HOST, COIN_CAP_PORT, CoinNamespace)
coin_socketIO.wait()
