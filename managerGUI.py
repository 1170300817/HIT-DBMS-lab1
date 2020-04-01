import tkinter
import manager


class ManagerGUI():
    
    def __call__(self):
        self.manager = manager.Manager()
        self.tk = tkinter.Tk()
        self.tk.title("Login")
        self.tk.geometry('800x300')
        self.tk.resizable(0,0)
        self.label1 = tkinter.Label(self.tk, text="管理员模式", compound='left')
        self.label1.grid(row=0, column=0, sticky=tkinter.W, pady=10)
        
        self.label4 = tkinter.Label(self.tk, text="电影名字", compound='left')
        self.label4.grid(row=3, column=0, sticky=tkinter.W, pady=10)
        self.entry3 = tkinter.Entry(self.tk, width=26)
        self.entry3.grid(row=3, column=1, sticky=tkinter.W, pady=10)
        self.label5 = tkinter.Label(self.tk, text="类型", compound='left')
        self.label5.grid(row=4, column=0, sticky=tkinter.W, pady=10)
        self.entry4 = tkinter.Entry(self.tk, width=26)
        self.entry4.grid(row=4, column=1, sticky=tkinter.W, pady=10)
        self.label6 = tkinter.Label(self.tk, text="导演名字", compound='left')
        self.label6.grid(row=5, column=0, sticky=tkinter.W, pady=10)
        self.entry5 = tkinter.Entry(self.tk, width=26)
        self.entry5.grid(row=5, column=1, sticky=tkinter.W, pady=10)
        self.button5 = tkinter.Button(self.tk, text="增加电影", activeforeground="red", command=self.newFilm)
        self.button5.grid(row = 5, column=2, sticky=tkinter.W)
        self.button6 = tkinter.Button(self.tk, text="删除电影", activeforeground="red", command=self.deleteFilm)
        self.button6.grid(row = 5, column=3, sticky=tkinter.W)
        
        self.label7 = tkinter.Label(self.tk, text="演员名字", compound='left')
        self.label7.grid(row=6, column=0, sticky=tkinter.W, pady=10)
        self.entry6 = tkinter.Entry(self.tk, width=26)
        self.entry6.grid(row=6, column=1, sticky=tkinter.W, pady=10)
        self.label8 = tkinter.Label(self.tk, text="电影名字", compound='left')
        self.label8.grid(row=7, column=0, sticky=tkinter.W, pady=10)
        self.entry7 = tkinter.Entry(self.tk, width=26)
        self.entry7.grid(row=7, column=1, sticky=tkinter.W, pady=10)
        self.button7 = tkinter.Button(self.tk, text="增加电影演员", activeforeground="red", command=self.newAct)
        self.button7.grid(row = 7, column=2, sticky=tkinter.W)
        self.tk.mainloop()

    
    def newFilm(self):
        title = self.entry3.get()
        type = self.entry4.get()
        name = self.entry5.get().split(" ")
        ret = self.manager.newFilm(title, type, name[0], name[1])
        if ret == True:
            self.tipGUI("Tips", "成功增加电影", self.tk)
        else:
            self.tipGUI("Error", "增加电影失败", self.tk)
    
    def deleteFilm(self):
        film = self.entry3.get()
        ret = self.manager.deleteFilm(film)
        if ret == True:
            self.tipGUI("Tips", "成功删除电影", self.tk)
        else:
            self.tipGUI("Error", "删除电影失败", self.tk)
            
    def newAct(self):
        actorname = self.entry6.get()
        filmname = self.entry7.get()
        ret = self.manager.newAct(actorname, filmname)
        if ret == True:
            self.tipGUI("Tips", "成功插入新演员", self.tk)
        else:
            self.tipGUI("Error", "插入演员失败", self.tk)
    
    def tipGUI(self, title, text, root):
        tkError = tkinter.Toplevel(root)
        tkError.title(title)
        tkError.geometry('300x80')
        tkError.resizable(0,0)
        lable = tkinter.Label(tkError, text = text, font=8, fg="red")
        lable.grid(row = 0, column=0, pady=23, padx = 70)
        tkError.mainloop()

a = ManagerGUI()
a()


