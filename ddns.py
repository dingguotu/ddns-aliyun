#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request
import json, os, logging
import aliyun
import logger

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
            logging.info(f"Begin update [{sub_domain}.{domain['name']}].")
            record_id = aliyun.get_record_id(Access_Key_Id, Access_Key_Secret, domain['name'], sub_domain)
            aliyun.record_ddns(Access_Key_Id, Access_Key_Secret, record_id, sub_domain, LocalIP)

    
def get_ip():
    global LocalIP
    try:
        response = request.urlopen(r'http://ip.taobao.com/outGetIpInfo?ip=myip&accessKey=alibaba-inc').read().decode('utf-8')
        data = json.loads(response)
        LocalIP = data['data']['ip']
        logging.info(f'LocalIP is {LocalIP}')
        pass
    except Exception as e:
        logging.error('Get [LocalIP] Failed')
        pass
    

    
if __name__ == '__main__':
    global Login_Token

    logger.setup_logging()
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
        logging.error(e)
        pass
