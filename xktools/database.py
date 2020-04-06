# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 8:49
# @Author  : davidxiaocn
# @Email   : davidxiaocn@qq.com
"""
SQLite 更新语法
UPDATE table1 SET col2 = (select col2 from table2 where table2.col1=table1.col1 limit 1)
where exists(select * from table2 where table2.col1=table1.col1);

update product set stock=(select stock from left where left.product_id=product.product_id)
where product_id in (select product_id from left)
"""
from pandas import DataFrame
import pymysql
import sqlite3
import os
import configparser

"""
对象的层级
DataBase，数据的基础类
    SQLite
    MySQL
"""


class DataBase(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.db_kind = ""
        self.file_name = ""
        self.sheet_name = ""

    def execute(self, sql):
        self.cursor.execute(sql)
        count = self.cursor.rowcount
        self.conn.commit()
        return count

    def fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def sql_to_excel(self, sql, file_name, sheet_name):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        DataFrame(result).to_excel(file_name, sheet_name)


class SQLite(DataBase):
    def __init__(self, db_name=":memory:"):
        super(SQLite, self).__init__(db_name)
        self.db_name = db_name
        self.db_kind = "SQLite"
        
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


class Config(object):
    """
    # Config().get_content("user_information")  配置文件里面的参数
    ------- dbMysqlConfig.cnf  -------
    [dbMysql]
    host = 192.168.1.180
    port = 3306
    user =
    password =
    --------
    """

    def __init__(self, config_filename="D:/python/__dbMysqlConfig.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class MySQL(DataBase):
    """
    MySQL数据库，数据库的配置文件 ： config_filename="D:/python/__dbMysqlConfig.cnf"
    """

    def __init__(self, db_name=""):
        super(MySQL, self).__init__(db_name)
        self.db_kind = "MySQL"
        conf_name = "dbMysql"
        self.conf = Config().get_content(conf_name)
        self.db_host = self.conf["host"]
        self.db_port = int(self.conf["port"])
        self.user = self.conf["user"]
        self.password = str(self.conf["password"])
        self.db_name = self.conf["db_name"]
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self.conn = pymysql.connect(host=self.db_host, port=self.db_port, user=self.user, passwd=self.password,
                                    db=self.db_name, charset='utf8')
        self.cursor = self.conn.cursor()
