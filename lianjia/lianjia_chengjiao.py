#!python3
# -*- coding: utf-8 -*-
import pymysql
import requests
from lxml import etree
import json
class LianjiaChengjiao:
    def __init__(self):
        self.db =pymysql.connect("localhost", "root", "123456", "lianjia")
        self.cursor = self.db.cursor()
        self.xiaoqu_url = "https://wh.lianjia.com/chengjiao/rs%s"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"}
    def get_xiaoqu_list(self):

        requery_sql = "select 小区 from xiaoqu limit 1"
        self.cursor.execute(requery_sql)
        xiaoqu_list = self.cursor.fetchall()
        print (xiaoqu_list)
        return xiaoqu_list
    def parse_url(self,url):
        res = requests.get(url,headers = self.headers)
        return res.content.decode()

    def get_xiaoqu_detail_url(self,html,xiaoqu):
        html_str = etree.HTML(html)
        xiaoqu_chengjiao_num = html_str.xpath("//div[@class='total fl']/span/text()")
        print (int(xiaoqu_chengjiao_num[0]))
        index_list = html_str.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
        index = json.loads(index_list[0])['totalPage']
        alone_xiaoqu_url_list=[]
        print('index:' + str(index))
        for i in range(1,index+1):
            index_url = "https://wh.lianjia.com/chengjiao/"+"pg"+str(i)+"rs"+xiaoqu
            print (index_url)
            html=self.parse_url(self.xiaoqu_url%(xiaoqu)) if i==1 else self.parse_url(index_url)
            html_str = etree.HTML(html)
            if int(xiaoqu_chengjiao_num[0]) > 0:
                xiaoqu_detail_url = html_str.xpath("//ul[@class='listContent']/li/div[@class='info']/div[@class='title']/a/@href")
                alone_xiaoqu_url_list.append(xiaoqu_detail_url)
        print (alone_xiaoqu_url_list)
        return alone_xiaoqu_url_list
    def run(self):
        #从数据库里读取小区数据
        xiaoqu_list = self.get_xiaoqu_list()
        #制造所有小区url
        for xiaoqu in xiaoqu_list:
            xiaoqu_url = self.xiaoqu_url%(xiaoqu[0])
            #提取小区成交套数，和翻页数
            html = self.parse_url(xiaoqu_url)
            self.get_xiaoqu_detail_url(html,xiaoqu[0])
        #获取每个翻页的小区数据
        #写入数据库
        #关闭数据库
        pass
if __name__=='__main__':
    lianjia_chengjiao = LianjiaChengjiao()
    lianjia_chengjiao.run()
