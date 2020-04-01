import pymysql
import time 
import traceback

#喜欢类型的枚举
favorList = ['comedy', 'tragedy', 'literary', 'detective', 'sciencefiction', 'action', 'thriller', 'romance']

class SqlHandler:
    def __init__(self, userType=None):
        # 打开数据库连接
        try:
             self.db = pymysql.connect(host='localhost', user='root', password="920618", port=3306, db='lab1',
                                       charset='utf8')
#            self.db = pymysql.connect("localhost", "root", "lin02200059", "lab1")
             self.userType = userType
        except:
            self.db = None
        if (self.db == None):
            return
        self.cursor = self.db.cursor()
    
    def __call__(self, userType):
        self.userType = userType
    
    ###################################
    #
    #
    #User 权限
    #
    #
    ###################################
    
    # 根据导演查电影
    def getFilmbyDirector(self, name):
        # 获得姓名
        nameString = name.split(" ")
        first_name = nameString[0]
        second_name = nameString[1]

        sql = "select * from user_dir_view where firstName = '{}' and secondName = '{}';".format(first_name, second_name)
        
        result = self.select(sql)
        return True, result

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
        return True, result
    

    # 根据名字查电影
    def getFilmbyName(self, name):
        sql = "select * from film where title = '%s';" % (name)
        result = self.select(sql)
        return True, result

    
    #根据电影查导演
    def getDirectbyfilm(self, dir_id):
        sql = "select * from director where dir_id = {};".format(dir_id)
        result = self.select(sql)
        return True, result       

    # 按照喜好推荐用户喜欢的，但是还没有看过的电影
    # 作为用户，当用户登陆时，应该将用户的个人信息或者其主键(用户的ID)保存到类的.self中，user指的是用户的主键ID
    def getFavorFilms(self, user_id):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        favorType = "select favorType from user where user_id = {}".format(user_id)  # 获取他喜欢的类型
        evenWatch = "select film_id from watch where user_id = {}".format(user_id)  # 看过的电影
        sql = "select * from film where type in ({}) and not exists ({} and film.film_id = watch.film_id);".format(
            favorType, evenWatch)
        result = self.select(sql)
        return True, result

    # 根据评论的个数推荐评论最多的电影，limit表示显示前几个(默认10个)
    def getMostFavorFilm(self, limit=10):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 根据电影序号分类数数即可
        sql = "select film_id from review group by film_id order by count(*) desc, film_id  limit {}".format(limit)
        # 查找相应film_id的电影信息
        # limit 不能在子查询中进行但可以在派生中出现，真的垃圾
        sql = "select * from film natural join ({}) as f;".format(sql)
        result = self.select(sql)
        return True, result

    # 根据打分排序推荐，score是分数阈值，可通过score筛选多少分数以上的电影
    def getMostRankingFilm(self, limit=10, score=0):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 这个挺好理解的
        sql = ("select * from film natural join "
               "(select film_id from review group by film_id "
               "having avg(ranked) >= {} order by avg(ranked) desc, film_id limit {}) as f;".format(score, limit)
               )
        result = self.select(sql)
        return True, result

    # 返回其他用户推荐给他的电影
    def getRecommedFilm(self, user):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 按照推荐表直接返回即可
        sql = ("select * from film where film_id in"
               "(select distinct film_id from recommend where recommended_id = {}) order by film_id;".format(user)
               )
        result = self.select(sql)
        return True, result

    # 写评论，解决两个用户自定义完整性：1.不可重复评价 2.只有看过一个电影之后才能评价
    def writeReview(self, film, user, text, rank=10, force=False):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 首先你要先看过这个电影，才能评价
        check = "select film_id from watch where film_id = {} and user_id = {};".format(film, user)
        check = self.select(check)
        if len(check) == 0:
            print("请先看过这个电影后再来评价")
            return False, "请先看过这个电影后再来评价"
        # 再看一下是否满足实体完整性约束
        check = "select film_id from review where film_id = {} and user_id = {};".format(film, user)
        check = self.select(check)
        # 如果重复，报错推出，提示用户重新进行
        if len(check) != 0:
            if force == False:
                print("重复评价同一个电影，如果想重新评价，请删除之前的评价再试")
                return False, "重复评价同一个电影，如果想重新评价，请删除之前的评价再试"
            else:
                delete = "delete from review where film_id = {} and user_id = {};".format(film, user)
                self.insert_delete(delete)
        timing = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql = ("insert into review values ({}, {}, '{}', {}, '{}');".format(film, user, text, rank, timing))
        self.insert_delete(sql)
        print("成功加入您的评价，谢谢")
        return True, "成功加入您的评价，谢谢"

    # 删除自己写的评论
    def deleteReview(self, film, user):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 先看看你写了没就想删除
        check = "select film_id from review where film_id = {} and user_id = {};".format(film, user)
        check = self.select(check)
        if len(check) != 0:
            sql = "delete from review where film_id = {} and user_id = {};".format(film, user)
            self.insert_delete(sql)
            print("删除成功！")
            return True, "删除成功！"
        print("没有查询到您的评价记录")
        return False, "没有查询到您的评价记录"

    # 给其他用户推荐电影
    def recommendFilm(self, referee, recommend, film):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 检查被推荐用户是否存在
        check = "select * from user where userName = '{}';".format(recommend)
        check = self.select(check)
        # 检查时候重复推荐
        if len(check) == 0:
            print("无此用户，请检查后重试")
            return False, "无此用户，请检查后重试"
        check = "select film_id from recommend where referee_id = {} and exists (select * from user where userName = '{}' and recommended_id = user_id)  and film_id = {};".format(
            referee, recommend, film)
        check = self.select(check)
        # 如果重复，报错推出，提示用户重新进行
        if len(check) != 0:
            print("重复给同一个用户推荐同一个电影,请检查后重试")
            return False, "重复给同一个用户推荐同一个电影,请检查后重试"
        sql = "select user_id from user where userName = '{}';".format(recommend)
        ret = self.select(sql)
        recommend = ret[0][0]
        sql = ("insert into recommend values ({}, {}, {});".format(referee, recommend, film))
        self.insert_delete(sql)
        print("成功给对方分享您的推荐，谢谢")
        return True, "成功给对方分享您的推荐，谢谢"

    # 删除自己的推荐
    def deleteRecommend(self, referee, recommend, film):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        # 先看看你写了没就想删除
        check = ("select film_id from recommend where referee_id = {} and " 
                "recommended_id in (select user_id from user where userName = '{}') and film_id = {};".format(referee, recommend, film))
        check = self.select(check)
        if len(check) != 0:
            sql = ("delete from recommend where referee_id = {} and " 
                   "recommended_id in (select user_id from user where userName = '{}') and film_id = {};".format(referee, recommend, film))
            self.insert_delete(sql)
            print("删除成功！")
            return True, "删除成功！"
        print("没有查询到您的推荐记录")
        return False, "没有查询到您的推荐记录"
    
    #更新自己的喜欢类型
    def updateFavor(self, user, favor):
        if self.userType != "USER":
            print("非用户，无权限访问")
            return False, "非用户，无权限访问"
        check = "select * from user where user_id = {};".format(user)
        check = self.select(check)
        # 检查是否没有此用户
        if len(check) == 0:
            print("无此用户，请检查后重试")
            return False, "无此用户，请检查后重试"
        #检查喜欢的类型是否在用户自定义完整性约束中
        if favor not in favorList:
            print("请输入正确的电影类型")
            return False, "请输入正确的电影类型"
        sql = "update user set favorType = '{}' where user_id = {}".format(favor, user)
        self.update(sql)
        print("更新类型成功")
        return True, "更新类型成功"
    
    #更新自己看过的电影
    def watchFilm(self, user, film):
        sql = "select * from watch where film_id = {} and user_id = {};".format(film, user)
        ret = self.select(sql)
        if len(ret) != 0:
            return False, "已经看过此电影了"
        sql = "insert into watch values ({}, {})".format(user, film)
        self.insert_delete(sql)
        return True, "更新已看电影完成"
    
    #查用户ID
    def getuser(self, name):
        sql = "select user_id from user where userName = '{}'".format(name)
        result = self.select(sql)
        return True, result
    
    
    ###################################
    #
    #
    #MANAGER 权限
    #
    #
    ###################################
    
    # 新增Act记录
    def newAct(self, actorname, filmname):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False
        nameString = actorname.split(" ")
        actfirst = nameString[0]
        actsecond = nameString[1]

        # 检查演员和电影是否存在，是否有重复元组
        check1 = "select actor_id from actor where firstName = '{}' and secondName = '{}';".format(actfirst, actsecond)
        ret1 = self.select(check1)
        check2 = "select film_id from film where title = '{}';".format(filmname)
        ret2 = self.select(check2)
        
        if len(ret1) == 0:
            self.newActor(actfirst, actsecond)
            ret1 = self.select(check1)

        if len(ret2) == 0:
            print("无此电影，请检查后重试")
            return False
        
        actor_id = ret1[0][0]
        film_id = ret2[0][0]
        sql = ("insert into act values ({}, {});".format(actor_id, film_id))
        self.insert_delete(sql)
        print("成功插入，谢谢")
        return True

    # 删除Act记录 1
    def deleteAct(self, film_id):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False

        sql = "delete from act where film_id = {};".format(film_id)
        self.insert_delete(sql)
        print("成功删除，谢谢")
        sql = "delete from actor where actor_id not in (select distinct actor_id from act);"
        self.insert_delete(sql)
        return True

    # 新增Actor记录
    def newActor(self, first_name, second_name):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False
        sql = ("insert into actor (firstName , secondName) values ('{}', '{}');".format(first_name, second_name))
        self.insert_delete(sql)
        print("成功插入新演员，谢谢")
        return True


    # 新增director记录 1
    def newDirector(self, first_name, second_name):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False
        sql = ("insert into director (firstName, secondName) values ('{}', '{}');".format(first_name, second_name))
        self.insert_delete(sql)
        print("成功插入新导演，谢谢")
        return True

    # 删除director记录 1
    def deleteDirector(self, dir_id):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False
        # 检查要删去的导演是否存在
        check = "select * from director where dir_id = {};".format(dir_id)
        check = self.select(check)

        if len(check) == 0:
            print("无此导演，请检查后重试")
            return False

        sql = "delete from director where dir_id = {};".format(dir_id)
        self.insert_delete(sql)
        print("成功删除导演，谢谢")
        return True

    # 新增film记录 1
    def newFilm(self, title, type, first, second):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False
        sql = "select * from manager_film_view where firstName = '{}' and secondName = '{}';".format(first, second)
        ret = self.select(sql)
        if len(ret) == 0:
            print("还未有此导演")
            self.newDirector(first, second)
        #查这个人的号码
        sql = "select dir_id from director where firstName = '{}' and secondName = '{}';".format(first, second)
        ret = self.select(sql)
        director_id = ret[0][0]
        timing = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        sql = ("insert into film (title, type, director,time) values ('{}','{}', {},'{}');".format(title, type, director_id, timing))
        self.insert_delete(sql)
        print("成功插入，谢谢")
        return True

    # 删除film记录
    def deleteFilm(self, film):
        if self.userType != "MANAGER":
            print("非管理员，无权限访问")
            return False
        #检查有无此电影
        check = "select film_id, director from film where title = '{}';".format(film)
        check = self.select(check)

        if len(check) == 0:
            print("无此电影，请检查后重试")
            return False
        #如果有此电影，那么将导演和电影编号记录下来
        director = check[0][1]
        film_id = check[0][0]
        #删除电影
        sql = "delete from film where film_id = {};".format(film_id)
        self.insert_delete(sql)
        print("成功删除，谢谢")
        #如果这个电影删除了，要检查他的导演是不是也没了
        sql = "select * from film where director = {};".format(director)
        ret = self.select(sql)
        if len(ret) == 0:
            self.deleteDirector(director)
        self.deleteAct(film_id)
        
        return True

    ###################################
    #
    #
    #DBA 权限
    #
    #
    ###################################

    #查询user记录，登陆用
    def login(self, userName, password):
        sql = "select * from DBA_user_view where userName = '{}' and password = '{}';".format(userName, password)
        result = self.select(sql)
        
        if len(result) == 0:
            return False, None
        else:
            return True, result[0]
    
    # 新增user记录,要增加用户名重名判断
    def newUser(self, firstName, secondName, userName, password, favorType='null'):
        check = "select user_id from DBA_user_view where userName = '{}';".format(userName)
        check = self.select(check)
        if len(check) > 0:
            print("用户名重复，请重新修改用户名")
            return False, "用户名重复，请重新修改用户名"
        password = str(password)
        if len(password) < 6 or len(password) > 10:
            print("请规范密码长度为6 - 10字符")
            return False, "请规范密码长度为6 - 10字符"
        if len(userName) < 6:
            print("请规范用户名长度至少6字符")
            return False, "请规范用户名长度至少6字符"
        sql = (
            "insert into user (firstName,secondName,favorType,userName,password) values ('{}','{}','{}','{}','{}');".format(
                firstName, secondName, favorType, userName, password))
        self.insert_delete(sql)
        print("成功插入，谢谢")
        return True, "成功插入，谢谢"

    # 删除user记录 注销？
    def deleteUser(self, user_id):
        check = "select * from DBA_user_view where user_id = {};".format(user_id)
        check = self.select(check)

        if len(check) == 0:
            print("无此用户，请检查后重试")
            return False

        sql = "delete from DBA_user_view where user_id = {};".format(user_id)
        self.insert_delete(sql)
        print("成功删除，谢谢")
        return True
    
    #修改密码
    def changePass(self, user_id, password):
        password = str(password)
        if len(password) < 6 or len(password) > 10:
            print("请规范密码长度为6 - 10字符")
            return False
        check = "select password from DBA_user_view where user_id = {};".format(user_id)
        check = self.select(check)
        if password in check[0]:
            print("请更换您的密码，不要和旧密码重复")
            return False
        sql = "update DBA_user_view set password = '{}' where user_id = {};".format(password, user_id)
        self.update(sql)
        print("成功修改密码")
        return True
    
    ###################################
    #
    #
    #三个基本函数，USER MANAGER DBA都可使用
    #
    #
    ###################################
    # 根据命令提供查询，返回元组所有信息
    def select(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("ERROR: Can not return fetch")
            traceback.print_exc()
            self.db.rollback()  # 如果出现问题，回滚
            # 应该增加错误处理
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

