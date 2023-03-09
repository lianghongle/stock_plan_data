import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from common.db import Mysql
from common.MyTushare import MyTushare as mts
import config.tables as conf_talbes
import config.config as conf
from sqlalchemy import text


def stock_basics(date=None, cache_file=False, debug=False):
    # 如果没有传日期，默认取当前日期
    if date is None:
        # date = datetime.now().strftime("%Y%m%d")
        date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        date_ts = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date_ts = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

    print('获取所有股票基本数据 ' + date)

    # 要存储股票信息的表名
    table_stock_basic = conf_talbes.PRO_STOCK_BASIC

    engine = Mysql.conn()
    with engine.connect() as conn:

        # 是否交易日
        if mts.is_trade_cal(exchange='', date=date) == False:
            print('非交易日')
            return False

        # 检查表是否存在
        check_table_sql = "show tables like '{}'".format(table_stock_basic)
        check_table_result = conn.execute(text(check_table_sql))
        print(check_table_result)


        # 检查表是否存在数据
        check = None
        if check_table_result != None:
            check_table_data_sql = "SELECT * FROM {} where `symbol` = '000001' and `created_date` = '{}'".format(
                table_stock_basic,
                date)
            check = conn.execute(text(check_table_data_sql)).fetchone()

        if check is None:
            # 所有股票基本数据的文件,可以临时保存文件
            tmp_file_all_stock_path = conf.CACHE_FILE_PATH + '/stock_basics'
            if not os.path.exists(tmp_file_all_stock_path):
                os.makedirs(tmp_file_all_stock_path)

            tmp_file_all_stock = tmp_file_all_stock_path + '/' + date + '.csv'

            tmpFileCheck = os.path.isfile(tmp_file_all_stock)
            if tmpFileCheck:
                # 从文件读取所有股票基本数据
                print('从文件读取所有股票基本数据')
                all_stock = pd.read_csv(tmp_file_all_stock, dtype={
                    'ts_code': np.str_,
                    'symbol': np.str_,
                    'totalAssets': np.str_
                }).sort_values(
                    by='ts_code')
                # print(all_stock.sort_values(by=['code']))
            else:
                # 从API获取所有股票基本数据
                print('从API获取所有股票基本数据')

                try:
                    # http://file.tushare.org/tsdata/201904/all20190401.csv
                    # http://file.tushare.org/tsdata/201904/all20190401.csv
                    # all_stock = mts.getTs().get_stock_basics(date_ts)
                    all_fields = 'ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs'
                    all_stock = mts.getPro().stock_basic(fields=all_fields)
                except Exception as e:
                    print(date_ts)
                    print(e)

                    return False

                all_stock = all_stock.reset_index().sort_values('ts_code')
                all_stock.drop(["index"], axis=1, inplace=True)
                all_stock.to_csv(tmp_file_all_stock, index=False)

            all_stock['created_date'] = date

            all_stock.to_sql(table_stock_basic, conn, if_exists='append', index=False)  ## replace/append

            conn.commit()
        else:
            print(date + '数据已经存在')

    print('获取所有股票基本数据 {} 完成'.format(date))

    # return all_stock
    return True


date = None
if len(sys.argv) == 2:
    script, date = sys.argv
    print(script)
    print(date)

# stock_basics(date='20190328')
stock_basics(date=date)
