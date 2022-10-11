#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv6

class Ident(ipv6.IPV6):
    def get_ip(ipDict):
        ident = ipv6.request.urlopen('https://v6.ident.me').read().decode('utf-8')
        ipDict[ident] = ipDict.setdefault(ident, 0) + 1