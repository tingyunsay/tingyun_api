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


#网易云歌单评论


#网易云歌曲评论
class QQ_Song(object):
    def __init__(self):
        self.headers = { 
            'Referer': 'http://y.qq.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            }

        #抓取详细评论，通过外面传参控制翻页
        self.data= {'notice': '0', 
                    'cmd': '6', 
                    'platform': 'yqq.json', 
                    #外部控制
                    'pagesize': '', 
                    #外部控制
                    'pagenum': '', 
                    'format': 'json', 
                    'biztype': '1', 
                    'outCharset': 'GB2312', 
                    'cid': '205360772', 
                    'hostUin': '0', 
                    'needNewCode': '0', 
                    'g_tk': '5381', 
                    'domain': 'qq.com', 
                    'loginUin': '0', 
                    'inCharset': 'utf8', 
                    'reqtype': '2', 
                    'needmusiccrit': '0', 
                    'ct': '24', 
                    'cv': '101010', 
                    #关键参数,传递songid进入
                    'topid': ''
                    }

    #需要前端传递一个mid,访问页面直接获取songid
    def get_songid(self,url):
        res = PyQuery(self.fetch(url))
        return (res('.js_more').attr['data-id']) 
	
        pass

    def fetch(self,url,headers={}):
        if not type(headers) == dict:
            #不符合条件不添加
            return requests.get(url,headers=self.headers).content
        for k,v in headers.items():
            if self.headers.get(k):
                continue
            self.headers[k] = v
        return requests.get(url,headers=self.headers).content

    def post(self,url,headers={},data={}):
        if not type(headers) == dict:
            #不符合条件不添加
            return requests.post(url,headers=self.headers,data=data)
        for k,v in headers.items():
            if self.headers.get(k):
                continue
            self.headers[k] = v
        return requests.post(url,headers=self.headers,data=data)
        

    def get_comment(self,url,offset,limit):
        songid = self.get_songid(url)
        if songid:
            self.data["topid"] = songid
            self.data["pagenum"] = offset
            self.data["pagesize"] = limit
            res = self.post("https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg",headers=self.headers,data=self.data)
            #print(res.json())
            return res.json() 
        else:
            return None
        
if __name__ == "__main__":
    #url = "https://y.qq.com/n/yqq/song/{mid}.html".format(mid="002E3MtF0IAMMY")
    #print(QQ_Song().get_songid(url))
    #print(QQ_Song().get_comment(url,"1","10"))

    pass



