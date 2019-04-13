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

desc = '周线行情'

def weekly(date=None, cache_file=False, debug=False):
    """
    周线行情
    """
    # 如果没有传日期，默认取当前日期
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
        # date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    print('获取 ' + desc + ' ' + date)

    # 交易日期 （每周五日期，YYYYMMDD格式）
    weekday = datetime.strptime(date, "%Y%m%d").weekday()
    if weekday != 4:
        print('非周五' + date)
        return False

    # 存储 日线行情 表名
    table_pro_weekly = conf_talbes.PRO_STOCK_WEEKLY

    engine = Mysql.conn()

    # 是否交易日
    # if mts.is_trade_cal(exchange = '', date = date) == False:
    #     print('非交易日')
    #     return False

    # 检查表是否存在
    check_table_sql = "show tables like '{}'".format(table_pro_weekly)
    check_table_result = engine.execute(check_table_sql).scalar()

    # 检查表是否存在数据
    check = None
    if check_table_result != None:
        check_table_data_sql = "SELECT * FROM {} where `ts_code` = '000001.SZ' and `created_date` = '{}'".format(table_pro_weekly,
                                                                                                date)
        check = engine.execute(check_table_data_sql).fetchone()

    if check is None:
        # 可以临时保存文件
        tmp_file_stock_weekly_path = conf.CACHE_FILE_PATH + '/pro/weekly'
        if not os.path.exists(tmp_file_stock_weekly_path):
            os.makedirs(tmp_file_stock_weekly_path)

        tmp_file_weekly = tmp_file_stock_weekly_path + '/' + date + '.csv'

        tmpFileCheck = os.path.isfile(tmp_file_weekly)
        if tmpFileCheck:
            # 从文件读取所有股票基本数据
            print('从文件读取 ' + desc)
            daily_data = pd.read_csv(tmp_file_weekly, dtype={'ts_code': np.str_, 'totalAssets': np.str_}).sort_values(by='ts_code')
            # print(all_stock.sort_values(by=['code']))
        else:
            # 从API获取所有股票基本数据
            print('从API获取 ' + desc)

            try:
                weekly_data = mts.getPro().daily(trade_date=date)
            except Exception as e:
                print(date)
                print(e)

                return False

            daily_data = weekly_data.sort_values('ts_code')
            daily_data.to_csv(tmp_file_weekly, index=False)

        daily_data['created_date'] = date

        # 存入数据库
        # 更新数据前清空表，防止修改表结构
        # sql_truncate = 'TRUNCATE `' + table_pro_stock_basic + '`'
        # engine.execute(sql_truncate)
        daily_data.to_sql(table_pro_weekly, engine, if_exists='append', index=False) ## replace/append

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
weekly(date=date)