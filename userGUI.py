import tkinter 
import user


favorList = ['comedy', 'tragedy', 'literary', 'detective', 'sciencefiction', 'action', 'thriller', 'romance']

class GUI():
    
    def __init__(self, command=None):
        self.root = tkinter.Tk()
        self.root.iconify()
        self.tkGUI = tkinter.Toplevel()
        #GUI config
        self.tkGUI.title("Login")
        self.tkGUI.geometry('240x300')
        self.tkGUI.resizable(0,0)
        self.label1 = tkinter.Label(self.tkGUI, text="用户名：", compound='left')
        self.label1.grid(row=0, column=0, sticky=tkinter.W+ tkinter.S, pady=10)
        self.label2 = tkinter.Label(self.tkGUI, text="密码：", compound='left')
        self.label2.grid(row=1, column=0, sticky=tkinter.W)
        self.entry1 = tkinter.Entry(self.tkGUI, width=23)
        self.entry1.grid(row=0, column=1, sticky=tkinter.E )
        self.entry2 = tkinter.Entry(self.tkGUI, width=23, show = '*')
        self.entry2.grid(row=1, column=1, sticky=tkinter.E)
        self.entry2.bind("<Return>", self.login)
        self.button1 = tkinter.Button(self.tkGUI, text="创建新账户", activeforeground="red", command=self.createAccount)
        self.button2 = tkinter.Button(self.tkGUI, text="登录", activeforeground="red", command=self.login)
        self.button1.grid(row = 2, column=0, columnspan= 2, pady=10)
        self.button2.grid(row = 2, column=1, sticky=tkinter.E, pady=10)
