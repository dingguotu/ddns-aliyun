#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv4

class IpApi(ipv4.IPV4):
    def get_ip(ipDict):
        ipapi = ipv4.json.loads(ipv4.request.urlopen('http://ip-api.com/json').read().decode('utf-8'))['query']
        ipDict[ipapi] = ipDict.setdefault(ipapi, 0) + 1