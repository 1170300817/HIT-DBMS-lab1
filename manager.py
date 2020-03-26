import SqlHandler


class Manager():
    
    def __init__(self):
        self.Type = 'MANAGER'
        self.sql = SqlHandler.SqlHandler(self.Type)
    # 新增Act记录
    def newAct(self, actor_id, film_id):
        return self.sql.newAct(actor_id, film_id)

    # 删除Act记录
    def deleteAct(self, actor_id, film_id):
        return self.sql.deleteAct(actor_id, film_id)

    # 新增Actor记录
    def newActor(self, first_name, second_name):
        return self.sql.newActor(first_name, second_name)

    # 删除Actor记录
    def deleteActor(self, first_name, second_name):
        return self.sql.deleteActor(first_name, second_name)

    # 新增director记录
    def newDirector(self, first_name, second_name):
        return self.sql.newDirector(first_name, second_name)

    # 删除director记录
    def deleteDirector(self, first_name, second_name):
        return self.sql.deleteDirector(first_name, second_name)

    # 新增film记录
    def newFilm(self, title, type, director_id):
        return self.sql.newFilm(title, type, director_id)

    # 删除film记录
    def deleteFilm(self, film_id):
        return self.sql.deleteFilm(film_id)

m = Manager()
m.deleteAct(3, 1)


