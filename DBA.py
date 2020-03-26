import SqlHandler as sq

class DBA():
    
    def __init__(self, type=None):
        self.userType = 'DBA'
        self.handler = sq.SqlHandler(self.userType)
        self.type = type
    
    def __call__(self, type):
        self.type = type
        
    def testLogin(self, userName, password):
        loginFlag, message = self.handler.login(userName, password)
        if loginFlag == True:
            self.type = "USER"
        return loginFlag, message
    
    def createCount(self, firstName, secondName, favorType, userName, password):
        if favorType is None:
            result = self.handler.newUser(firstName, secondName, userName, password)
        else:
            result = self.handler.newUser(firstName, secondName, userName, password, favorType)
        return result
     
    def changePass(self, user_id, password):
        if self.type != 'USER':
            print("请先登录再试")
            return False
        result = self.handler.changePass(user_id, password)
        return result
       