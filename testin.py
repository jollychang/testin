#!/bin/env python
# coding=utf8
import requests
import time
import json
from config import mcfg_url, apikey, secret_key




def get_dispatch_list():
    timestamp = str(int(time.time()*1000))
    payload = {'apikey':apikey,
                'secret_key':secret_key,
                'op':'Dispatch.list',
                'timestamp':timestamp}
    r = requests.post(mcfg_url, data = json.dumps(payload))
    if r.status_code == requests.codes.ok:
        return r.text


if __name__ == '__main__':
    print get_dispatch_list()