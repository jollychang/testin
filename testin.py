#!/bin/env python
# coding=utf8
import requests
import time
import json
import logging
from config import mcfg_url, apikey, secret_key, email, password

logging.getLogger().setLevel(logging.DEBUG)
timestamp = str(int(time.time()*1000))
external_url, sid = None, None


def get_dispatch_list():
    payload = {'apikey':apikey,
                'secret_key':secret_key,
                'op':'Dispatch.list',
                'timestamp':timestamp}
    result = requests.post(mcfg_url, data = json.dumps(payload))
    if result.status_code == requests.codes.ok:
        return result.json()

def get_external_url():
    global external_url
    if not external_url:
        logging.debug("generate new external_url")
        dispatch = get_dispatch_list()['data']['dispatches'][0]
        external_url =  "http://%s:%s" % (dispatch['externalIp'], dispatch['externalPort'])
    return external_url

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
    global sid
    if not sid:
        logging.debug("not sid")
        sid = str(login()['data']['sid'])
    logging.debug("sid is : %s" % sid)
    return sid

def get_devices():
    #暂时只能拿到三个机型
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

def submit_test():
    url = "%s/realtest/nativeapp.action" % get_external_url()
    payload = {'op':'App.add',
                'apikey':apikey,
                'timestamp':timestamp,
                'sid':get_sid(),
                'syspfId':1,
                'testType':0,
                'secrecy':0,
                'cloud':'adapt.testin',
                'prodId':10004,
                'models':[{'modelId':'11',}],
                'packageUrl':'http://andariel.douban.com/d/com.douban.shuo'
                    }
    logging.info(payload)
    result = requests.post(url, data = json.dumps(payload))
    if result.status_code == requests.codes.ok:
        logging.debug(result.json())
        if result.json()['code'] == 0:
            adaptid = str(result.json()['data']['result'])
            logging.info("adaptId is: %s" % adaptid)
            return adaptid

def get_result(adaptid):
    url = "%s/realtest/nativeapp.action" % get_external_url()
    payload = {'op':'Report.overview',
                'apikey':apikey,
                'timestamp':timestamp,
                'sid':get_sid(),
                'adaptId':adaptid,
                }
    data = json.dumps(payload)
    result = requests.post(url, data = data)
    logging.info("url: %s" % url)
    logging.info(data)
    print result.status_code
    if result.status_code == requests.codes.ok:
        return result.json()



if __name__ == '__main__':
    # print get_devices()
    adaptid = submit_test()
    print "adaptid: %s" % adaptid
    print get_result(adaptid)