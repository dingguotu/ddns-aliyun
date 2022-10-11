#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv4

class IPIFY(ipv4.IPV4):
    def get_ip(ipDict):
        ipify = ipv4.json.loads(ipv4.request.urlopen('https://api.ipify.org/?format=json').read().decode('utf-8'))['ip']
        ipDict[ipify] = ipDict.setdefault(ipify, 0) + 1