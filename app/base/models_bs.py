"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean
import sqlalchemy
from sqlalchemy.schema import PrimaryKeyConstraint

from app import db, login_manager

from app.base.util import hash_pass

class friends_bs(db.Model):
    
    __tablename__ = 'friends_bs'
    
    user_id = Column(String)
    friend_id = Column(String)
    amount = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'friend_id'),
    )
    
    def __init__(self, a, b, c):
        self.user_id = a
        self.friend_id = b
        self.amount = c

class friend_requests(db.Model):
    
    __tablename__ = 'friend_requests'
    
    user_id = Column(String)
    friend_id = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'friend_id'),
    )
    
    def __init__(self, a, b):
        self.user_id = a
        self.friend_id = b
        
class confirmed_transactions(db.Model):
    
    __tablename__ = 'confirmed_transactions'
    
    from_id = Column(String)
    to_id = Column(String)
    amount = Column(String)
    date_p = Column(String)
    comment = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('from_id', 'to_id','amount','date_p','comment'),
    )
    def __init__(self, a, b, c, d, e):
        self.from_id = a
        self.to_id = b
        self.amount = c
        self.date_p = d
        self.comment = e

        
class pending_transactions(db.Model):
    
    __tablename__ = 'pending_transactions'
    
    from_id = Column(String)
    to_id = Column(String)
    amount = Column(String)
    date_p = Column(String)
    comment = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('from_id', 'to_id','amount','date_p','comment'),
    )
    def __init__(self, a, b, c, d, e):
        self.from_id = a
        self.to_id = b
        self.amount = c
        self.date_p = d
        self.comment = e        


# @login_manager.user_loader
# def user_loader(id):
#     return User.query.filter_by(id=id).first()

# @login_manager.request_loader
# def request_loader(request): 
#     username = request.form.get('username')
#     user = User.query.filter_by(username=username).first()
#     return user if user else None
