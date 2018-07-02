id = '77476055'
base_report = "https://bj.lianjia.com/ershoufang/"
import requests
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    # "Referer":"https://www.xin.com/40d0arywy9/che77476055.html",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
r  =requests.get(base_report,headers=headers,allow_redirects=True)
print(r.history)
# print(r.text)
print(r.url)
