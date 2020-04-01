import SqlHandler


class Manager():
    
    def __init__(self):
        self.Type = 'MANAGER'
        self.sql = SqlHandler.SqlHandler(self.Type)
    # 新增Act记录
    def newAct(self, actorname, filmname):
        return self.sql.newAct(actorname, filmname)

    # 新增film记录
    def newFilm(self, title, type, first, second):
        return self.sql.newFilm(title, type, first, second)

    # 删除film记录
    def deleteFilm(self, film):
        return self.sql.deleteFilm(film)




