import pymysql


#
# sql = "select * from actor;"
#
# cursor.execute(sql)
# 获取所有记录列表
# results = cursor.fetchall()
# for row in results:
#     actor_id = row[0]
#     first_name = row[1]
#     last_name = row[2]
#     last_update = row[3]

# 打印结果
# print("actor_id=%s,first_name=%s,last_name=%s,last_update=%s" % \
#       (actor_id, first_name, last_name, last_update))
# except:
#     print("Error: unable to fetch data")

# 关闭数据库连接
# db.close()


class SqlHandler:
    def __init__(self, userType):
        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "lin02200059", "film")
        # 使用cursor()方法获取操作游标
        self.cursor = db.cursor()

    # 根据导演查电影
    def getFilmbyDirector(self, name):
        sql = "select * from film where director = '%s';" % name
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(results)

    # 根据演员查电影
    def getFilmbyActor(self, name):


if __name__ == '__main__':
    handler = SqlHandler("user")
    handler.getFilmbyActor("BELA")
