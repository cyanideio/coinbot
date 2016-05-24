from settings import DB
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase(DB)

class BaseModel(Model):
    class Meta:
        database = db

class Transaction(BaseModel):
    username = CharField(unique=True)