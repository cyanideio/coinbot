#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.db.models import User
import datetime
import hashlib, uuid


def register(username, password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    User.create(username=username, password=hashed_password, salt=salt)
    return True