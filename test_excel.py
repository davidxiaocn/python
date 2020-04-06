# -*- coding: utf-8 -*-
# @Time    : 2020/4/4 21:36
# @Author  : davidxiaocn
# @Email   : davidxiaocn@qq.com
import xktools.excel as excel
from xktools.database import SQLite
from xktools.excel import KmWorkBook


path = 'C:\\python\\xkgraph\\'
path_data = 'C:\\python\\data\\'
db = SQLite(path_data +"Contract.db")    # 保存到文件
#db = SQLite()                         # 保存到内存


is_creat_table = 1
if is_creat_table == 1 :
    file_name = path +"学校1.xlsx"
    sheet_name = "明细"
    table_name = "km_excel_score"
    excel.excel_save_to_db(file_name, sheet_name, db, table_name, 1)

    is_creat_table = 0
    file_name =  path +"学校2.xlsx"
    sheet_name = "明细"
    table_name = "km_excel_score"
    excel.excel_save_to_db(file_name, sheet_name, db, table_name, is_creat_table, 0)


    """
    可以增加数据处理的SQL处理
    """
sql = "update  km_excel_score set 全校排名 = ID"
print("更新数据：%d" % db.execute(sql))

file_name =  path +"学校-模版.xlsx"
sheet_name = "明细"
table_name = "km_excel_score"

wb = KmWorkBook(file_name)
wb.read_to_sheet(db, table_name, sheet_name, )
sheet_name = "明细-及格"
wb.read_to_sheet(db, table_name, sheet_name, "where  加权得分>=80")

save_file_name =  path_data +"学校-" + excel.get_time_stamp() + ".xlsx"
wb.save_file(save_file_name)


