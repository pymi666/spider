# encoding: utf-8
import time
import requests
import json

'''
headers_app = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
             "Referer": "https: // m.douban.com / tv / japanese"}

url = "https://m.douban.com/rexxar/api/v2/subject_collection/tv_japanese/items?os=ios&for_mobile=1&start=0&count=18"

r = requests.get(url,headers=headers_app)
data = r.content.decode()
data_json = json.loads(data)
print (r.json()["total"])

print (r.content.decode().encode('utf-8').decode("unicode_escape"))
for i in data_json["subject_collection_items"]:
    with open("豆瓣电视名.txt","a",encoding="utf-8") as f:
        f.write(i["title"]+"\n")
#print (r.text.encode('utf-8').decode("unicode_escape"))
'''
class DouBan():
    def __init__(self,country,country_url):
        self.country = country
        self.cuntry_url = country_url

    def headers(self):
        Referer = "https://m.douban.com/tv/%s"%self.country
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
             "Referer": Referer}
        return headers

    def url_pool(self):
        url = "https://m.douban.com/rexxar/api/v2/subject_collection/%s/items?os=ios&for_mobile=1&start=%d&count=18&loc_id=108288"
        start = 0
        post_url = url%(self.cuntry_url,start)
        post_url_list = []
        r = requests.get(post_url, headers=self.headers())
        tv_num = r.json()["total"]
        while True:
            if (start+18) < tv_num:
                post_url_list.append(url%(self.cuntry_url,start))
            else:
                break
            start +=18
        return post_url_list

    def run(self):
        #构造url地址池
        url_list = self.url_pool()
        #发送请球，获取响应
        title_list = []
        for url in url_list:
            r = requests.get(url, headers=self.headers())
            for title in r.json()["subject_collection_items"]:
                  # 提取数据
                title_list.append(title["title"])
        #保存数据:
        title_dict = {self.country:title_list}
        return title_dict

if __name__ == "__main__":
    country = {"chinese":"tv_domestic","american":"tv_american","korean":"tv_korean","japanese":"tv_japanese"}
    for country_name,country_url in country.items():
        douban_tv = DouBan(country_name,country_url)
        tv_dict = douban_tv.run()
        print (tv_dict)