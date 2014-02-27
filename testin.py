#!/bin/env python
# coding=utf8
import requests
import time
import json
import logging
from config import mcfg_url, apikey, secret_key, email, password

logging.getLogger().setLevel(logging.DEBUG)
timestamp = str(int(time.time()*1000))

def get_dispatch_list():
    payload = {'apikey':apikey,
                'secret_key':secret_key,
                'op':'Dispatch.list',
                'timestamp':timestamp}
    r = requests.post(mcfg_url, data = json.dumps(payload))
    if r.status_code == requests.codes.ok:
        return r.json()

def get_external_url():
    dispatch = get_dispatch_list()['data']['dispatches'][0]
    return "http://%s:%s" % (dispatch['externalIp'], dispatch['externalPort'])

def login(email=email, password=password):
    external_url = get_external_url()
    login_url = '%s/sso/user.action' % external_url
    payload = {'op':'Login.login',
                'apikey':apikey,
                'timestamp':timestamp,
                'email':email,
                'pwd':password}
    r = requests.post(login_url, data = json.dumps(payload))
    if r.status_code == requests.codes.ok:
        #{u'code': 0, u'data': {u'sid': u'E0DF927C4c8d27b4205fe74ec5f57c3c36d024ee'}, u'op': u'Login.login'}
        return r.json()    

def get_sid():
    return login()['data']['sid']

def get_devices():
    url = "%s/deviceunit/cfg.action" % get_external_url()
    payload = {'op':'Model.getSpecimens',
                'apikey':apikey,
                'timestamp':timestamp,
                'sid':get_sid(),
                'syspfName':'android',
                'cloud':'adapt.testin'}
    logging.info(payload)
    r = requests.post(url, data = json.dumps(payload))
    if r.status_code == requests.codes.ok:
        return r.json()                




if __name__ == '__main__':
