#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request
import socket 
import json
import os
import re
import aliyun

global LocalIP
global HostIP
global Login_Token
global Domain_Id
global Access_Key_Id
global Access_Key_Secret

def init_domain(domain):
    domain_exists = aliyun.check_domain_exists(Access_Key_Id, Access_Key_Secret, domain['name'])
    if domain_exists == False:
        aliyun.create_domain(Access_Key_Id, Access_Key_Secret, domain['name'])


def ddns(domain):
    for sub_domain in domain['sub_domains']:
        record_value = aliyun.get_record_value(Access_Key_Id, Access_Key_Secret, domain['name'], sub_domain)
        if record_value == 0:
            aliyun.add_record(Access_Key_Id, Access_Key_Secret, domain['name'], sub_domain, LocalIP)
        elif record_value != LocalIP:
            print(f"Begin update [{sub_domain}.{domain['name']}].")
            record_id = aliyun.get_record_id(Access_Key_Id, Access_Key_Secret, domain['name'], sub_domain)
            aliyun.record_ddns(Access_Key_Id, Access_Key_Secret, record_id, sub_domain, LocalIP)

    
def get_ip():
    global LocalIP
    #sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
    #LocalIP = sock.recv(16).decode('utf-8')
    url = str(request.urlopen(r'http://txt.go.sohu.com/ip/soip').read())
    ip = re.findall(r'\d+.\d+.\d+.\d+', url)
    LocalIP = ip[0]
    print(f'LocalIP is {LocalIP}')
    #sock.close()

    
if __name__ == '__main__':
    global Login_Token
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.json"), "r"))

    Access_Key_Id = conf['access_key']
    Access_Key_Secret = conf['access_secret']
    Domains = conf['domains']
    
    try:
        get_ip()
        for domain in Domains:
            init_domain(domain)
            ddns(domain)
    except Exception as e:
        print(e)
        pass
