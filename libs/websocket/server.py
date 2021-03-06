import sys
import json
from utils.db.auth_methods import token_auth
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from utils.watcher import getPrice


class BroadcastServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))
        if 'key' not in request.params.keys():
            self._closeConnection(abort=True)
        else:
            key = request.params['key'][0]
            if key[-1] != ':' and key[0] != ':' and len(key.split(':'))==2:
                access_token, email = key.split(':')
                req = { 'email': email, 'access_token': access_token }
                succeed, result = token_auth(req)
                if not succeed:
                    self._closeConnection(abort=True)
                else:
                    self.factory.register(self)
            else:
                self._closeConnection(abort=True)

    def onOpen(self):
        print("WS Connection Open, waiting for Authentication ... ")

    def onMessage(self, payload, isBinary):
        # self.sendMessage(payload, isBinary)
        if not isBinary:
            msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            print msg
            # self.factory.broadcast(msg)
        else:
            print("Binary message received: {} bytes".format(len(payload)))

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tick()

    def tick(self):
        RESULT = {
            "markets": {
            }
        }
        # self.tickcount += 1
        yunbi_btc_sc = str(format(getPrice('yunbi', 'sc/cny') / getPrice('yunbi', 'btc/cny'), '.10f'))
        polon_btc_sc = format(getPrice('poloniex', 'btc/sc'), '.10f')
        yunbi_btc_cny = format(getPrice('yunbi', 'btc/cny'), '.10f')
        polon_btc_usd = format(getPrice('poloniex', 'usdt/btc'), '.10f')
        RESULT['markets']['yunbi_btc/sc'] = yunbi_btc_sc
        RESULT['markets']['polon_btc/sc'] = polon_btc_sc
        RESULT['markets']['yunbi_btc/cny'] = yunbi_btc_cny
        RESULT['markets']['polon_btc/usd'] = polon_btc_usd

        self.broadcast(json.dumps(RESULT))
        reactor.callLater(1, self.tick)

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))


class BroadcastPreparedServerFactory(BroadcastServerFactory):

    """
    Functionally same as above, but optimized broadcast using
    prepareMessage and sendPreparedMessage.
    """

    def broadcast(self, msg):
        print("broadcasting prepared message '{}' ..".format(msg))
        preparedMsg = self.prepareMessage(msg)
        for c in self.clients:
            c.sendPreparedMessage(preparedMsg)
            print("prepared message sent to {}".format(c.peer))


# if __name__ == '__main__':

#     log.startLogging(sys.stdout)

#     ServerFactory = BroadcastServerFactory
#     # ServerFactory = BroadcastPreparedServerFactory

#     factory = ServerFactory(u"ws://127.0.0.1:9000")
#     factory.protocol = BroadcastServerProtocol
#     listenWS(factory)

#     webdir = File(".")
#     web = Site(webdir)
#     reactor.listenTCP(8080, web)

#     reactor.run()