#        destroy
        
    def login(self, _=None):
        username = self.entry1.get()
        password = self.entry2.get()
        if username == "" or password == "":
            self.errorUI("用户名和密码不得为空", self.tkGUI)
            return
        self.user = user.User()
        ret = self.user(self.entry1.get(), self.entry2.get())
        if ret[0] == False:
            self.errorUI(ret[1], self.tkGUI)
            return
        #如果登陆成功
        self.tkGUI.destroy()
        self.loginUI(self.user.getName()[0], self.user.getName()[1], self.user.getFavor())
    
    def createAccount(self):
        self.tkCreate = tkinter.Toplevel(self.tkGUI)
        self.tkCreate.title("Create")
        self.tkCreate.geometry('240x300')
        self.tlabel1 = tkinter.Label(self.tkCreate, text="用户名：", compound='left')
        self.tlabel1.grid(row=0, column=0, sticky=tkinter.W+ tkinter.S, pady=10)
        self.tlabel2 = tkinter.Label(self.tkCreate, text="密码：", compound='left')
        self.tlabel2.grid(row=1, column=0, sticky=tkinter.W)
        self.tlabel3 = tkinter.Label(self.tkCreate, text="确认密码：", compound='left')
        self.tlabel3.grid(row=2, column=0, sticky=tkinter.W)
        self.tlabel4 = tkinter.Label(self.tkCreate, text="姓：", compound='left')
        self.tlabel4.grid(row=3, column=0, sticky=tkinter.W)
        self.tlabel5 = tkinter.Label(self.tkCreate, text="名：", compound='left')
        self.tlabel5.grid(row=4, column=0, sticky=tkinter.W)
        self.tlabel6 = tkinter.Label(self.tkCreate, text="类型：", compound='left')
        self.tlabel6.grid(row=5, column=0, sticky=tkinter.W)
        self.tentry1 = tkinter.Entry(self.tkCreate, width=23)
        self.tentry1.grid(row=0, column=1, sticky=tkinter.E )
        self.tentry2 = tkinter.Entry(self.tkCreate, width=23, show = '*')
        self.tentry2.grid(row=1, column=1, sticky=tkinter.E)
        self.tentry3 = tkinter.Entry(self.tkCreate, width=23, show = '*')
        self.tentry3.grid(row=2, column=1, sticky=tkinter.E)
        self.tentry4 = tkinter.Entry(self.tkCreate, width=23)
        self.tentry4.grid(row=3, column=1, sticky=tkinter.E )
        self.tentry5 = tkinter.Entry(self.tkCreate, width=23)
        self.tentry5.grid(row=4, column=1, sticky=tkinter.E )
        self.tentry6 = tkinter.Entry(self.tkCreate, width=23)
        self.tentry6.grid(row=5, column=1, sticky=tkinter.E )
        self.tbutton1 = tkinter.Button(self.tkCreate, text="创建新账户", activeforeground="red", command=self.create)
        self.tbutton1.grid(row = 6, column=0, columnspan= 2, pady=10)
        self.tkCreate.mainloop()
        
    def create(self):
        if self.tentry2.get() != self.tentry3.get():
            self.errorUI("两次输入密码不一致", self.tkCreate)
            return
        first = self.tentry4.get()
        second = self.tentry5.get()
        userid = self.tentry1.get()
        password = self.tentry2.get()
        if self.tentry6.get() == '':
            favor=None
        else:
            favor=self.tentry6.get()
            if favor not in favorList:
                self.errorUI("检查您的爱好，填写有误", self.tkCreate)
            return    
        self.user = user.User()
        ret = self.user.createAccount(firstName=first, secondName=second, favorType=favor, userName=userid, password=password)
        if ret[0] == False:
             self.errorUI(ret[1], self.tkCreate)   
             return
        self.tkGUI.destroy()
        self.loginUI(self.user.getName()[0], self.user.getName()[1], self.user.getFavor())
    
    def errorUI(self, text, root, err='ERROR'):
        #报错专用弹窗
        tkError = tkinter.Toplevel(root)
        tkError.title(err)
        tkError.geometry('300x80')
        tkError.resizable(0,0)
        lable = tkinter.Label(tkError, text = text, font=8, fg="red")
        lable.grid(row = 0, column=0, pady=23, padx = 70)
        tkError.mainloop()
    
    def loginUI(self, firstname, secondname, favortype):
        #主页面专用弹窗
        self.tkMain = tkinter.Toplevel(self.root)
        self.tkMain.title("Welcome")
        self.tkMain.geometry('1500x600')
        self.tkMain.resizable(0,0)
        self.label3 = tkinter.Label(self.tkMain, text="欢迎您：{}·{}   \t您喜欢的电影类型:".format(firstname, secondname), compound='left')
        self.label3.grid(row=0, column=0, sticky=tkinter.W, pady=10)
        self.entry3 = tkinter.Entry(self.tkMain, width=26)
        self.entry3.grid(row=0, column=1, sticky=tkinter.W)
        if favortype == "null":
            favortype = "您还没有设置自己喜欢的类型"
        self.entry3.insert(2, favortype)    
        self.entry3.bind("<Return>", self.updateFavor)
        self.text1 = tkinter.Text(self.tkMain, width=80, height=27)
        self.text1.grid(row=1, column=0, rowspan=5, columnspan= 2)
        self.text2 = tkinter.Text(self.tkMain, width=80, height=3)
        self.text2.grid(row=6, column=0, columnspan= 2, pady=15)
        self.text3 = tkinter.Text(self.tkMain, width=80, height=15)
        self.text3.grid(row=7, column=0, rowspan=2, columnspan= 2)
        self.button3 = tkinter.Button(self.tkMain, text="查电影", activeforeground="red", command=self.getFilmbyName)
        self.button3.grid(row = 1, column=2, sticky=tkinter.W + tkinter.N)
        self.button4 = tkinter.Button(self.tkMain, text="评价最多", activeforeground="red", command=self.getMostFavorFilm)
        self.button4.grid(row = 2, column=2, sticky=tkinter.W + tkinter.N)
        self.button5 = tkinter.Button(self.tkMain, text="最高评分", activeforeground="red", command=self.getMostRankingFilm)
        self.button5.grid(row = 3, column=2, sticky=tkinter.W + tkinter.N)
        self.button6 = tkinter.Button(self.tkMain, text="其他用户推荐", activeforeground="red", command=self.getRecommedFilm)
        self.button6.grid(row = 4, column=2, sticky=tkinter.W + tkinter.N)
        self.button7 = tkinter.Button(self.tkMain, text="查该导演的电影", activeforeground="red", command=self.getFilmbyDirector)
        self.button7.grid(row = 6, column=2, sticky=tkinter.W)
        self.button8 = tkinter.Button(self.tkMain, text="查该演员的电影", activeforeground="red", command=self.getFilmbyActor)
        self.button8.grid(row = 7, column=2, sticky=tkinter.W + tkinter.N)
        self.label4 = tkinter.Label(self.tkMain, text="输入查找个数,不填则默认10个", compound = 'left')
        self.label4.grid(row = 2, column=3, sticky=tkinter.W)
        self.entry4 = tkinter.Entry(self.tkMain, width=6)
        self.entry4.grid(row=2, column=2, sticky=tkinter.W)
        self.label5 = tkinter.Label(self.tkMain, text="输入查找个数,不填则默认10个", compound = 'left')
        self.label5.grid(row = 3, column=3, sticky=tkinter.W)
        self.entry5 = tkinter.Entry(self.tkMain, width=6)
        self.entry5.grid(row=3, column=2, sticky=tkinter.W)
        self.label6 = tkinter.Label(self.tkMain, text="输入分数下线,不填则默认0分以上", compound = 'left')
        self.label6.grid(row = 3, column=3, sticky=tkinter.W + tkinter.S)
        self.entry6 = tkinter.Entry(self.tkMain, width=6)
        self.entry6.grid(row=3, column=2, sticky=tkinter.W + tkinter.S)
        self.favorButton = tkinter.Button(self.tkMain, text="按爱好推荐", activeforeground="red", command=self.getFavorFilms)
        self.favorButton.grid(row = 5, column=2, sticky=tkinter.W + tkinter.N)
        
        #评论板块
        self.text4 = tkinter.Text(self.tkMain, width=80, height=25)
        self.text4.grid(row=1, column=5, rowspan=4, columnspan= 4, padx=35)
        self.film = tkinter.Label(self.tkMain, text="推荐电影编号:", compound='left')
        self.film.grid(row=5, column=5, sticky=tkinter.W + tkinter.N, padx=35)
        self.filmentry = tkinter.Entry(self.tkMain, width=15)
        self.filmentry.grid(row=5, column=6, sticky=tkinter.W + tkinter.N, padx=35)
        
        self.recommend = tkinter.Label(self.tkMain, text="打分:", compound='left')
        self.recommend.grid(row=5, column=7, sticky=tkinter.W + tkinter.N, padx=35)
        self.recentry = tkinter.Entry(self.tkMain, width=15)
        self.recentry.grid(row=5, column=8, sticky=tkinter.W + tkinter.N, padx=35)
        
        self.reced = tkinter.Label(self.tkMain, text="被推荐人用户名:", compound='left')
        self.reced.grid(row=6, column=5, sticky=tkinter.W + tkinter.N, padx=35)
        self.recedentry = tkinter.Entry(self.tkMain, width=15)
        self.recedentry.grid(row=6, column=6, sticky=tkinter.W + tkinter.N, padx=35)
        self.reviewbutton = tkinter.Button(self.tkMain, text="评论", activeforeground="red", command=self.writeReview)
        self.reviewbutton.grid(row = 6, column=7, sticky=tkinter.W + tkinter.N)
        
        self.reviewbutton2 = tkinter.Button(self.tkMain, text="删除评论", activeforeground="red", command=self.deleteReview)
        self.reviewbutton2.grid(row = 6, column=8, sticky=tkinter.W + tkinter.N)
        
        self.recbutton2 = tkinter.Button(self.tkMain, text="推荐", activeforeground="red", command=self.recommendFilm)
        self.recbutton2.grid(row = 7, column=6, sticky=tkinter.W + tkinter.N)
        
        self.deletrecbutton2 = tkinter.Button(self.tkMain, text="删除推荐", activeforeground="red", command=self.deleteRecommend)
        self.deletrecbutton2.grid(row = 7, column=7, sticky=tkinter.W + tkinter.N)
        #修改密码按钮
        self.button9 = tkinter.Button(self.tkMain, text="修改密码", activeforeground="red", command=self.changepassUI)
        self.button9.grid(row = 0, column=5)
        #增加已看
        self.label7 = tkinter.Label(self.tkMain, text="输入已看电影编号", compound = 'left')
        self.label7.grid(row = 0, column=6, sticky=tkinter.W)
        self.entry7 = tkinter.Entry(self.tkMain, width=6)
        self.entry7.grid(row=0, column=7, sticky=tkinter.W)
        self.button10 = tkinter.Button(self.tkMain, text="增加已看", activeforeground="red", command=self.watchFilm)
        self.button10.grid(row = 0, column=8)
        
        self.tkMain.mainloop()
    
    
    def changepassUI(self):
        self.tkChange = tkinter.Toplevel(self.tkMain)
        self.tkChange.title("Change")
        self.tkChange.geometry('240x300')
        self.tlc1 = tkinter.Label(self.tkChange, text="原密码：", compound='left')
        self.tlc1.grid(row=0, column=0, sticky=tkinter.W+ tkinter.S, pady=10)
        self.tlc2 = tkinter.Label(self.tkChange, text="密码：", compound='left')
        self.tlc2.grid(row=1, column=0, sticky=tkinter.W)
        self.tlc3 = tkinter.Label(self.tkChange, text="确认密码：", compound='left')
        self.tlc3.grid(row=2, column=0, sticky=tkinter.W)
        self.tec1 = tkinter.Entry(self.tkChange, width=23)
        self.tec1.grid(row=0, column=1, sticky=tkinter.E )
        self.tec2 = tkinter.Entry(self.tkChange, width=23, show = '*')
        self.tec2.grid(row=1, column=1, sticky=tkinter.E)
        self.tec3 = tkinter.Entry(self.tkChange, width=23, show = '*')
        self.tec3.grid(row=2, column=1, sticky=tkinter.E)
        self.tbc1 = tkinter.Button(self.tkChange, text="修改密码", activeforeground="red", command=self.changepass)
        self.tbc1.grid(row = 3, column=0, columnspan= 2, pady=10)
        self.tkChange.mainloop()
    
    def changepass(self):
        if self.tec2.get() != self.tec3.get():
            self.errorUI("两次输入密码不一致", self.tkChange)
            return
        if self.tec1.get() != self.user.getPass():
            self.errorUI("原密码输入不正确", self.tkChange)
            return
        if self.tec1.get() == self.tec2.get():
            self.errorUI("不得与原密码相同", self.tkChange)
            return
        password = self.tec2.get()
        ret = self.user.changepass(password)
        self.tkChange.destroy()
        self.errorUI(ret[1], self.tkMain, 'TIP')
    
    #更新自己的电影喜好
    def updateFavor(self, _=None):
        favor = self.entry3.get()
        if favor not in favorList:
            self.errorUI("请输入正确的电影类型", self.tkMain)
        ret = self.user.updateFavor(favor)
        if ret[0] == False:
            self.errorUI(ret[1], self.tkMain)
            return False
        else:
            lable = tkinter.Label(self.tkMain, text=ret[1])
            lable.grid(row=0, column=1, sticky=tkinter.E, padx=5)
    
    #通过电影名字查询
    def getFilmbyName(self):
        film = self.text1.get(1.0, tkinter.END)
        film = film.replace("\n", "")
        if film == '':
            self.text1.delete(1.0,tkinter.END)
            self.text1.insert(1.0, "请在此处填写电影名称后再试")
            return False
        ret = self.user.getFilmbyName(film)
        self.returnResult(ret)  
    
    #获得最受欢迎的电影（评论最多的）
    def getMostFavorFilm(self):
        limit = self.entry4.get()
        if limit == "":
            ret = self.user.getMostFavorFilm()
            self.returnResult(ret)
            return
        limit = int(limit)
        ret = self.user.getMostFavorFilm(limit)
        self.returnResult(ret)
        return
   
    #获得评分最高的电影
    def getMostRankingFilm(self, limit=10, score=0):
        if self.entry5.get() != "":
            limit=self.entry5.get()
        if self.entry6.get() != "":
            score=self.entry6.get()
        ret = self.user.getMostRankingFilm(limit, score)
        self.returnResult(ret)
    
    #获得别的用户推荐给你的电影
    def getRecommedFilm(self):
        ret = self.user.getRecommedFilm()
        self.returnResult(ret)
    
    #根据电影名字查电影
    def getFilmbyDirector(self):
        direct = self.text2.get(1.0, tkinter.END)
        direct = direct.replace("\n", "")
        if direct == '':
            self.text2.delete(1.0,tkinter.END)
            self.text2.insert(1.0, "请在此处填写导演名称后再试")
            return False
        ret = self.user.getFilmbyDirector(direct)
        self.returnResult(ret)
    
    #根据演员名字查电影
    def getFilmbyActor(self):
        act = self.text3.get(1.0, tkinter.END)
        act = act.replace("\n", "")
        if act == '':
            self.text3.delete(1.0,tkinter.END)
            self.text3.insert(1.0, "请在此处填写演员名称后再试")
            return False
        ret = self.user.getFilmbyActor(act)
        self.returnResult(ret)
    
    #写影评
    def writeReview(self):
        film = self.filmentry.get()
        text = self.text4.get(1.0, tkinter.END)
        if self.recentry.get() == '':
            rank = 10
        else:
            rank = self.recentry.get()
        ret = self.user.writeReview(film, text, rank, False)
        self.text4.delete(1.0,tkinter.END)
        self.text4.insert(1.0, ret[1] + '\n')
    
    #写影评 
    def deleteReview(self):
        film = self.filmentry.get()
        ret = self.user.deleteReview(film)
        self.text4.delete(1.0,tkinter.END)
        self.text4.insert(1.0, ret[1] + '\n')   
    
    def recommendFilm(self):
        film = self.filmentry.get()
        recommend = self.recedentry.get()
        ret = self.user.recommendFilm(recommend, film)
        self.text4.delete(1.0,tkinter.END)
        self.text4.insert(1.0, ret[1] + '\n')
   
    def deleteRecommend(self):
        film = self.filmentry.get()
        recommend = self.recedentry.get()
        ret = self.user.deleteRecommend(recommend, film)
        self.text4.delete(1.0,tkinter.END)
        self.text4.insert(1.0, ret[1] + '\n')
    
    def getFavorFilms(self):
        favor = self.user.getFavor()
        if favor == 'null':
            self.errorUI("请先输入一个喜欢的电影类型", self.tkMain)
            return 
        ret = self.user.getFavorFilms()
        self.returnResult(ret)
    
    def watchFilm(self):
        film = self.entry7.get()
        ret = self.user.watchFilm(film)
        if ret[0] == False:
            self.errorUI(ret[1], self.tkMain)
        else:
            self.errorUI(ret[1], self.tkMain, err="Tips")
   
    #打印结果用
    def returnResult(self, ret):   
        index = 1.0; num = 1
        self.text1.delete(1.0,tkinter.END)
        for item in ret:
            self.text1.insert(index, str(num) + "."+ item + '\n\n')
            index += 2.0
            num += 1
        
        
tk = GUI()
tkinter.mainloop()