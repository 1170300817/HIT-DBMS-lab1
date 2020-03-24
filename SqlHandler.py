import pymysql
import time


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
 
        sql = ("select * from film where director in" 
                "(select dir_id from director where firstName = '{}' and secondName = '{}');".format(first_name, second_name)
        )

        result = self.select(sql)
        return result

    # 根据演员查电影
    def getFilmbyActor(self, name):
        nameString = name.split(" ")
        first_name = nameString[0]
        second_name = nameString[1]
        sql = ("select * from film where film_id in" 
               " (select film_id from act where actor_id in " 
               "(select actor_id from actor where firstName = '{}' and secondName = '{}'));".format(first_name, second_name) 
        )
        result = self.select(sql)
        return result
    #
    # # 根据年份查电影 ,!!!!!等待完成
    def getFilmbyTime(self, name):
        pass
    
    # 根据名字查电影
    def getFilmbyName(self, name):
        sql = "select * from film where title = '%s';" % (name)
        result = self.select(sql)
        return result
    
    #按照喜好推荐用户喜欢的，但是还没有看过的电影
    #作为用户，当用户登陆时，应该将用户的个人信息或者其主键(用户的ID)保存到类的.self中，user指的是用户的主键ID 
    def getFavorFilms(self, user_id):
        
        favorType =  "select favorType from user where user_id = {}".format(user_id) #获取他喜欢的类型
        evenWatch =  "select film_id from watch where user_id = {}".format(user_id) #看过的电影
        sql =  "select * from film where type in ({}) and not exists ({} and film.film_id = watch.film_id);".format(favorType, evenWatch)
        result = self.select(sql)
        return result

    #根据评论的个数推荐评论最多的电影，limit表示显示前几个(默认10个)
    def getMostFavorFilm(self, limit=10):
        #根据电影序号分类数数即可
        sql = "select film_id from review group by film_id order by count(*) desc, film_id  limit {}".format(limit)
        #查找相应film_id的电影信息
        #limit 不能在子查询中进行但可以在派生中出现，真的垃圾
        sql = "select * from film natural join ({}) as f;".format(sql)
        result = self.select(sql)
        return result
    
    #根据打分排序推荐，score是分数阈值，可通过score筛选多少分数以上的电影
    def getMostRankingFilm(self, limit=10, score=0):
        #这个挺好理解的
        sql = ("select * from film natural join "
               "(select film_id from review group by film_id "
               "having avg(ranked) >= {} order by avg(ranked) desc limit {}) as f;".format(score, limit) 
        )
        result = self.select(sql)
        return result
    
    #返回其他用户推荐给他的电影
    def getRecommedFilm(self, user):
        #按照推荐表直接返回即可
        sql = ("select * from film where film_id in" 
               "(select distinct film_id from recommend where recommended_id = {}) order by film_id;".format(user)
        )
        result = self.select(sql)
        return result
    
    #写评论，解决两个用户自定义完整性：1.不可重复评价 2.只有看过一个电影之后才能评价
    def writeReview(self, film, user, text, rank=10, force=False):
        #首先你要先看过这个电影，才能评价
        check = "select film_id from watch where film_id = {} and user_id = {};".format(film, user)
        check = self.select(check)
        if len(check) == 0:
            print("请先看过这个电影后再来评价")
            return False
        #再看一下是否满足实体完整性约束
        check = "select film_id from review where film_id = {} and user_id = {};".format(film, user)
        check = self.select(check)
        #如果重复，报错推出，提示用户重新进行
        if len(check) != 0:
            if force == False:
                print("重复评价同一个电影，如果想重新评价，请删除之前的评价再试")
                return False
            else:
                delete = "delete from review where film_id = {} and user_id = {};".format(film, user)
                self.insert_delete(delete)
        timing = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = ("insert into review values ({}, {}, '{}', {}, '{}');".format(film, user, text, rank, timing))
        self.insert_delete(sql)
        print("成功加入您的评价，谢谢")
        return True
    
    #删除自己写的评论
    def deleteReview(self, film, user):
        #先看看你写了没就想删除
        check = "select film_id from review where film_id = {} and user_id = {};".format(film, user)
        check = self.select(check)
        if len(check) != 0:
            sql = "delete from review where film_id = {} and user_id = {};".format(film, user)
            self.insert_delete(sql)
            print("删除成功！")
            return True
        print("没有查询到您的评价记录")
        return False
    
    #给其他用户推荐电影
    def recommendFilm(self, referee, recommend, film):
        #检查被推荐用户是否存在
        check = "select * from recommend where recommended_id = {};".format(recommend)
        check = self.select(check)
        #检查时候重复推荐
        if len(check) == 0:
            print("无此用户，请检查后重试")
            return False
        check = "select film_id from recommend where referee_id = {} and recommended_id = {} and film_id = {};".format(referee, recommend, film)
        check = self.select(check)
        #如果重复，报错推出，提示用户重新进行
        if len(check) != 0:
            print("重复给同一个用户推荐同一个电影,请检查后重试")
            return False
        sql = ("insert into recommend values ({}, {}, {});".format(referee, recommend, film))
        self.insert_delete(sql)
        print("成功给对方分享您的推荐，谢谢")
        return True
    
    #删除自己的推荐
    def deleteRecommend(self, referee, recommend, film):
        #先看看你写了没就想删除
        check = "select film_id from recommend where referee_id = {} and recommended_id = {} and film_id = {};".format(referee, recommend, film)
        check = self.select(check)
        if len(check) != 0:
            sql = "delete from recommend where referee_id = {} and recommended_id = {} and film_id = {};".format(referee, recommend, film)
            self.insert_delete(sql)
            print("删除成功！")
            return True
        print("没有查询到您的推荐记录")
        return False
    
    #根据命令提供查询，返回元组所有信息
    def select(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("ERROR: Can not return fetch")
            self.db.rollback() #如果出现问题，回滚
            #应该增加错误处理
            pass
            return False
        results = self.cursor.fetchall()
        return results
    
    #根据命令增删元组
    def insert_delete(self, sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            print("ERROR: Can not do this option")
            self.db.rollback()
            return False
    
    def update(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 发生错误时回滚
            print("ERROR: Can not do this option")
            self.db.rollback()
            return False
        
    #创建视图
    def create_view(self, create_view_words):
        try:
            # 执行SQL语句
            self.cursor.execute(create_view_words)
            # 提交修改
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

if __name__ == '__main__':
    handler = SqlHandler("user")
#    result = handler.getFilmbyDirector("HENRY BERRY")
    
#    result = handler.getFilmbyActor('PARKER GOLDBERG')
#    result = handler.getFilmbyName("BEETHOVEN EXORCIST")
#    result = handler.getFavorFilms("3")
#    result = handler.getMostFavorFilm(4)
#    result = handler.getMostRankingFilm(30, 9)
#    result = handler.getRecommedFilm(1)
#    result = handler.writeReview(1, 15, 'A Epic Panorama of a Mad Scientist And a Monkey who must Redeem a Secret Agent in Berlin', 9, False)
#    result = handler.deleteReview(1, 41)
    result = handler.deleteRecommend(6, 1, 149)
#    for item in result:
#        print(item)
    
    
    