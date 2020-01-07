import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from lib.tushare.pro.stock_basics import stock_basics

date = None
if len(sys.argv) == 2:
    script, date = sys.argv

# stock_basics(date='20200106')

# 获取基础信息数据
stock_basics(date)
