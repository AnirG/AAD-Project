# -*- encoding: utf-8 -*-

"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])

class MakeTransactionCrypto(FlaskForm):
    public_key = TextField('public_key', id='public_key', validators=[DataRequired()])
    private_key = PasswordField('private_key', id='private_key', validators=[DataRequired()])
    #amount = IntegerField('amount', id='amount')
    amount = IntegerField('amount', validators=[DataRequired()])
    receiver_public_key = TextField('receiver_public_key', id='receiver_public_key', validators=[DataRequired()])
    comments = TextField('comments', id='comments', validators=[DataRequired()])
    
    