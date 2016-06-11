# import logging, logging.handlers
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from HTMLParser import HTMLParser

from settings import POLONIEX_HOST, POLONIEX_REALM
from utils.db.models import PoloniexTrans

# logging.basicConfig(format='%(message)s' ,level=logging.DEBUG)
# trolllogger = logging.getLogger()
# trolllogger.addHandler(logging.handlers.RotatingFileHandler('TrollBox.log', maxBytes=10**9, backupCount=5)) # makes 1Gb log files, 5 files max

class SubscribeTrollbox(ApplicationSession):
	@inlineCallbacks
	def onJoin(self, details):
		h = HTMLParser()
		def onTroll(*args):
			try:
				logging.info('%s:%s:: (%s)-%s- %s' % (args[0].upper(), str(args[1]), str(args[4]), args[2], h.unescape(args[3]) ))
			except IndexError: # Sometimes its a banhammer!
				#(u'trollboxMessage', 6943543, u'Banhammer', u'OldManKidd banned for 0 minutes by OldManKidd.')
				logging.info('%s:%s:: -%s- %s' % (args[0].upper(), str(args[1]), args[2], h.unescape(args[3]) ))
		yield self.subscribe(onTroll, 'trollbox')

class SubscribeTicker(ApplicationSession):
	@inlineCallbacks
	def onJoin(self, details):
		h = HTMLParser()
		def onTick(*args):
			print args
			PoloniexTrans.create(
				coinType = args[0].lower().replace('_', '/'),
				price = float(args[1]),
				lowestAsk = float(args[2]),
				highestBid = float(args[3]),
				percent = float(args[4]),
				volume = float(args[5]),
				quoteVolume = float(args[6]),
				mkt24hrHigh = float(args[8]),
				mkt24hrLow = float(args[9])
			)
			# logging.info(args)
		yield self.subscribe(onTick, 'ticker')

BaseSubscriber = ApplicationRunner(POLONIEX_HOST, POLONIEX_REALM)