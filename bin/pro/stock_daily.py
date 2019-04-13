import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from common.db import Mysql
from common.MyTushare import MyTushare as mts
import config.tables as conf_talbes
import config.config as conf

desc = '日线行情'

def daily(date=None, cache_file=False, debug=False):
    """
    日线行情

    数据更新时间：交易日每天15点～16点之间

    Args:
        date:

    Returns:

    """
    # 如果没有传日期，默认取当前日期
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
        # date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    print('获取 ' + desc + ' ' + date)

    # 存储 日线行情 表名
    table_pro_daily = conf_talbes.PRO_STOCK_DAILY

    engine = Mysql.conn()

    # 是否交易日
    if mts.is_trade_cal(exchange = '', date = date) == False:
        print('非交易日')
        return False

    # 检查表是否存在
    check_table_sql = "show tables like '{}'".format(table_pro_daily)
    check_table_result = engine.execute(check_table_sql).scalar()

    # 检查表是否存在数据
    check = None
    if check_table_result != None:
        check_table_data_sql = "SELECT * FROM {} where `ts_code` = '000001.SZ' and `created_date` = '{}'".format(table_pro_daily,
                                                                                                date)
        check = engine.execute(check_table_data_sql).fetchone()

    if check is None:
        # 所有股票基本数据的文件,可以临时保存文件
        tmp_file_stock_daily_path = conf.CACHE_FILE_PATH + '/pro/daily'
        if not os.path.exists(tmp_file_stock_daily_path):
            os.makedirs(tmp_file_stock_daily_path)

        tmp_file_daily = tmp_file_stock_daily_path + '/' + date + '.csv'

        tmpFileCheck = os.path.isfile(tmp_file_daily)
        if tmpFileCheck:
            # 从文件读取所有股票基本数据
            print('从文件读取 ' + desc)
            daily_data = pd.read_csv(tmp_file_daily, dtype={'ts_code': np.str_, 'totalAssets': np.str_}).sort_values(by='ts_code')
            # print(all_stock.sort_values(by=['code']))
        else:
            # 从API获取所有股票基本数据
            print('从API获取 ' + desc)

            try:
                daily_data = mts.getPro().daily(trade_date=date)
            except Exception as e:
                print(date)
                print(e)

                return False

            daily_data = daily_data.sort_values('ts_code')
            daily_data.to_csv(tmp_file_daily, index=False)

        daily_data['created_date'] = date

        # 存入数据库
        # 更新数据前清空表，防止修改表结构
        # sql_truncate = 'TRUNCATE `' + table_pro_stock_basic + '`'
        # engine.execute(sql_truncate)
        daily_data.to_sql(table_pro_daily, engine, if_exists='append', index=False) ## replace/append

    else:
        print(date + desc + '数据已经存在')

    print(('获取 '+desc+' {} 完成') .format(date))

    # return all_stock
    return True

date = None
if len(sys.argv) == 2:
    script,date = sys.argv
    print(script)
    print(date)

# 获取基础信息数据
daily(date=date)