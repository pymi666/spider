#!/usr/bin/env python
# encoding: utf-8
import requests
headers_win={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
headers_app={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
def _parse_url(url,method,data,agent,proxies):
    headers = headers_win if agent=="win" else headers_app
    print (headers)
    if method=="POST":
        r = requests.post(url,data=data,headers=headers,proxies=proxies)
    else:
        r =requests.get(url,headers=headers)
    assert r.status_code == 200
    return r.content.decode()

def parse_url(url,method="GET",data=None,agent="win",proxies={}):
    try:
        html_str = _parse_url(url,method,data,agent,proxies)
    except:
        html_str = None
    return html_str

if __name__ == '__main__':
    url = "http://www.baidu.com"
    print(parse_url(url,agent="app"))