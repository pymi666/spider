#!python3
# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree,html
import re
class LianjiaXiaoqu:
    def __init__(self,jiedao_json):
        self.jiedao_json = jiedao_json
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"}
    def get_jiedao_url(self):
        jiedao_url_all=[]
        for daqu,jiedao_list in self.jiedao_json.items():
            for jiedao_dict in jiedao_list:
                jiedao_url_list = []
                jiedao = list(jiedao_dict.keys())[0]
                jiedao_url = jiedao_dict[jiedao]
                jiedao_url_list = [jiedao_url,jiedao,daqu]
                jiedao_url_all.append(jiedao_url_list)
        return jiedao_url_all
    def parse_url(self,url):
        res = requests.get(url,headers = self.headers)
        return res.content.decode()
    def get_index_url(self,html):
        html_str = etree.HTML(html)
        index_list = html_str.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
        index = json.loads(index_list[0])['totalPage']
        return index
    def get_jiancheng(self,xpath_jiancheng):
        s = etree.tostring(xpath_jiancheng).decode('utf-8')
        #print (s)
        jiancheng_year = re.findall(r"/&#160;(.+)&#24180;&#24314;", s, re.S)[0]
        jiancheng_year = html.fromstring(jiancheng_year).text
        #print (jiancheng_year)
        return jiancheng_year
    def get_xiaoqu(self,html_str):
        html = etree.HTML(html_str)
        daqu_list = html.xpath("//div[@class='leftContent']//li[@class='clear xiaoquListItem']")
        content_xiaoqu=[]
        for a in daqu_list:
            item = {}
            item["小区"]=a.xpath("./div[@class='info']/div[@class='title']/a/text()")[0]
            item["均价"]=a.xpath(".//div[@class='totalPrice']/span/text()")[0]
            item["建筑时间"]  = self.get_jiancheng(a.xpath(".//div[@class='positionInfo']")[0])
            item["出租"]=list(a.xpath(".//div[@class='houseInfo']/a[2]/text()")[0])[0]
            item["挂牌"]=a.xpath(".//a[@class='totalSellCount']/span/text()")[0]
            content_xiaoqu.append(item)
        return content_xiaoqu
    def save_xiaoqu(self,index,url,jiedao,jiedao_xiaoqu):
        print ('*'+url+jiedao+'*')
        xiaoqu=[]
        jiedao_xiaoqu={}
        for i in range(1,index+1):
            index_url = url+"pg"+str(i)
            html=self.parse_url(url) if i==1 else self.parse_url(index_url)
            content_xiaoqu_list=self.get_xiaoqu(html)
            #print (content_xiaoqu_list)
            xiaoqu.append(content_xiaoqu_list)
        #print ('*'*10)
        #print (xiaoqu)

        jiedao_xiaoqu[jiedao]=xiaoqu
        print (jiedao_xiaoqu)
        return jiedao_xiaoqu

    def run(self):
        #获取每个街道url,
        jiedao_xiaoqu={}
        for jiedao_list in self.get_jiedao_url():
            url = jiedao_list[0]
            jiedao = jiedao_list[1]
            daqu = jiedao_list[2]
            print (url,jiedao,daqu)
            #获取每个街道小区的翻页数
            html = self.parse_url(url)
            index = self.get_index_url(html)
            xiaoqu_list = self.save_xiaoqu(index,url,jiedao,jiedao_xiaoqu)
            #jiedao_xiaoqu = xiaoqu_list
            #获取小区数据
            qu_name = daqu+jiedao
            with open("%s.json"%qu_name, "a", encoding="utf-8") as f:
                f.write(json.dumps(xiaoqu_list,indent=4, ensure_ascii=False))
        return jiedao_xiaoqu

        #获取翻页数，制造翻页url
        #获取第二页及每一页小区数据
        #保存数据
        pass

if __name__=="__main__":
    with open("jiedao.json","rb") as f:
        jiedao_json = json.loads(f.read())
    lianjia_xiaoqu = LianjiaXiaoqu(jiedao_json)

    print (lianjia_xiaoqu.run())
