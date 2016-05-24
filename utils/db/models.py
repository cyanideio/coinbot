from settings import DB
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase(DB)

class BaseModel(Model):
    class Meta:
        database = db

class Transaction(BaseModel):
	coin_type = CharField()      # Type of the Virtual Coin
	market = CharField()	     # Market on which the coin is traded
	price =  DoubleField()       # Unit Price of the trade
	volume = DoubleField()       # Volume of the Trade
