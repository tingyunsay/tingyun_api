#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#根据配置生成相应的各个接口
items = {
    "wangyiyun":{
        "songlist":{
            #0表示不使用配置
            "use":0,
            
        },
        "song":{
            "use":1,
            
        
        }
    
    },
    "qq":{
    
    },
    "xiami":{
        
    
    }
}
#维护的squid集群,单独管理
proxies = [
    "192.168.218.11:9112"
]

redis_conf = {
    #"ip" : "10.1.18.65 ",
    #"port" : "7001",
    "ip" : "127.0.0.1",
    "port" : "6379",
}

banned_key = "sc:hash:banned:user"
banned_mid = "sc:hash:banned:mid"


