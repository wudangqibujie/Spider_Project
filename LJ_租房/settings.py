import random
SPIDER_NAME = "LJ_ZF"

REDIS_HOST = '*******'
REDIS_PORT = 6379

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '*******'
MYSQL_DATABASE = SPIDER_NAME

TIMEOUT = None

CON_NUMS = 5

LOG_LEVLE = "debug"

TRANS_ITEM = False

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_NAME = SPIDER_NAME

INTO_DB = False


agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"

]

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "H0430Z21W9G039LD"
proxyPass = "6197FECC49ED762A"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

HEADERS = {"User-Agent":random.choice(agents)}
PROXIES = None