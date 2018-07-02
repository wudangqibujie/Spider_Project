import logging
from settings import *
class Log(object):
    def __init__(self,set_level=LOG_LEVLE):
        choi = {"debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR}
        self.logger = logging.getLogger()
        self.logger.setLevel(choi[set_level])
        logfile = 'logger.txt'
        fh = logging.FileHandler(logfile, mode='a', encoding="utf-8")
        fh.setLevel(choi["warning"])
        ch = logging.StreamHandler()
        ch.setLevel(choi[set_level])
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    def log(self,obj,obj_level):
        self.logger.debug(obj) if obj_level == "debug" else None
        self.logger.info(obj) if obj_level == "info" else None
        self.logger.warning(obj) if obj_level == "warning" else None
        self.logger.error(obj) if obj_level == "error" else None
log = Log()
if __name__ == '__main__':
    l = Log()
    for i in range(10):
        l.log(str(i),"info")

    pass



















# import logging
#
#
# # 第一步，创建一个logger
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)  # Log等级总开关
# # 第二步，创建一个handler，用于写入日志文件
# logfile = './log/logger.txt'
# fh = logging.FileHandler(logfile, mode='a')
# fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 第三步，再创建一个handler，用于输出到控制台
# ch = logging.StreamHandler()
# ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关
# # 第四步，定义handler的输出格式
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s--%(threadName)s")
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# # 第五步，将logger添加到handler里面
# logger.addHandler(fh)
# logger.addHandler(ch)
# # 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')