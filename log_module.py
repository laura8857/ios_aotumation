# -*- coding: utf-8 -*-
# @Time    : 2017/3/2 下午12:00
# @Author  : Yuhsuan
# @File    : deepblu_lib.py.py
# @Software: PyCharm Community Edition

#import datetime
# from pymongo import *
# from datetime import datetime
# import requests
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

dir = '%s/' % os.getcwd()
dir = dir+datetime.datetime.now().strftime("%Y%m%d_")+"result/"
if not os.path.exists(dir):
    os.makedirs(dir)
now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
file_path = dir+now+".log"

logging.basicConfig(level=11,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logging.addLevelName(0, "N")
logging.addLevelName(11, "D")
logging.addLevelName(20, "I")
logging.addLevelName(30, "W")
logging.addLevelName(40, "E")
logging.addLevelName(50, "C")

logger = logging.getLogger(__name__)

# 5MB = 5*1000*1000 Bytes
# MaxCount = 5
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',datefmt="%Y-%m-%d %H:%M:%S")
handler = RotatingFileHandler(file_path, maxBytes=5000000,backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

d = ["d", "D", "debug", "DEBUG", "Debug"]
i = ["i","I","info","INFO","Info"]
w = ["w","W","warning","WARNING","Warning"]
e = ["e","E","error","ERROR","Error"]
c = ["c","C","critical","CRITICAL","Critical"]


def log(output,lvl=None):
    if lvl in d:
        logger.debug(output)
    elif lvl in i:
        logger.info(output)
    elif lvl in w:
        logger.warning(output)
    elif lvl in e:
        logger.error(output)
    elif lvl in c:
        logger.critical(output)
    else:
        logger.log(11,output)
        #logger.debug(output)