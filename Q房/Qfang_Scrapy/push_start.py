from redis  import StrictRedis
tasks = [
"https://beijing.qfang.com/sale"
        ]
r = StrictRedis()
for i in tasks:
    r.lpush("QF:start_urls",i)