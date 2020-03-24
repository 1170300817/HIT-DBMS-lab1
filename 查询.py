import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "lin02200059", "lab1")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句

sql = "delete from act where actor_id = 50 and film_id = 512;"

cursor.execute(sql)
db.commit()
# 获取所有记录列表
results = cursor.fetchall()

# 关闭数据库连接
db.close()
