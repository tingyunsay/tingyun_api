#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author -- tingyun
#date -- 20190119
from utils.qq_api import *
from utils.wangyiyun_api import *
import asyncio
from aiohttp import web
import re
from config import *
import redis
import logging

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def wangyiyun_all(request):
    info = await request.text()
    req = {}
    for tmp in info.split("&"):
        fk = tmp.split('=')
        req[fk[0]] = fk[1]
    
    if req.get('id') and req.get('offset') and req.get('limit') and req.get('type'):
        ID = req.get('id')
        offset = req.get('offset')
        limit = req.get('limit')
        Type = req.get('type')
        if Type == "song":
            text = WYY_All().get_comment("http://music.163.com/weapi/v1/resource/comments/R_SO_4_{ID}?csrf_token=".format(ID=ID),offset,limit)
        elif Type == "album":
            text = WYY_All().get_comment("http://music.163.com/weapi/v1/resource/comments/R_AL_3_{ID}?csrf_token=".format(ID=ID),offset,limit)
        elif Type == "songlist":
            text = WYY_All().get_comment("http://music.163.com/weapi/v1/resource/comments/A_PL_0_{ID}?csrf_token=".format(ID=ID),offset,limit)
        else:
            text = "your param is not in [album , song , songlist] , can not be processed."
        return web.Response(body=json.dumps(text))
    else:
        text = "wrong param , failed"
        return web.Response(body=text.encode('utf-8'))

async def qq_all(request):
    #print(request.message)
    #print(await request.text())
    info = await request.text()
    req = {}
    for tmp in info.split("&"):
        fk = tmp.split('=')
        req[fk[0]] = fk[1]
    
    if req.get('id') and req.get('offset') and req.get('limit') and req.get('type'):
        ID = req.get('id')
        offset = req.get('offset')
        limit = req.get('limit')
        Type = req.get('type')
        if Type == "song":
            text = QQ_Song().get_comment("https://y.qq.com/n/yqq/song/{ID}.html".format(ID=ID),offset,limit)
        elif Type == "album":
            text = QQ_Album().get_comment("https://y.qq.com/n/yqq/album/{ID}.html".format(ID=ID),offset,limit)
        elif Type == "songlist":
            text = QQ_Songlist().get_comment("https://y.qq.com/n/yqq/playsquare/{ID}.html".format(ID=ID),offset,limit)
        else:
            text = "your param is not in [album , song , songlist] , can not be processed."
        
        return web.Response(body=json.dumps(text))
    else:
        text = "wrong param , failed"
        return web.Response(body=text.encode('utf-8'))

async def get_ban(request):
    get = request.rel_url.query
    Type = get['Type']
    
    if Type == 'banned':
        ckey = banned_key
        
        #redis获取的k,v均是byte,需转成str
        res = hget_redis(ckey)
        h = {}
        for k,v in res.items():
            h[k.decode()] = v.decode()
        return web.Response(text = json.dumps(h))
        
    if Type == '':

        pass

#添加封禁uid
async def set_ban(request):
    post = await request.post()
    uid = int(post['uid'])
    if uid > 0:
        ckey = banned_key
        res = hset_redis(ckey , uid , 1)
        return web.Response( text =  json.dumps({"status" : 1 , "errmsg" : "" }))

    return web.Response( text =  json.dumps({"status" : 0 , "errmsg" : "hset failed" }))

#移除封禁uid
async def remove_ban(request):
    post = await request.post()
    uid = int(post['uid'])
    if uid > 0:
        ckey = banned_key
        res = hdel_redis(ckey , uid )
        return web.Response( text =  json.dumps({"status" : 1 , "errmsg" : "" }))

    return web.Response( text =  json.dumps({"status" : 0 , "errmsg" : "hdel failed" }))

#获取map
def hget_redis(ckey):
    r = redis.Redis(redis_conf['ip'], redis_conf['port'], db=0)
    r_con = r.hgetall(ckey)
    return r_con

#添加封禁uid
def hset_redis(ckey , k , v):
    r = redis.Redis(redis_conf['ip'], redis_conf['port'], db=0)
    r_con = r.hset(ckey , k , v)
    return r_con

#移除封禁uid
def hdel_redis(ckey , k ):
    r = redis.Redis(redis_conf['ip'], redis_conf['port'], db=0)
    r_con = r.hdel(ckey , k )
    return r_con


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_routes([web.get('/',index),
                          web.get('/hello/{name}',hello),
                          web.post('/comment/qq_all',qq_all),
                          web.post('/comment/wangyiyun_all',wangyiyun_all),
                          web.get('/snapchat/redis/get',get_ban),
                          web.post('/snapchat/redis/add',set_ban),
                          web.post('/snapchat/redis/remove',remove_ban),
                ])
    #app.router.add_get('/snapchat/redis',get_redis)
    
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
