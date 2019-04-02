import tushare as ts
import threading

import config.config as config

class MyTushare(object):

    _instance_lock = threading.Lock()

    ts = None
    pro = None

    def __init__(self):
        ts.set_token(config.TUSHARE_TOKEN)

        self.ts = ts
        self.pro = ts.pro_api()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(MyTushare, "_instance"):
            with MyTushare._instance_lock:
                if not hasattr(MyTushare, "_instance"):
                    MyTushare._instance = MyTushare(*args, **kwargs)
        return MyTushare._instance

    def getTs(self):
        return self.ts

    def getPro(self):
        return self.pro

    def trade_cal(self, exchange, start_date, end_date, is_open):
        """获取各大交易所交易日历数据,默认提取的是上交所"""
        return self.pro.trade_cal(exchange, start_date, end_date, is_open)

    def is_trade_cal(self, exchange, date):
        """是否交易日"""
        df = self.pro.trade_cal(exchange = exchange, start_date = date, end_date = date)
        # print(df['is_open'])
        return True if df['is_open'][0] == 1 else False

MyTushare = MyTushare.instance()