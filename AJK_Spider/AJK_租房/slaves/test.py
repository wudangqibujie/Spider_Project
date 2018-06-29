id = '77476055'
base_report = "https://www.xin.com/apis/ajax_report/get_chake_report/?carid="
import requests
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Referer":"https://www.xin.com/40d0arywy9/che77476055.html",
}
r  =requests.get(base_report+id,headers=headers)
import json
data = json.loads(r.text)
print(data)