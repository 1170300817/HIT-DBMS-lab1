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
        try:
            self.db = pymysql.connect(host='localhost',user='root',password="920618",port=3306,db='lab1',charset='utf8')
        # 使用cursor()方法获取操作游标
        except:
            self.db = None
        if(self.db == None):
            return
        self.cursor = self.db.cursor()
    # 根据导演查电影
    def getFilmbyDirector(self, name):
        #获得姓名
        nameString = name.split(" ")
        first_name = nameString[0] 
        second_name = nameString[1]
        
        
        sql1 = ("select * from film where director in" 
                "(select dir_id from director where firstName = '{}' and secondName = '{}');".format(first_name, second_name)
        )
#        # 查导演号码
#        sql1 = "select * from director where firstName = '%s' and secondName='%s';" % (first_name, second_name)
#        self.cursor.execute(sql1)
#        results = self.cursor.fetchall()
#        dir_num = results[0][0]
#
#        # 再根据号码查电影
#        sql2 = "select * from film where director = '%s';" % dir_num
        try:
            self.cursor.execute(sql1)
            self.db.commit()
        except:
            print("ERROR: Can not return fetch")
            self.db.rollback()
            #应该增加错误处理
            pass
            return None
        results = self.cursor.fetchall()
        return results

    # 根据演员查电影
    def getFilmbyActor(self, name):
        nameString = name.split(" ")
        first_name = nameString[0]
        second_name = nameString[1]
#        # 查演员号码
#        sql1 = "select * from actor where firstName = '%s' and secondName='%s';" % (first_name, second_name)
#        self.cursor.execute(sql1)
#        results = self.cursor.fetchall()
#        actor_num = results[0][0]
#        # 再根据演员号码查所有电影
#        sql2 = "select * from film where film_id in (select film_id from act where actor_id = '%s');" % (actor_num)
        
        sql = ("select * from film where film_id in" 
               " (select film_id from act where actor_id in " 
               "(select actor_id from actor where firstName = '{}' and secondName = '{}'));".format(first_name, second_name) 
        )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("ERROR: Can not return fetch")
            self.db.rollback() #如果出现问题，回滚
            #应该增加错误处理
            pass
            return None
        results = self.cursor.fetchall()
        return results
    #
    # # 根据年份查电影
    # def getFilmbyActor(self, name):
    # 根据名字查电影
    def getFilmbyName(self, name):
        sql1 = "select * from film where title = '%s';" % (name)
        try:
            self.cursor.execute(sql1)
            self.db.commit()
        except:
            print("ERROR: Can not return fetch")
            self.db.rollback() #如果出现问题，回滚
            #应该增加错误处理
            pass
            return None
        results = self.cursor.fetchall()
        return results




if __name__ == '__main__':
    handler = SqlHandler("user")
#    result = handler.getFilmbyDirector("GARY PHOENIX")
    
#    result = handler.getFilmbyActor('PARKER GOLDBERG')
    result = handler.getFilmbyName("BEETHOVEN EXORCIST")
    for item in result:
        print(item)
    
    
    