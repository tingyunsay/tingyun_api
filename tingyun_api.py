#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author -- tingyun
#date -- 20190119
from wangyiyun_api import *
from qq_api import *
import asyncio
from aiohttp import web
import re
async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def wangyiyun_song(request):
    #print(request.message)
    #print(request.text())
    info = await request.text()
    req = {}
    for tmp in info.split("&"):
        fk = tmp.split('=')
        req[fk[0]] = fk[1]
    
    if req.get('id') and req.get('offset') and req.get('limit'):
        ID = req.get('id')
        offset = req.get('offset')
        limit = req.get('limit')
        text = WYY_Song().get_comment("http://music.163.com/weapi/v1/resource/comments/R_SO_4_{ID}?csrf_token=".format(ID=ID),offset,limit)
        return web.Response(body=json.dumps(text))
    else:
        text = "wrong param , failed"
        return web.Response(body=text.encode('utf-8'))
async def qq_song(request):
    #print(request.message)
    #print(await request.text())
    info = await request.text()
    req = {}
    for tmp in info.split("&"):
        fk = tmp.split('=')
        req[fk[0]] = fk[1]
    
    if req.get('id') and req.get('offset') and req.get('limit'):
        ID = req.get('id')
        offset = req.get('offset')
        limit = req.get('limit')
        text = QQ_Song().get_comment("https://y.qq.com/n/yqq/song/{ID}.html".format(ID=ID),offset,limit)
        return web.Response(body=json.dumps(text))
    else:
        text = "wrong param , failed"
        return web.Response(body=text.encode('utf-8'))
async def init(loop):
    app = web.Application(loop=loop)
    """
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    app.router.add_route('POST', '/hello/qq_song', qq_song)
    app.router.add_route('POST', '/hello/wangyiyun_song', wangyiyun_song)
    """
    app.router.add_routes([web.get('/',index),
                          web.get('/hello/{name}',hello),
                          web.post('/hello/qq_song',qq_song),
                          web.post('/hello/wangyiyun_song',wangyiyun_song)
                ])
    
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
