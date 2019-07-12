#!python3
# -*- coding: utf-8 -*-

import requests
import sys

class FanYi:
    def __init__(self,trans_str):
        self.url = "http://m.youdao.com/translate"
        self.headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
        self.trans_str = trans_str
    def _post(self,data):
        r = requests.post(self.url,data=data,headers=self.headers)
        return r.content.decode()

    def run(self):
        #伪造要发送的data
        data = {"inputtext":self.trans_str,"type":"AUTO"}

        #发送请求，获得相应

        fanyin_data = self._post(data)
        #提取数据
        return fanyin_data
if __name__ == "__main__":
    trans_str= sys.argv[1]
    baidu_fanyi = FanYi(trans_str)
    print (baidu_fanyi.run())
