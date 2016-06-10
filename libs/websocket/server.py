from autobahn.twisted.websocket import WebSocketServerProtocol
from utils.db.auth_methods import token_auth

class SyncServerProtocol(WebSocketServerProtocol):

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
                self._closeConnection(abort=True)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: {}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))