import os
import sys

from lib.tushare.pro.stock_company import stock_company

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

date = None
if len(sys.argv) == 2:
    script, date = sys.argv
    print(script)
    print(date)

# 获取基础信息数据
stock_company(exchange='SSE', date=date)
stock_company(exchange='SZSE', date=date)
