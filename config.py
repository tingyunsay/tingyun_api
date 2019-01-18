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
proxies = {
    "ip":"192.168.218.11",
    "port":8888
}

