#import logging
#logging.getLogger('requests').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
import sys
from colorama import init as color_init
from socketIO_client import SocketIO
from settings import COIN_CAP_HOST, COIN_CAP_PORT, YB_HOST

from libs.trading_centers.coincap.namespaces import CoinNamespace
from libs.trading_centers.yunbi.ticker import BaseTicker
from libs.trading_centers.poloniex.subscriber import BaseSubscriber, SubscribeTrollbox, SubscribeTicker

from utils.db.models import db, CoinCapBTCTrans, CoinCapAltTrans, YunbiTrans, PoloniexTrans

from multiprocessing import Process, Queue

# Initialize Color Library
color_init()
db.connect()

# Initialize DataBase
try:
    db.create_tables([PoloniexTrans])
    db.create_tables([YunbiTrans])
    db.create_tables([CoinCapBTCTrans, CoinCapAltTrans])
except Exception:
	print "[USING EXISITNG TABLE]"

market = sys.argv[1]

####################
# Market Input
####################

# t1 = threading.Thread(target=BaseSubscriber.run, args=(SubscribeTicker))
# t1.start()
# t1.join()

# Poloniex
def runPoloniex():
	# BaseSubscriber.run(SubscribeTrollbox)
	BaseSubscriber.run(SubscribeTicker)

# CoinCap
def runCoinCap():
	coin_socketIO = SocketIO(COIN_CAP_HOST, COIN_CAP_PORT, CoinNamespace)
	coin_socketIO.wait()

# Yunbi
def runYunbi():
	yb = BaseTicker(YB_HOST)
	yb.init()
	yb.tick()

if market == 'yunbi':
	runYunbi()

if market == 'poloniex':
	runPoloniex()

if market == 'coincap':
	runCoinCap()

print "Invalide Arg"