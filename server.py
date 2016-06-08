#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, g, request, jsonify, abort
from re import match
from utils.db.auth_methods import register as do_register

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

RESPONSE = { "body" : "", "meta" : R['success'] }

regis_req = {
    "email": r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
    "password": r"[A-Za-z0-9\._-]"
}

login_req = {
    "email": r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
    "password": r"[A-Za-z0-9\._-]"
}

def handlePOSTRequest(req, handler):
    r = RESPONSE
    if request.method == 'POST':
        req_dict = request.get_json()
        if req_dict.keys() == req.keys():
            for key in req_dict.keys():
                if not match(req[key], req_dict[key]):
                    r['meta'] = R['fail']
                    r['body'] = ERRORS['invalid_param'] % key
                    return jsonify(**r)
            return handler(req_dict, r)
    abort(401) 

def register_handler(request_dict, r):
    email = request_dict['email']
    password = request_dict['password']
    if do_register(email, password):
        return jsonify(**r)


def login_handler(request_dict, r):
    print request_dict
    return jsonify(**r)

@app.route("/register", methods=['POST'])
def register():
    return handlePOSTRequest(regis_req, register_handler)

@app.route("/login", methods=['POST'])
def login():
    return handlePOSTRequest(login_req, login_handler)