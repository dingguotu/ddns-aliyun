#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ipv6
import logging
import logger

class IPV6(object):
    Headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
        }

    def __init_subclass__(cls):  # 一旦创建这个类的子类，就会触发此方法
        super().__init_subclass__()

    def get_ip(ipDict):
        pass
    
    def get_local_ip(self):
        if IPV6.__subclasses__().__len__() == 0:
            logging.info("No functions are registered for ipv6")
            return

        ipDict = dict()
        for chi in IPV6.__subclasses__():
            try:
                chi.get_ip(ipDict)
            except Exception as e:
                logging.error(e)
                pass
        
        if ipDict.__len__() == 0:
            logging.info("Local machine has not ipv6.")
            return
        LocalIP = sorted(ipDict.items(), key=lambda d:d[1], reverse = True)[0][0]
        return LocalIP