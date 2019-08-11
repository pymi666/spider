#!python3
# -*- coding: utf-8 -*-
import pymysql
import time
import requests
from lxml import etree
import json
from retrying import retry
class LianjiaChengjiao:
    def __init__(self):
        self.db =pymysql.connect("localhost", "root", "123456", "lianjia")
        self.xiaoqu_url = "https://wh.lianjia.com/chengjiao/rs%s"
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
    #一个小区的所有成交房子的详情url
    def get_xiaoqu_detail_url(self,html,xiaoqu,jiedao,daqu):
        html_str = etree.HTML(html)
        xiaoqu_chengjiao_num = html_str.xpath("//div[@class='total fl']/span/text()")
        print (int(xiaoqu_chengjiao_num[0]))
        alone_xiaoqu_url_list = [[xiaoqu, jiedao, daqu], []]
        if int(xiaoqu_chengjiao_num[0]) > 0:
            index_list = html_str.xpath("//div[@class='page-box house-lst-page-box']/@page-data")
            index = json.loads(index_list[0])['totalPage']
            print('index:' + str(index))
            for i in range(1,index+1):
                index_url = "https://wh.lianjia.com/chengjiao/"+"pg"+str(i)+"rs"+xiaoqu
                print (index_url)
                html=self.parse_url(self.xiaoqu_url%(xiaoqu)) if i==1 else self.parse_url(index_url)
                if html:
                    html_str = etree.HTML(html)
                    xiaoqu_detail_url = html_str.xpath("//ul[@class='listContent']/li/div[@class='info']/div[@class='title']/a/@href")
                    alone_xiaoqu_url_list[1].extend(xiaoqu_detail_url)
                #print (alone_xiaoqu_url_list)
                #print (len(alone_xiaoqu_url_list))
                #[[xiaoqu,jiedao,xiaoqu],[url1,url2]]
                else:
                    alone_xiaoqu_url_list = [[xiaoqu, jiedao, daqu], []]
        else:
            alone_xiaoqu_url_list = [[xiaoqu, jiedao, daqu], []]
        return alone_xiaoqu_url_list
    #针对一个房子的url，提取信息信息
    def get_xiaoqu_detail(self,html,xiaoqu_name,jiedao,daqu):
        html_str = etree.HTML(html)
        xiaoqu = xiaoqu_name

        for i in range(3):
            try:
                chengjiao_time= html_str.xpath("//div[@class='wrapper']/span/text()")[0].split()[0]
            except IndexError:
                chengjiao_time=''
            if chengjiao_time:
                break
            time.sleep(1)
        print (chengjiao_time)
        fangwu_base = html_str.xpath("//div[@class='introContent']/div[@class='base']/div[@class='content']/ul")[0]
        fangwuhuxing=fangwu_base.xpath("./li/span[text()='房屋户型']/../text()")[0].strip()
        mianji=fangwu_base.xpath("./li/span[text()='建筑面积']/../text()")[0].strip().strip('㎡')
        taoneimianji=fangwu_base.xpath("./li/span[text()='套内面积']/../text()")[0].strip()
        taoneimianji = 'Null' if taoneimianji == "暂无数据" else taoneimianji.strip('㎡')
        chaoxiang=fangwu_base.xpath("./li/span[text()='房屋朝向']/../text()")[0].strip()
        zhuangxiu=fangwu_base.xpath("./li/span[text()='装修情况']/../text()")[0].strip()
        chanquannianxian=fangwu_base.xpath("./li/span[text()='产权年限']/../text()")[0].strip()
        louceng=fangwu_base.xpath("./li/span[text()='所在楼层']/../text()")[0].strip()
        huxingjiegou=fangwu_base.xpath("./li/span[text()='户型结构']/../text()")[0].strip()
        jianzuleixing=fangwu_base.xpath("./li/span[text()='建筑类型']/../text()")[0].strip()
        jianzu_time=fangwu_base.xpath("./li/span[text()='建成年代']/../text()")[0].strip()
        jianzujiegou=fangwu_base.xpath("./li/span[text()='建筑结构']/../text()")[0].strip()
        tihubili=fangwu_base.xpath("./li/span[text()='梯户比例']/../text()")[0].strip()
        dianti=fangwu_base.xpath("./li/span[text()='配备电梯']/../text()")[0].strip()
        zongjia=html_str.xpath("//div[@class='price']/span[@class='dealTotalPrice']/i/text()")[0].strip()
        danjia=html_str.xpath("//div[@class='price']/b/text()")[0]

        fangwu_info = html_str.xpath("//div[@class='info fr']/div[@class='msg']")[0]
        guapaijia=fangwu_info.xpath("./span[1]/label/text()")[0].strip()
        chengijaozhouqi=fangwu_info.xpath("./span[2]/label/text()")[0].strip()
        tiaojia=fangwu_info.xpath("./span[3]/label/text()")[0].strip()
        daikan=fangwu_info.xpath("./span[4]/label/text()")[0].strip()
        guanzhu=int(fangwu_info.xpath("./span[5]/label/text()")[0].strip())
        guanzhu = None if guanzhu == "暂无数据" else guanzhu
        liulan=fangwu_info.xpath("./span[6]/label/text()")[0].strip()
        liulan = None if liulan == "暂无数据" else liulan

        fangwu_transaction=html_str.xpath("//div[@class='transaction']//div[@class='content']/ul")[0]
        guaipaishijian=fangwu_transaction.xpath("./li[3]/text()")[0].strip()
        fangban_time=fangwu_transaction.xpath("./li[5]/text()")[0].strip()
        jiaoyiquanshu=fangwu_transaction.xpath("./li[2]/text()")[0].strip()
        fangwuyongtu=fangwu_transaction.xpath("./li[4]/text()")[0].strip()
        fangquan=fangwu_transaction.xpath("./li[6]/text()")[0].strip()
        jiedao= jiedao
        daqu= daqu

        write_sql = "INSERT INTO chengjiao (小区,成交时间,房屋户型,建筑面积,套内面积,朝向,装修,产权年限,楼层,户型结构,建筑类型,建成年代,建筑结构,梯户比例,配备电梯,总价,单价,挂牌价,成交周期,调价,带看,关注,浏览,挂牌时间,房本年限,交易权属,房屋用途,房权所属,街道,大区) VALUES " \
                    "('{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(xiaoqu,chengjiao_time,fangwuhuxing,mianji,taoneimianji,chaoxiang,zhuangxiu,chanquannianxian,louceng,huxingjiegou,jianzuleixing,jianzu_time,jianzujiegou,tihubili,dianti,zongjia,danjia,guapaijia,chengijaozhouqi,tiaojia,daikan,guanzhu,liulan,guaipaishijian,fangban_time,jiaoyiquanshu,fangwuyongtu,fangquan,jiedao,daqu)
        print (write_sql)
        return write_sql

    def save_data(self,SQL):
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
            xiaoqu_url = self.xiaoqu_url%(xiaoqu_name)
            jiedao = xiaoqu[1]
            daqu = xiaoqu[2]
            #提取小区成交套数，和翻页数
            html = self.parse_url(xiaoqu_url)
            if html:
                alone_xiaoqu_url_list=self.get_xiaoqu_detail_url(html,xiaoqu_name,jiedao,daqu)
            #获取每个翻页的小区数据
                if alone_xiaoqu_url_list[1]:
                    for url in alone_xiaoqu_url_list[1]:
                        print (url)
                        html = self.parse_url(url)
                        if html:
                            try:
                                add_sql=self.get_xiaoqu_detail(html,xiaoqu_name,jiedao,daqu)
                                self.save_data(add_sql)
                            except:
                                pass
        self.commit_data()
        #写入数据库
        #关闭数据库
if __name__=='__main__':
    lianjia_chengjiao = LianjiaChengjiao()
    lianjia_chengjiao.run()

