#!/usr/bin/python
# -*- coding: utf-8 -*-
import peewee
import datetime
import redis
import hashlib, uuid
from playhouse.shortcuts import model_to_dict
from utils.db.models import User

r = redis.StrictRedis(host='localhost', port=6379, db=0)

USER_FILTER = ['password', 'salt', 'id']

def gen_access_token():
    return str(uuid.uuid1()).replace('-','_')

def apply_filter(data_dict, filter):
    for key in filter:
        del data_dict[key]

def export_data(data, f):
    data = model_to_dict(data)
    apply_filter(data, f)
    return data

def token_auth(req):
    username = req['email']
    access_token = req['access_token']
    try:
        user = User.get(User.username == username)
    except Exception, e:
        return False, "User Doesn't Exist"
    if user.access_token == access_token:
        data = export_data(user, USER_FILTER)
        return True, data
    else:
        return False, "Invalid Access Token"

def register(req):
    username = req['email']
    password = req['password']
    ip = req['ip']
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    access_token = gen_access_token()
    try:
        user = User.create(username=username, password=hashed_password, salt=salt, last_login=datetime.datetime.now(), last_ip=ip, access_token=access_token)
    except peewee.IntegrityError, e:
        return False, e
    r.set(str(user.id), access_token)
    data = export_data(user, USER_FILTER)
    return True, data

def login(req):
    username = req['email']
    password = req['password']
    access_token = gen_access_token()
    try:
        user = User.get(User.username == username)
    except Exception, e:
        return False, "User Doesn't Exist"
    user.access_token = access_token
    user.save()
    r.set(str(user.id), access_token)
    salt = user.salt
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    if hashed_password != user.password:
        return False, "Mismatched Username & Password"
    data = export_data(user, USER_FILTER)
    user.last_login = datetime.datetime.now()
    user.last_ip = req['ip']
    user.save()
    return True, data
