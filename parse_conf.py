#! /usr/bin/env python
#coding=utf-8

'''     
1. process ini file
[a]
aa_1=1
aa_2=2
visit: get_value('a.aa_1')
@author gulijing@baidu.com
''' 
import sys
import os
import os.path
import traceback
import ConfigParser

class INI_Conf:    
    def __init__(self, config_file_path):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        self._cf = cf

    def get_values(self, key):
        values = {}

        s = self._cf.sections()
        keyArr = key.split('.')
        o = self._cf.options(keyArr[0])
        items = self._cf.items(keyArr[0])
        for item in items:
            values[item[0]] = item[1]

        return values

    def get_value(self, key):
        values = self.get_values(key)
        keyArr = key.split('.')
        return values[keyArr[1]]

        
if __name__ == '__main__':
    ini_conf = INI_Conf('./driver.conf')   
    res = ini_conf.get_values('qrw')
    #print res
    res = ini_conf.get_value('qrw.req_json')
    #print res
