#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv4

class IP42(ipv4.IPV4):
    def get_ip(ipDict):
        ip42 = ipv4.request.urlopen('http://ip.42.pl/raw').read().decode('utf-8')
        ipDict[ip42] = ipDict.setdefault(ip42, 0) + 1