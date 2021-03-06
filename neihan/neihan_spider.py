#!/usr/bin/env python
# encoding: utf-8
import requests
import re
import json

class Neihan:
    def __init__(self):
        self.start_url = "http://neihanshequ.com/"
        self.next_url_temp = "http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}"
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    def parse_url(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_first_page_content_list(self,html_str):
        content_list = re.findall(r"<h1 class=\"title\">.*?<p>(.*?)</p>",html_str,re.S)
        max_time = re.findall("max_time: '(.*?)',",html_str)[0]
        return content_list,max_time
    def get_content_list(self,json_str):
        #提取从第二页开始的josn数据
        dict_ret = json.loads(json_str)
        data = dict_ret["data"]["data"]
        content_list = [i["group"]["content"] for i in data]
        max_time = dict_ret["data"]["max_time"]
        has_more = dict_ret["data"]["has_more"]
        return content_list,max_time,has_more

    def save_content_list(self,content_list):
        with open("neihan.txt","a",encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dump(content,ensure_ascii=False,indent=4))
                f.write("\n")
        print ("保存成功")

    def run(self):
        #1、发送请求，获取响应
        html_str = self.parse_url(self.start_url)
        #2、提取数据
        content_list,max_time = self.get_first_page_content_list(html_str)
        #3、保存数据
        self.save_content_list(content_list)
        has_more = True #有第二页
        while has_more:
            #5.构造下一页的url地址
            next_url = self.next_url_temp.format(max_time)
            #6.发送请求，获取响应
            json_str = self.parse_url(next_url)
            #7.提取数据，提取max_time
            content_lsit,max_time,has_more = self.get_content_list(json_str)
            #8.保存
            self.save_content_list(content_lsit)
            #9.循环5-8步

if __name__ == '__main__':
    neihan = Neihan()
    neihan.run()