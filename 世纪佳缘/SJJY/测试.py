import requests
import json
import re
url = "http://search.jiayuan.com/v2/search_v2.php"
headers = {
'Host': 'search.jiayuan.com',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Origin': 'http://search.jiayuan.com',
'Referer': 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=&sn=default&sv=1&p=1&pt=39234&ft=off&f=select&mt=d',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
'Cookie': 'guider_quick_search=on; SESSION_HASH=6096ea8d29ca6d5fe5ea0a577b8d1ad9bc079369; REG_ST_ID=15; REG_ST_URL=https://www.baidu.com/link?url=B04F7-_8yzNA-DNSjazYxE0SUKQTvq0b_WYvLRXYLAfi3zq8ps8HFF0pK6emzlFG&wd=&eqid=c0862b200001f168000000065b1a16c4; REG_REF_URL=https://www.baidu.com/link?url=B04F7-_8yzNA-DNSjazYxE0SUKQTvq0b_WYvLRXYLAfi3zq8ps8HFF0pK6emzlFG&wd=&eqid=c0862b200001f168000000065b1a16c4; user_access=1; PHPSESSID=cb835d7fe8a91eead9181f3b3431ee70; is_searchv2=1',
}
for i in range(1,5):
    post_data = {
    'sex': 'f',
    'key': '%E9%AB%98%E6%8C%91',
    'stc': '1:44,2:20.28,3:165.0,23:1',
    'sn': 'default',
    'sv': 1,
    'p': i,
    'f': 'search',
    'listStyle': 'bigPhoto',
    'pri_uid': 0,
    'jsversion': 'v5'
    }
    r = requests.post(url)
    text = r.text.encode("utf-8").decode("unicode_escape")
    text_1 = re.findall(r'"userInfo":(.*?]),"second_searc',text)[0]
    text_first = json.loads(text_1)
    print(text_first)
    text_2 = re.findall(r'express_search":(.*?),"cond',text)[0]
    text_second = json.loads(text_2)
    print(text_second)
    for i in text_first:
        print(i)
    for j in text_second:
        print(j)