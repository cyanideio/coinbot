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
from utils.db.models import user_db, User

from utils.watcher import getPrice

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory
from libs.websocket.server import BroadcastServerProtocol, BroadcastServerFactory
from libs.websocket.client import SyncClientProtocol

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

try:
    do = sys.argv[1]
    target = sys.argv[2]
except Exception:
    print "Error"

def init_user_db():
    user_db.connect()

    # Initialize DataBase
    try:
        db.create_tables([User])
    except Exception:
        print "[USING EXISITNG TABLE]"

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
    yb.tickforever()

# Watch
def watch():
    print 'yunbi btc/sc', format(getPrice('yunbi', 'sc/cny') / getPrice('yunbi', 'btc/cny'), '.10f')
    print 'polon btc/sc', format(getPrice('poloniex', 'btc/sc'), '.10f')
    print 'yunbi btc/cny', format(getPrice('yunbi', 'btc/cny'), '.10f')
    print 'polon btc/usd', format(getPrice('poloniex', 'usdt/btc'), '.10f')

def start_ws_server(url):
    factory = BroadcastServerFactory(url)
    factory.protocol = BroadcastServerProtocol
    reactor.listenTCP(9000, factory)
    reactor.run()

def start_ws_client(url):
    factory = WebSocketClientFactory(url)
    factory.protocol = SyncClientProtocol
    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()

if do == 'initialize':
    if target == 'user_db':
        init_user_db()

if do == 'sync':
    if target == 'yunbi':
        runYunbi()
    if target == 'poloniex':
        runPoloniex()
    if target == 'coincap':
        runCoinCap()

if do == 'start':
    if target == 'watch':
        watch()
    if target == 'wsserver':
        try:
            url = sys.argv[3]
            start_ws_server(url)
        except Exception:
            print "error"
    if target == 'wsclient':
        try:
            url = sys.argv[3]
            start_ws_client(url)
        except Exception:
            print "error"
