#!/usr/bin/env python
# encoding: utf-8
import pymysql
import time
import requests
from lxml import etree
import json
from retrying import retry
class LianjiaChuzu:
    def __init__(self,zufangleixing):
        self.zufangleixing=zufangleixing
        self.db =pymysql.connect("localhost", "root", "123456", "lianjia")
        self.xiaoqu_url = "https://wh.lianjia.com/zufang/%srt200600000001rs%s/#contentList"
        #self.xiaoqu_url = "https://wh.lianjia.com/zufang/pg2rt200600000001rs万科魅力/#contentList"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"}
    def get_xiaoqu_list(self):
        requery_sql = "select 小区,街道,大区 from xiaoqu"
        cursor = self.db.cursor()
        cursor.execute(requery_sql)
        xiaoqu_list = cursor.fetchall()
        cursor.close()
        print (xiaoqu_list)
        return xiaoqu_list
    @retry(stop_max_attempt_number=3)
    def _parse_url(self,url):
        res = requests.get(url,headers = self.headers)
        return res.content.decode()

    def parse_url(self,url):
        try:
            html_str = self._parse_url(url)
        except:
            html_str = None
        return html_str
    #获取每个小区翻页数
    def get_index(self,html):
        html_str = etree.HTML(html)
        xiaoqu_chuzu_num = html_str.xpath("//p[@class='content__title']/span[@class='content__title--hl']/text()")
        print (int(xiaoqu_chuzu_num[0]))
        if int(xiaoqu_chuzu_num[0]) > 0:
            index_list = html_str.xpath("//div[@class='content__pg']/@data-totalpage")
            index =int(index_list[0])
            print('index:' + str(index))
        else:
            index=0
        return index
    #每个小区页面数据
    def get_data(self,html,xiaoqu,jiedao,daqu):
        html_str=etree.HTML(html)
        xiaoqu_chuzu_base=html_str.xpath("//div[@class='content__list']/div[@class='content__list--item']")
        for li in xiaoqu_chuzu_base:
            xiaoqu_name=xiaoqu
            jiedao=jiedao
            daqu=daqu
            detail = li.xpath(".//p[@class='content__list--item--des']/text()")
            mianji = detail[4].strip().split("㎡")[0]
            chaoxiang=detail[5].strip()
            huxing=detail[6].strip().split()[0]
            fabushijian=li.xpath(".//p[@class='content__list--item--time oneline']/text()")[0]
            chuzu_jiage=li.xpath(".//span[@class='content__list--item-price']/em/text()")[0]
            #print(mianji,chaoxiang,huxing,fabushijian,chuzu_jiage)
            SQL = "INSERT INTO lianjia_chuzu_ing (小区,出租类型,面积,朝向,户型,发布时间,租金,街道,大区) VALUES " \
                  "('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(xiaoqu,self.zufangleixing,mianji,chaoxiang,huxing,fabushijian,chuzu_jiage,jiedao,daqu)
            cursor = self.db.cursor()
            cursor.execute(SQL)
            cursor.close()
    def commit_data(self):
        self.db.commit()
        self.db.close()


    def run(self):
        #从数据库里读取小区数据
        xiaoqu_list = self.get_xiaoqu_list()
        #制造所有小区url
        for xiaoqu in xiaoqu_list:
            xiaoqu_name = xiaoqu[0]
            xiaoqu_url = self.xiaoqu_url%('',xiaoqu_name)
            jiedao = xiaoqu[1]
            daqu = xiaoqu[2]
            #提取小区成交套数，和翻页数
            html = self.parse_url(xiaoqu_url)
            if html:
                index=self.get_index(html)
                if index:
                    for i in range(1, index + 1):
                        index_url = self.xiaoqu_url%('pg'+str(i),xiaoqu_name)
                        print(index_url)
                        html = self.parse_url(xiaoqu_url) if i == 1 else self.parse_url(index_url)
                        if html:
                            self.get_data(html,xiaoqu_name,jiedao,daqu)
        self.commit_data()

        #获取每个小区挂牌出租信息
        #写sql

if __name__=='__main__':
    LianjiaChuzu = LianjiaChuzu('整租')
    LianjiaChuzu.run()