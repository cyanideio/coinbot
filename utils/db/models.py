#!/usr/bin/python
# -*- coding: utf-8 -*-
from settings import DB, USERDB
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase(DB)
user_db = SqliteExtDatabase(USERDB)

##################
# For User DB
##################
class User(Model):
    is_super_user = BooleanField()
    is_staff = BooleanField()
    username = CharField()
    password = CharField()
    access_token = CharField()
    class Meta:
        database = user_db

##################
# For Exchange DB
##################
class BaseModel(Model):
    coinType = CharField()       # Type of the Virtual Coin
    price =  DoubleField()       # Unit Price of the trade
    volume = DoubleField()       # Volume of the Trade
    timestamp = DateTimeField(   # Now
        default = datetime.datetime.now) 
    class Meta:
        database = db

class CoinCapTransaction(BaseModel):
    percent = DoubleField()      # Price Change in Percentage
    supply = DoubleField()       # Supply
    cap24hrChange = FloatField() # Cap Change in 24 Hours
    vWAP = DoubleField()         # Volume weighted price based on 24hours of trading data on all exchanges
    vWAPBTC = DoubleField()      # vWap by BTC
    marketCap = DoubleField()    # Market Capitalization, total value of the coin

class CoinCapBTCTrans(CoinCapTransaction):
    pass

class CoinCapAltTrans(CoinCapTransaction):
    delta = DoubleField()        # DeltaPrice
    cap24hrChangePercent = FloatField()
    capPercent = FloatField()

class YunbiTrans(BaseModel):
    sell = DoubleField()
    buy = DoubleField()
    high = DoubleField()
    low = DoubleField()

class PoloniexTrans(BaseModel):
    percent = DoubleField()      # Price Change in Percentage
    lowestAsk = DoubleField()
    highestBid = DoubleField()
    quoteVolume = DoubleField()
    mkt24hrHigh = DoubleField()
    mkt24hrLow = DoubleField()