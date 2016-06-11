#!/usr/bin/python
# -*- coding: utf-8 -*-
from settings import DB, USERDB
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.db_url import connect
import datetime
import os

db = PostgresqlExtDatabase(DB, user='coin_watcher', register_hstore=False)
db = connect(os.environ.get('DATABASE'))
user_db = SqliteExtDatabase(USERDB)

##################
# For User DB
##################
class User(Model):
    salt = CharField()
    is_super_user = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    username = CharField(unique=True)
    password = CharField()
    access_token = CharField(unique=True, null=True)
    created = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField(null=True)
    last_ip = CharField(null=True)
    class Meta:
        database = user_db

##################
# For Exchange DB
##################
class BaseModel(Model):
    coinType = CharField()       # Type of the Virtual Coin
    price =  FloatField()       # Unit Price of the trade
    volume = FloatField()       # Volume of the Trade
    timestamp = DateTimeField(   # Now
        default=datetime.datetime.now) 
    class Meta:
        database = db

class CoinCapTransaction(BaseModel):
    percent = FloatField()      # Price Change in Percentage
    supply = FloatField()       # Supply
    cap24hrChange = FloatField() # Cap Change in 24 Hours
    vWAP = FloatField()         # Volume weighted price based on 24hours of trading data on all exchanges
    vWAPBTC = FloatField()      # vWap by BTC
    marketCap = FloatField()    # Market Capitalization, total value of the coin

class CoinCapBTCTrans(CoinCapTransaction):
    pass

class CoinCapAltTrans(CoinCapTransaction):
    delta = FloatField()        # DeltaPrice
    cap24hrChangePercent = FloatField()
    capPercent = FloatField()

class YunbiTrans(BaseModel):
    sell = FloatField()
    buy = FloatField()
    high = FloatField()
    low = FloatField()

class PoloniexTrans(BaseModel):
    percent = FloatField()      # Price Change in Percentage
    lowestAsk = FloatField()
    highestBid = FloatField()
    quoteVolume = FloatField()
    mkt24hrHigh = FloatField()
    mkt24hrLow = FloatField()