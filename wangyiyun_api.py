#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re,time
import codecs
from Crypto.Cipher import AES
import base64
import requests
import datetime
import json


#网易云歌单评论


#网易云歌曲评论
class WYY_Song(object):
    def __init__(self):
        self.headers = { 
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            }

        #抓取详细评论，通过外面传参控制翻页
        self.first_param = {'rid':'', 'offset':'', 'total':'true', 'limit':'', 'csrf_token':''}
        self.second_param = "010001"
        self.third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.forth_param = "0CoJUm6Qyw8W8jud"

    def get_params(self,offset,limit):
        iv = "0102030405060708"
        first_key = self.forth_param
        second_key = 16 * 'F'
        self.first_param["offset"] = offset
        self.first_param["limit"] = limit
        h_encText = self.AES_encrypt(json.dumps(self.first_param), first_key, iv) 
        h_encText =self. AES_encrypt(h_encText, second_key, iv) 
        return h_encText

    def get_encSecKey(self):
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey

    def AES_encrypt(self,text, key, iv):
        pad = 16 - len(text) % 16
        try:
            text = text.decode()
        except Exception as e:
            pass
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv) 
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def get_json(self,url, params, encSecKey):
        data = { 
                        "params": params,
                        "encSecKey": encSecKey
                }
        response = requests.post(url, headers=self.headers, data=data)# ,proxies = {'http':'http://192.168.218.11:9112'})
        return response.content

    def get_comment(self,url,offset,limit):
        params = self.get_params(offset,limit)
        encSecKey = self.get_encSecKey()
        json_text = self.get_json(url, params, encSecKey)
        json_dict = json.loads(json_text)
        #print(json_dict)
        #return json_dict['total']
        return json_dict

if __name__ == "__main__":
    #print(Song().get_comment("http://music.163.com/weapi/v1/resource/comments/R_SO_4_{ID}?csrf_token=".format(ID="31311140"),1,10))
    
    pass



