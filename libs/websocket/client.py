from autobahn.twisted.websocket import WebSocketClientProtocol

class SyncClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        # self.sendMessage(u"Connected".encode('utf8'))
        print "Connected !"

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
    	print("WebSocket connection closed: {}".format(reason))

