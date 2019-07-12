#!python3
# -*- coding: utf-8 -*-
import requests
from retrying import retry
@retry(stop_max_attempt_number=3)
def _parse_url(url,method,data,proxies,headers):
    if method=="get":
        r = requests.get(url,headers=headers,proxies=proxies)
    else:
        r = requests.post(url,data=data,headers=headers,proxies=proxies)
    assert r.status_code == 200
    return r.content.decode()

def parse_url(url,headers,method = "get",data = None,proxies = {}):
    try:
        html_str = _parse_url(url,method,data,proxies,headers)
    except :
        html_str = None

    return html_str

if __name__ == "__main__":
    url = "http://www.baidu.com"
    headers = {}
    print (parse_url(url,headers))
