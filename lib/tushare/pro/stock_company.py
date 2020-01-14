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


def stock_company(exchange='SSE', date=None, cache_file=False, debug=False):
    # 如果没有传日期，默认取当前日期
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
        # date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    print('获取上市公司基本信息 ' + date)

    # 要存储上市公司信息的表名
    table_pro_stock_company = conf_talbes.PRO_STOCK_COMPANY

    engine = Mysql.conn()

    # 是否交易日
    if mts.is_trade_cal(exchange='', date=date) == False:
        print('非交易日')
        return False

    # 检查表是否存在
    check_table_sql = "show tables like '{}'".format(table_pro_stock_company)
    check_table_result = engine.execute(check_table_sql).scalar()

    # 检查表是否存在数据
    check = None
    if check_table_result != None:
        check_table_data_sql = "SELECT * FROM {} where `ts_code` = '000001.SZ' and `exchange` = '{}' and `created_date` = '{}'" \
            .format(table_pro_stock_company,exchange,datetime.strptime(date,"%Y%m%d").strftime("%Y-%m-%d"))
        check = engine.execute(check_table_data_sql).fetchone()

    if check is None:
        # 所有股票基本数据的文件,可以临时保存文件
        tmp_file_path = conf.CACHE_FILE_PATH + '/pro/stock_company'
        if not os.path.exists(tmp_file_path):
            os.makedirs(tmp_file_path)

        tmp_file_company = tmp_file_path + '/' + exchange + '_' + date + '.csv'

        tmpFileCheck = os.path.isfile(tmp_file_company)
        if tmpFileCheck:
            # 从文件读取上市公司信息
            print('从文件读取上市公司基本信息')
            company = pd.read_csv(tmp_file_company, dtype={'ts_code': np.str_, 'totalAssets': np.str_}).sort_values(
                by='ts_code')
            # print(all_stock.sort_values(by=['code']))
        else:
            # 从API获取上市公司基本信息
            print('从API获取上市公司基本信息')

            try:
                fields = 'ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,' \
                         'office,employees,main_business,business_scope'
                company = mts.getPro().stock_company(exchange=exchange, fields=fields)
            except Exception as e:
                print(date)
                print(e)

                return False

            company = company.sort_values('ts_code')
            company.to_csv(tmp_file_company, index=False)

        company['created_date'] = date

        # 存入数据库
        # 更新数据前清空表，防止修改表结构
        # sql_truncate = 'TRUNCATE `' + table_pro_stock_basic + '`'
        # engine.execute(sql_truncate)
        company.to_sql(table_pro_stock_company, engine, if_exists='append', index=False)  ## replace/append

    else:
        print(date + '数据已经存在')

    print('获取上市公司基本信息 {} 完成'.format(date))

    # return all_stock
    return True
