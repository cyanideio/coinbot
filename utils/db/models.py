#!/usr/bin/python
# -*- coding: utf-8 -*-
from settings import DB
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase(DB)

class BaseModel(Model):
    class Meta:
        database = db

class CoinCapTransaction(BaseModel):
    market = CharField()         # Market on which the coin is traded
    supply = DoubleField()       # Supply
    cap24hrChange = FloatField() # Cap Change in 24 Hours
    price =  DoubleField()       # Unit Price of the trade
    volume = DoubleField()       # Volume of the Trade
    vWAP = DoubleField()         # Volume weighted price based on 24hours of trading data on all exchanges
    vWAPBTC = DoubleField()      # vWap by BTC
    marketCap = DoubleField()    # Market Capitalization, total value of the coin
    timestamp = DateTimeField(   # Now
        default = datetime.datetime.now) 

class CoinCapBTCTrans(CoinCapTransaction):
    pass

class CoinCapAltTrans(CoinCapTransaction):
    coinType = CharField()       # Type of the Virtual Coin
    delta = DoubleField()        # DeltaPrice
    percent = DoubleField()      # Price Change in Percentage
    cap24hrChangePercent = FloatField()
    capPercent = FloatField()