from settings import DB
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase(DB)

class BaseModel(Model):
    class Meta:
        database = db

class Transaction(BaseModel):
	coinType = CharField()       # Type of the Virtual Coin
	market = CharField()	     # Market on which the coin is traded
	price =  DoubleField()       # Unit Price of the trade
	volume = DoubleField()       # Volume of the Trade
	vWap = DoubleField()         # Volume weighted price based on 24hours of trading data on all exchanges
	vWapBTC = DoubleField()      # vWap by BTC
	marketCap = DoubleField()    # Market Capitalization, total value of the coin
	timestamp = DateTimeField(   # Now
		default = datetime.datetime.now) 