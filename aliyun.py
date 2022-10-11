#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request, parse
import hmac, datetime, uuid, base64
import json, os, logging
import logger


Headers = {
    'Accept': 'text/json',
    'Content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

CommonParams = {
    'Format':'json',
    'SignatureMethod': 'HMAC-SHA1',
    'SignatureVersion': '1.0',
    'Timestamp': datetime.datetime.utcnow().isoformat(),
    'Version': '2015-01-09',
}

class Aliyun():
    _access_key_id = ''
    _access_key_secret = ''

    def __init__(self, access_key_id, access_key_secret):
        global _access_key_id
        global _access_key_secret
        _access_key_id = access_key_id
        _access_key_secret = access_key_secret


    def check_domain_exists(self, domain_name):
        CommonParams['AccessKeyId'] = _access_key_id
        CommonParams['Action'] = 'DescribeDomainInfo'
        CommonParams['DomainName'] = domain_name
        try:
            self._get_response_data(CommonParams)
            return True
        except Exception as e:
            logging.error(e)
            return False


    def create_domain(self, domain_name):
        CommonParams['AccessKeyId'] = _access_key_id
        CommonParams['Action'] = 'AddDomain'
        CommonParams['DomainName'] = domain_name
        try:
            self._get_response_data(CommonParams)
        except Exception as e:
            logging.error(e)
            pass


    def get_record_value(self, domain_name, sub_domain, record_type):
        CommonParams['AccessKeyId'] = _access_key_id
        CommonParams['Action'] = 'DescribeDomainRecords'
        CommonParams['DomainName'] = domain_name
        try:
            data = self._get_response_data(CommonParams)
            records = data['DomainRecords']['Record']
            for record in records:
                if record['Type'] == record_type and record['RR'] == sub_domain:
                    logging.info(f"Sub_Domain [{sub_domain}] hostIP is {record['Value']}")
                    return record['Value']
            return 0
        except Exception as e:
            logging.error(e)
            return 0


    def get_record_id(self, domain_name, sub_domain, record_type):
        CommonParams['AccessKeyId'] = _access_key_id
        CommonParams['Action'] = 'DescribeDomainRecords'
        CommonParams['DomainName'] = domain_name
        try:
            data = self._get_response_data(CommonParams)
            records = data['DomainRecords']['Record']
            for record in records:
                if record['Type'] == record_type and record['RR'] == sub_domain:
                    return record['RecordId']
            return 0
        except Exception as e:
            logging.error(e)
            return 0


    def add_record(self, domain_name, sub_domain, record_type, localIP):
        CommonParams['AccessKeyId'] = _access_key_id
        CommonParams['Action'] = 'AddDomainRecord'
        CommonParams['DomainName'] = domain_name
        CommonParams['RR'] = sub_domain
        CommonParams['Type'] = record_type
        CommonParams['Value'] = localIP

        try:
            data = self._get_response_data(CommonParams)
            return data['RecordId']
        except Exception as e:
            logging.error(e)
            return 0


    def record_ddns(self, record_id, sub_domain, record_type, localIP):
        CommonParams['AccessKeyId'] = _access_key_id
        CommonParams['Action'] = 'UpdateDomainRecord'
        CommonParams['RR'] = sub_domain
        CommonParams['RecordId'] = record_id
        CommonParams['Type'] = record_type
        CommonParams['Value'] = localIP

        try:
            data = self._get_response_data(CommonParams)
            return data['RecordId']
        except Exception as e:
            logging.error(e)
            return 0


    def _get_response_data(self, params):
        CommonParams['SignatureNonce'] = uuid.uuid1()
        params = self._sort_dict(params)

        params['Signature'] = self._sign(params)
        req = request.Request(url=f'https://alidns.aliyuncs.com/?{parse.urlencode(params)}', headers=Headers, method='GET')
        response = request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))


    def _sort_dict(self, dic):
        result = {}
        for key in sorted(dic.keys()):
            result[key] = dic[key]
        return result


    def _sign(self, params):
        stringToSign = 'GET&%2F&' + parse.quote(parse.urlencode(params))
        h = hmac.new((_access_key_secret+'&').encode('utf-8'), stringToSign.encode('utf-8'), digestmod='sha1').digest()
        signature = base64.b64encode(h).decode('utf-8')
        return signature
