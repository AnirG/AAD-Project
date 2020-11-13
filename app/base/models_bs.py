"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean
import sqlalchemy
from app import db, login_manager

from app.base.util import hash_pass



@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request): 
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
