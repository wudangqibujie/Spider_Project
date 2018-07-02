url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
data = {
'first': 'false',
'pn': 11,
'kd': 'Python',
}
import requests
import json
headers = {
    "Referer":"https://www.lagou.com/jobs/list_Java?px=default&city=%E4%B8%8A%E6%B5%B7",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
r = requests.post(url,data=data,headers=headers)
print(r.text)