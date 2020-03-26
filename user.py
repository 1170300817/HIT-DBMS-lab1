import SqlHandler as sq
import DBA 

class User():
    
    def __init__(self):
        self.sqlHandler = sq.SqlHandler()
        self.dba = DBA.DBA()
        self.username = None
        self.password = None
        self.favorType = None
        self.firstName = None
        self.secondName = None
        self.id = None
    #UI登陆调用
    def __call__(self, username, password):
        ret = self.login(username, password)
        if ret[0] == True:
            self.userType = "USER"
        else:
            self.userType = None
        self.sqlHandler(self.userType)
        return ret
        
    #登录,如果登陆成功返回True并且更新个人数据，否则返回false
    def login(self, username, password):
        flag, info = self.dba.testLogin(username, password)
        if flag == False:
            print("用户名密码输入错误")
            return False, "用户名密码输入错误"
        else:
            self.id = info[0]
            self.firstName = info[1]
            self.secondName = info[2]
            self.favorType = info[3]
            print("登陆成功")
            return True, "登陆成功"
    
    #创建账号，如果创建成功，自动登录
    def createAccount(self, firstName, secondName, favorType, userName, password):
        ret = self.dba.createCount(firstName, secondName, favorType, userName, password)
        if ret[0] == False:
            return False, ret[1]
        else:
            self.username = userName
            self.password = password
            self.login(self.username, self.password)
            self.sqlHandler("USER")
            print("创建账户成功")
            return True, ret[1]
    
    #修改密码
    def changepass(self, password):
        ret = self.dba.changePass(self.id, password)
        if ret == True:
            print("修改密码成功")
            return True
        else:
            print("修改密码失败")
            return False
    
    def updateFavor(self, favor):
        ret = self.sqlHandler.updateFavor(self.id, favor)
        self.favorType = favor
        if ret[0] == True:
            print("更新喜好成功")
            return ret
        else:
            print("修改喜好失败")
            return ret
    
    #查询某位导演拍的电影：
    def getFilmbyDirector(self, name):
        ret = self.sqlHandler.getFilmbyDirector(name)
        return self.returnFilms(ret)
    
    #查某位演员演过的电影:
    def getFilmbyActor(self, name):
        ret = self.sqlHandler.getFilmbyActor(name)
        return self.returnFilms(ret)
    
    #根据电影名字
    def getFilmbyName(self, name):
        ret = self.sqlHandler.getFilmbyName(name)
        return self.returnFilms(ret)
    
    #根据评价最多来查询
    def getMostFavorFilm(self,limit=10):
        ret = self.sqlHandler.getMostFavorFilm(limit)
        return self.returnFilms(ret)
    
    #根据喜欢的类型来查询电影
    def getFavorFilms(self):
        if self.favorType == 'null':
            print("请填写您喜欢的电影类型后再来查询")
            return False
        ret = self.sqlHandler.getFavorFilms(self.id)
        return self.returnFilms(ret)
    
    #根据分数高低来查询
    def getMostRankingFilm(self, limit=10, score=0):
        ret = self.sqlHandler.getMostRankingFilm(limit, score)
        return self.returnFilms(ret)
    
    # 返回其他用户推荐给他的电影
    def getRecommedFilm(self):
        ret = self.sqlHandler.getRecommedFilm(self.id)
        return self.returnFilms(ret)
    
    #写评论
    def writeReview(self, film, text, rank=10, force=False):
        ret = self.sqlHandler.writeReview(film, self.id, text, rank=10, force=False)
        return ret
    
    #删除自己写的评论
    def deleteReview(self, film):
        ret = self.sqlHandler.deleteReview(film, self.id)
        return ret
    
    #为别人推荐电影
    def recommendFilm(self, recommend, film):
        ret = self.sqlHandler.recommendFilm(self.id, recommend, film)
        return ret 
    
    #删除自己的推荐
    def deleteRecommend(self, recommend, film):
        ret = self.sqlHandler.deleteRecommend(self.id, recommend, film)
        return ret
    
    #返回电影信息
    def returnFilms(self, ret):
        infoList = []
        flag, ret = ret
        #如果操作出现错误，则会返回错误信息
        if flag == False:
            infoList.append(ret)
            return infoList
        #如果没有错误
        if len(ret) == 0:
            infoList.append("还没有相应记录")
            return infoList
        for item in ret:
            director = self.sqlHandler.getDirectbyfilm(int(item[3]))
            infoList.append("电影名称：{}；电影类型：{}；导演：{}·{}; 上映时间：{}".format(item[1], item[2], director[1][0][1], director[1][0][2], item[4]))
        return infoList
    
    
    
    
    def getName(self):
        return self.firstName, self.secondName
    
    def getFavor(self):
        return self.favorType
#    
#user = User()
#user("hhhhhh", "234567")
#user.changepass("123456")

        
        
        
        
        
        
        
        