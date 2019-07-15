# encoding: utf-8
import time
import requests
import json
headers_app = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
             "Referer": "https: // m.douban.com / tv / japanese"}

url = "https://m.douban.com/rexxar/api/v2/subject_collection/tv_japanese/items?os=ios&for_mobile=1&start=0&count=18"

r = requests.get(url,headers=headers_app)
data = r.content.decode()
data_json = json.loads(data)
print (data_json)

print (r.content.decode().encode('utf-8').decode("unicode_escape"))
for i in data_json["subject_collection_items"]:
    with open("豆瓣电视名.txt","a",encoding="utf-8") as f:
        print (i["title"])

        f.write(i["title"]+"\n")
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
