#coding:utf-8
from scrapy.cmdline import execute

import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logging.getLogger('scrapy').setLevel(logging.WARNING)
execute(["scrapy", "crawl", "userinfo"])