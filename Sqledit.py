import sqlite3
import os
from datetime import datetime
import json
from nonebot.log import logger
DB_DIR = os.path.dirname(__file__)

def time_format() :
    return datetime.now().strftime("%Y-%m-%d")

def is_sqlite3_exists(DIR):
    # SQL路径
    db_path = os.path.join(DIR, "CatBoxPro.db")
    # 连接
    conn = sqlite3.connect(db_path)
    # 开始事务
    c = conn.cursor()
    # 签到数据表
    c.execute('SELECT count(*) FROM sqlite_master WHERE "type"="table" AND "name" = "DefaultData"')
    result = c.fetchone()
    if result[0] == 0:
        c.execute("Create Table 'DefaultData' ('CID' Integer Primary Key Autoincrement,'Group' Varchar(4000),'QQ' Varchar(4000),'猫粮' Varchar(4000),'鱼干' Varchar(4000),'Hex' Varchar(4000),'月签' Varchar(4000),'累计' Varchar(4000),'最后签到' Varchar(4000),'备注' Varchar(4000),'Bin' Varchar(4000));")
    # 签到表
    c.execute('SELECT count(*) FROM sqlite_master WHERE "type"="table" AND "name" = "签到数据表"')
    result = c.fetchone()
    if result[0] == 0:
        c.execute("Create Table '签到数据表' ('UUID' Integer Primary Key Autoincrement,'Group' Varchar(4000),'QQ' Varchar(4000),'时间' Varchar(4000),'附加时间' Varchar(4000));")
    # 提交事务
    conn.commit()
    # 关闭
    conn.close()



# Sql.取本群排名
def get_group_count(group_id):  # {time_format()}
    SqlCommand = f"Select * From '签到数据表' Where [Group]='{group_id}' And [时间]='{time_format()}'"
    cursor = sql.cursor()  # 开始事务
    cursor.execute(SqlCommand)  # 执行Sql命令
    records = cursor.fetchall()  # 取所有记录
    if not records:
        return '1'
    else:
        # 取数组成员数
        return str(len(records))

# Sql_更新数据
def Sql_UPDATA(group_id, user_id, row):
    SqlCommand = f"Update 'DefaultData' Set [猫粮]='{row[3]}',[鱼干]='{row[4]}',[Hex]='{row[5]}',[月签]='{row[6]}',[累计]='{row[7]}',[最后签到]=DateTime(CURRENT_TIMESTAMP,'localtime') Where [Group]='{group_id}' And [QQ]='{user_id}'"
    c = sql.cursor()
    c.execute(SqlCommand)
    sql.commit()

# Sql_新数据
def Sql_New(group_id, user_id, Data):
    SqlCommand = f"Insert Into 'DefaultData' ([Group],[QQ],[猫粮],[鱼干],[Hex],[月签],[累计],[最后签到])Values('{group_id}', '{user_id}', '{Data[3]}', '{Data[4]}', '{Data[5]}','1','1',DateTime(CURRENT_TIMESTAMP,'localtime'))"
    c = sql.cursor()
    c.execute(SqlCommand)
    sql.commit()

# 签到表新增 <群号><触发QQ>
def add_signinfrom_data(group_id, user_id):
    SqlCommand = f"Insert Into '签到数据表' ([GROUP],[QQ],[时间],[附加时间]) Values ('{group_id}','{user_id}','{datetime.now().strftime('%Y-%m-%d')}',DateTime(CURRENT_TIMESTAMP,'localtime'))"
    c = sql.cursor()  # 开始事务
    c.execute(SqlCommand)
    sql.commit()  # 提交事务

# sql 取已签到的日期 成功返回整数型列表
def sql_command(group_id, user_id) -> list:
    today = datetime.now()
    first_day_of_month = today.replace(day=1).date()
    next_month = today.replace(month=today.month + 1).replace(day=1).date()
    Command = f"SELECT DISTINCT 时间 FROM '签到数据表' WHERE [时间]>='{first_day_of_month}' AND [时间]<='{next_month}' AND [QQ]='{user_id}' AND [Group]='{group_id}'"
    cursor = sql.cursor()  # 开始事务
    cursor.execute(Command)  # 执行Sql命令
    records = cursor.fetchall()  # 取所有记录
    list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 数组从0开始
    if records:
        for date_str, in records:
            year, month, day = date_str.split('-')
            list[int(day)-1] = int(day)
    return list

# Sql.查询信息<群号><QQ> 成功返回数组数据
def DefaultData(group_id, user_id):
    """
    row[0]  # 唯一编号
    row[1]  # 群
    row[2]  # QQ
    row[3]  # 猫粮
    row[4]  # 鱼干
    row[5]  # 幸运色HEX
    row[6]  # 月签
    row[7]  # 累计
    row[8]  # 最后签到
    """
    SqlCommand = f"Select * From 'DefaultData' Where [Group]='{group_id}' And [QQ]='{user_id}'"
    c = sql.cursor()
    cursor = c.execute(SqlCommand)
    for row in cursor:
        if row:
            return row[:8]
        else:
            return None

#排行榜取数据 成功返回json字符串
def mlb_Group_Data(group_id:int) -> str:
    SqlCommand = f"Select Distinct [QQ],[猫粮],[累计] From 'DefaultData' Where [Group]='{group_id}' Order By Cast([猫粮] as Numeric) Desc Limit 20"
    c = sql.cursor()
    cursor = c.execute(SqlCommand)
    result = []
    i = 0
    for row in cursor:
        if i == 10: break
        user_id = row[0]
        ml = row[1]
        lj = row[2]
        result.append({"user_id":user_id,"ml":ml,"lj":lj})
        i += 1
    text = json.dumps(result)
    if text == '[]':return None
    return text

is_sqlite3_exists(DB_DIR)
sql = sqlite3.connect(os.path.join(DB_DIR, "CatBoxPro.db"))
logger.info("签到数据库初始化完成")




if __name__ == '__main__':
    print(DefaultData('1075718428','2033689024'))