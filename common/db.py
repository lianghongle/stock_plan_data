from sqlalchemy import create_engine
import config.mysql as mysql_setting

import pymysql
pymysql.install_as_MySQLdb()

class Mysql(object):

    db_pool = {}

    @classmethod
    def config(cls, db=None):

        if db is None:
            db = 'default'

        mysql_conf = mysql_setting.config

        # "mysql://scott:tiger@hostname:3306/dbname?charset=charset"
        conf_url = "mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset={CHARSET}"

        conf_url = conf_url.format(**mysql_conf)

        return conf_url


    @classmethod
    def conn(cls, db=None):
        if db in cls.db_pool.keys():
            engine = cls.db_pool[db]
        else:
            engine = create_engine(cls.config(db))
            cls.db_pool[db] = engine

        return engine
