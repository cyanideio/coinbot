#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
from colorama import init as color_init
from socketIO_client import SocketIO
from settings import COIN_CAP_HOST, COIN_CAP_PORT, YB_HOST

from libs.trading_centers.coincap.namespaces import CoinNamespace
from libs.trading_centers.yunbi.ticker import BaseTicker

from utils.db.models import db, CoinCapBTCTrans, CoinCapAltTrans

# Initialize Color Library
#color_init()
#db.connect()
#
#try:
#	db.create_tables([CoinCapBTCTrans, CoinCapAltTrans])
#except Exception:
#	print "[USING EXISITNG TABLE]"
#
#coin_socketIO = SocketIO(COIN_CAP_HOST, COIN_CAP_PORT, CoinNamespace)
#coin_socketIO.wait()

yb = BaseTicker(YB_HOST)
yb.init()
yb.tick()
