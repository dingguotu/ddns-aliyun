#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv4

class JsonIp(ipv4.IPV4):
    def get_ip(ipDict):
        jsonip = ipv4.json.loads(ipv4.request.urlopen('http://jsonip.com').read().decode('utf-8'))['ip']
        ipDict[jsonip] = ipDict.setdefault(jsonip, 0) + 1