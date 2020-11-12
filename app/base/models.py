# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean
import sqlalchemy
from app import db, login_manager

from app.base.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value )
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class User_Crypto(db.Model):

    __tablename__ = 'User_Crypto'

    id = Column(Integer, primary_key=True)      # same as the User class
    username = Column(String, unique=True)      
    private_key = Column(String, unique=True)   # store the hash of private key actually. FOR NOW, NOT HASHING FOR DEBUG PURPOSES.. 
    public_key = Column(String, unique=True)
    net_balance = Column(String)

    def __init__(self, username, pvk, pbk, id):
        self.username = username
        self.private_key = pvk
        self.public_key = pbk
        self.id = id
        self.net_balance = 1000

class Public_Ledger(db.Model):    # this will contain info for block

    __tablename__ = 'Public_Ledger'

    id = Column(Integer, primary_key=True)
    pbk_sender = Column(String) 
    pbk_receiver = Column(String) 
    amount = Column(String) 
    date = Column(String) 
    comments = Column(String) 
    prev_hash = Column(String)
    current_hash = Column(String)
    nonce = Column(String)
    verify_digital_signature = Column(Boolean, unique=False, default=False)

    def __init__(self,b,c,e,f,g,h,i,j,k):
        self.pbk_sender = b
        self.pbk_receiver = c 
        self.amount = e
        self.date = f
        self.comments = g 
        self.current_hash = h
        self.prev_hash = i
        self.nonce = j
        self.digital_signature = k


class Transaction_Crypto(db.Model):

    __tablename__ = 'Transaction_Crypto'

    id = Column(Integer, primary_key=True)
    pbk_sender = Column(String) 
    pbk_receiver = Column(String) 
    amount = Column(String) 
    date = Column(String) 
    comments = Column(String) 
    digital_signature = Column(String)

    def __init__(self, a, b, d, e, f, g):
    #id = Column(Integer, primary_key=True)
        self.pbk_sender = a
        self.pbk_receiver = b 
        self.amount = d
        self.date = e 
        self.comments = f 
        self.digital_signature = g



@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
