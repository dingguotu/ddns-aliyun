#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv4

class IPCN(ipv4.IPV4):
    def get_ip(ipDict):
        ipcnReq = ipv4.request.Request(url=f'https://ip.cn/api/index?ip=&type=0', headers=ipv4.IPV4.Headers, method='GET')
        ipcn = ipv4.json.loads(ipv4.request.urlopen(ipcnReq).read().decode('utf-8'))['ip']
        ipDict[ipcn] = ipDict.setdefault(ipcn, 0) + 1