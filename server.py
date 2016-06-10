#!/usr/bin/python
# -*- coding: utf-8 -*-
from re import match
from flask import Flask, render_template, g, request, jsonify, abort
from utils.db.auth_methods import register as do_register
from utils.db.auth_methods import login as do_login
app = Flask(__name__)

# Response Meta Dictionary
R = { 
    "fail": {
        "msg"  : "Request Failed",
        "code" : 0
    },
    "success": {
        "msg"  : "Request Succeed",
        "code" : 1
    }
}

ERRORS = { 'invalid_param': 'invalid %s' }
RESPONSE = { "data" : "", "meta" : R['success'] }
REG_IP = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
REG_EMAIL = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$" 
REG_PASSWORD = r"[A-Za-z0-9\._-]" 

regis_req = {
    "email": REG_EMAIL,
    "password": REG_PASSWORD,
    "ip": REG_IP
}

login_req = {
    "email": REG_EMAIL,
    "password": REG_PASSWORD,
    "ip": REG_IP
}

def handlePOSTRequest(req, handler, method):
    r = RESPONSE
    if request.method == 'POST' and request.is_json:
        req_dict = request.get_json()
        req_dict['ip'] = request.remote_addr
        if req_dict.keys() == req.keys():
            for key in req_dict.keys():
                if not match(req[key], req_dict[key]):
                    r['meta'] = R['fail']
                    r['data'] = ERRORS['invalid_param'] % key
                    return jsonify(**r)
            return handler(req_dict, r, method)
    abort(401) 

def request_handler(request_dict, r, method):
    succeed, result = method(request_dict)
    if not succeed:
        r['meta'] = R['fail']
        r['data'] = ERRORS['invalid_param'] % result
    else:
        r['meta'] = R['success']
        r['data'] = result
    return jsonify(**r)

@app.route("/register", methods=['POST'])
def register():
    return handlePOSTRequest(regis_req, request_handler, do_register)

@app.route("/login", methods=['POST'])
def login():
    return handlePOSTRequest(login_req, request_handler, do_login)