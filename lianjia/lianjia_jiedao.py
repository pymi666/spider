#!python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
import json
class LianjiaJiedao:
    def __init__(self):
        self.url = "https://wh.lianjia.com/xiaoqu/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"}
    def parse_url(self,url):
        res = requests.get(url,headers = self.headers)
        return res.content.decode()
    def get_daqu(self,html_str):
        html = etree.HTML(html_str)
        daqu_list = html.xpath("//div[@data-role='ershoufang']/div[1]/a")
        content_daqu=[]
        for a in daqu_list:
            item = {}
            item[a.xpath("./text()")[0]]="https://wh.lianjia.com"+a.xpath("./@href")[0]
            content_daqu.append(item)
        return content_daqu
    def get_jiedao(self,daqu,daqu_url,jiedao):
            html_jiedao = self.parse_url(daqu_url)
            html = etree.HTML(html_jiedao)
            jiedao_list = html.xpath("//div[@data-role='ershoufang']/div[2]/a")
            content_jiedao=[]
            for b in jiedao_list:
                item = {}
                item[b.xpath("./text()")[0]] = "https://wh.lianjia.com" + b.xpath("./@href")[0]
                content_jiedao.append(item)
            jiedao[daqu] = content_jiedao
            return jiedao
    def save_data(self,jiedao_list):
        with open("jiedao.json","a",encoding="utf-8") as f:
            f.write(json.dumps(jiedao_list,ensure_ascii=False))

    def run(self):
        #获取武汉大区：
        html = self.parse_url(self.url)
        daqu_list = self.get_daqu(html)
        jiedao = {}
        # 获取每个街道里小区
        for item in daqu_list:
            daqu = list(item.keys())[0]
            daqu_url = item[daqu]
            jiedao = self.get_jiedao(daqu,daqu_url,jiedao)
        self.save_data(jiedao)

if __name__ == '__main__':
   jiedao = LianjiaJiedao()
   jiedao.run()

