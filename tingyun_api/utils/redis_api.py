#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re,time
from pyquery import PyQuery
import codecs
from Crypto.Cipher import AES
import base64
import requests
import datetime
import json
import logging
import redis
from config import *

class Redis_Api(object):
    def __init__(self):
        self.r = redis.Redis(redis_conf['ip'], redis_conf['port'], db=0)

    #获取map
    def hget_redis(self, ckey):
        r_con = self.r.hgetall(ckey)
        return r_con

    #添加封禁uid
    def hset_redis(self, ckey , k , v):
        r_con = self.r.hset(ckey , k , v)
        return r_con

    #移除封禁uid
    def hdel_redis(self, ckey , k ):
        r_con = self.r.hdel(ckey , k )
        return r_con

if __name__ == "__main__":


    pass

