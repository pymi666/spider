# encoding: utf-8
import time
import requests
import chardet

_time = int(time.time()*1000)
headers_app={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
             "Referer": "https: // m.douban.com / tv / japanese"}
url = "https://m.douban.com/rexxar/api/v2/subject_collection/tv_japanese/items?os=ios&for_mobile=1&start=0&count=18&loc_id=108288&_=%d"%_time
print (url)
r = requests.get(url,headers=headers_app)

print (r.content.decode().encode('utf-8').decode("unicode_escape"))
#print (r.text.encode('utf-8').decode("unicode_escape"))
'''
class DouBan():
    def __init__(self,country):
        self.country = country
        self.cuntry_url = country_url
    def headers(self):
        Referer = "https://m.douban.com/tv/%s"%self.country
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
             "Referer": Referer}
        return headers
    def url_pool(self):
        url = "https://m.douban.com/rexxar/api/v2/subject_collection/%s/items?os=ios&for_mobile=1&start=%d&count=18&loc_id=108288&_=%d"%(self.cuntry_url,start,_time)
    def run(self):
        #构造url地址池
        #发送请球，获取响应
        #提取数据
        #保存数据
'''