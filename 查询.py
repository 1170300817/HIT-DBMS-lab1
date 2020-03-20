import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "lin02200059", "sakila")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# sql = "use sakila;"
# cursor.execute(sql)


# SQL 查询语句
sql = "select * from actor;"
# try
# 执行SQL语句
cursor.execute(sql)
# 获取所有记录列表
results = cursor.fetchall()
for row in results:
    actor_id = row[0]
    first_name = row[1]
    last_name = row[2]
    last_update = row[3]

    # 打印结果
    print("actor_id=%s,first_name=%s,last_name=%s,last_update=%s" % \
          (actor_id, first_name, last_name, last_update))
# except:
#     print("Error: unable to fetch data")

# 关闭数据库连接
db.close()
