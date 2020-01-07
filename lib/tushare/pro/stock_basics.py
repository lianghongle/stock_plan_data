import os
from datetime import datetime

import pandas as pd
import numpy as np

from common.db import Mysql
from common.MyTushare import MyTushare as mts

import config.tables as conf_talbes
import config.config as conf


# date demo 20190328
from common.func import get_date


def stock_basics(date=None, cache_file=False, debug=False):

    date = get_date(date)

    print('获取所有股票基本数据 ' + date + ' 开始')

    # 要存储股票信息的表名
    table_pro_stock_basic = conf_talbes.PRO_STOCK_BASIC

    engine = Mysql.conn()

    # 是否交易日
    if not mts.is_trade_cal(exchange='', date=date):
        print('非交易日')
        return False

    # 检查表是否存在
    check_table_sql = "show tables like '{}'".format(table_pro_stock_basic)
    check_table_result = engine.execute(check_table_sql).scalar()

    # 检查表是否存在数据
    check = None
    if check_table_result is not None:
        check_table_data_sql = "SELECT * FROM {} where `symbol` = '000001' and `created_date` = '{}'".format(
            table_pro_stock_basic,
            date)
        check = engine.execute(check_table_data_sql).fetchone()

    if check is None:
        # 所有股票基本数据的文件,可以临时保存文件
        tmp_file_all_stock_path = conf.CACHE_FILE_PATH + '/pro/stock_basics'
        if not os.path.exists(tmp_file_all_stock_path):
            os.makedirs(tmp_file_all_stock_path)

        tmp_file_all_stock = tmp_file_all_stock_path + '/' + date + '.csv'

        tmpFileCheck = os.path.isfile(tmp_file_all_stock)
        if tmpFileCheck:
            # 从文件读取所有股票基本数据
            print('从文件读取所有股票基本数据')
            all_stock = pd.read_csv(tmp_file_all_stock, dtype={'symbol': np.str_, 'totalAssets': np.str_}).sort_values(
                by='symbol')
            # print(all_stock.sort_values(by=['code']))
        else:
            # 从API获取所有股票基本数据
            print('从API获取所有股票基本数据')

            try:
                fields = 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs'
                all_stock = mts.getPro().stock_basic(date=date, fields=fields)
            except Exception as e:
                print(date)
                print(e)

                return False

            all_stock = all_stock.sort_values('symbol')
            all_stock.to_csv(tmp_file_all_stock, index=False)

        all_stock['created_date'] = date

        # 存入数据库
        # 更新数据前清空表，防止修改表结构
        sql_truncate = 'TRUNCATE `' + table_pro_stock_basic + '`'
        engine.execute(sql_truncate)
        all_stock.to_sql(table_pro_stock_basic, engine, if_exists='append', index=False)  ## replace/append

        # 所在地域处理
        table_pro_stock_area = conf_talbes.PRO_STOCK_AREA
        area = all_stock.drop_duplicates(['area'])
        area = area.loc[:, ['area', 'created_date']]
        area_truncate = 'TRUNCATE `' + table_pro_stock_area + '`'
        engine.execute(area_truncate)
        area.to_sql(table_pro_stock_area, engine, if_exists='append', index=False)

        # 所属行业处理
        table_pro_stock_industry = conf_talbes.PRO_STOCK_INDUSTRY
        industry = all_stock.drop_duplicates(['industry'])
        industry = industry.loc[:, ['industry', 'created_date']]
        industry_truncate = 'TRUNCATE `' + table_pro_stock_industry + '`'
        engine.execute(industry_truncate)
        industry.to_sql(table_pro_stock_industry, engine, if_exists='append', index=False)

    else:
        print(date + '数据已经存在')

    print('获取所有股票基本数据 {} 完成'.format(date))

    # return all_stock
    return True
