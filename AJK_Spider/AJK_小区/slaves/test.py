id = '77476055'
base_report = "https://zhengzhou.anjuke.com/v3/ajax/prop/pricetrend/?commid=227517"
import requests
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # "Referer":"https://zhengzhou.anjuke.com/prop/view/A1225466506?from=filter-saleMetro&spread=commsearch_p&position=1&kwtype=filter&now_time=1528182641",
}
r  =requests.get(base_report,headers=headers)
import json
data = json.loads(r.text)
print(data)
# print(r.text)