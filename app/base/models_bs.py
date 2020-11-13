"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean
import sqlalchemy
from app import db, login_manager

from app.base.util import hash_pass

class friends_bs(db.Model):
    
    __tablname__ = 'friends_bs'
    
    user_id = Column(String)
    friend_id = Column(String)
    amount = Column(Integer)
    
    def __init__(self, a, b, c):
        self.user_id = a
        self.friend_id = b
        self.amount = c

class friend_requests(db.Model):
    
    __tablname__ = 'friend_requests'
    
    user_id = Coulmn(String)
    friend_id = Column(String)
    
    def __init__(self, a, b):
        self.user_id = a
        self.friend_id = b
        
class confirmed_transactions(db.Model):
    
    __tablname__ = 'confirmed_transactions'
    
    from_id = Column(String)
    to_id = Column(String)
    amount = Column(Integer)
    status = Coulmn(String)
    
    def __init__(self, a, b, c, d):
        self.from_id = a
        self.to_id = b
        self.amount = c
        self.status = d
        
class pending_transactions(db.Model):
    
    __tablname__ = 'pending_transactions'
    
    from_id = Column(String)
    to_id = Column(String)
    amount = Column(integer)
    
    def __init__(self, a, b, c):
        self.from_id = a
        self.to_id = b
        self.amount = c        


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request): 
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
