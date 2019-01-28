# tingyun_api
听云api服务，各大音乐网站不同类型的评论抓取api  
### 依赖
```
python3 

pip3 install aiohttp asyncio
```
### 使用
```
git clone https://github.com/tingyunsay/tingyun_api.git

python3 tingyun_api.py
```
## 网易云
### post 形式, 参数:   
```
id  -- 对应类型下的id: songid,albumid,songlistid  
offset -- 第几页  
limit  -- 每一页的评论数  
type -- 类型: song,songlist,singer
```
```
res=requests.post("http://127.0.0.1:8000/hello/wangyiyun_all",data={"id":"2094881280","offset":"1","limit":10,"type":"songlist"})
```
### return
返回是json.dumps(dict) 的字符串，可以使用json.loads(res.content) 成一个字典类型的数据，再进行进一步操作

## QQ
### post 形式, 参数:   
```
id  -- 对应类型下的id: songid,albumid,songlistid  
offset -- 第几页  
limit  -- 每一页的评论数  
type -- 类型: song,songlist,singer
```
```
res=requests.post("http://127.0.0.1:8000/hello/qq_all",data={"id":"0015rUVB2OUdGA","offset":"1","limit":10,"type":"album"})
```
**注意**  
QQ的song和album均是以mid传递进来（其在前端作了一层转换，先将mid ==> topid ,再进行接口访问），而 album则是直接传真实topid即可  
### return
返回是json.dumps(dict) 的字符串，可以使用json.loads(res.content) 成一个字典类型的数据，再进行进一步操作
