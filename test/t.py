#!python3
# -*- coding: utf-8 -*-
import requests,json
#url = 'http://10.0.4.168:8080/?opt=put&mq=gg_data&data=bbb=103'
url = 'http://10.0.4.168:8080/?opt=put&type=json'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer':'http://www.cnblogs.com/',
           'Origin':'http://www.cnblogs.com/',
           'Content-Type':'application/json',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
           }
data_json = {
	"type": "object",
	"para": [{
	"mq": "gg_data",
	"data":[
{
          "id": 110,
          "t":"abcd1",
          "gid": 102,
          "pcname": "abcd3",
          "mac": "abcd4",
          "pv": 105,
          "uv": 106,
          "click": 107,
          "sid": 108,
          "bdver": "e54749b76e2077dd085a46210a7ed267",
          "r_d": 1010,
          "referer": "json_object11"
		}
      ]
	}]}

#r = requests.get(url, headers=headers)
r = requests.post(url,data=json.dumps(data_json),headers=headers)
print (r.content.decode())