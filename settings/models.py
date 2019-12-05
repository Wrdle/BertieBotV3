from flask_login import UserMixin
from . import botDB

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def get(cls, username):
        return botDB.getUser(username)
    
    @classmethod
    def getWithID(cls, username):
        return botDB.getUserWithID(username)

