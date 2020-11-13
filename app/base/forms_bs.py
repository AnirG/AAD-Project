# -*- encoding: utf-8 -*-

"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired

class friends_form(FlaskForm):
    user = TextField('user', id='user'   , validators=[DataRequired()])
    friends = TextField('friend', id='friend'   , validators=[DataRequired()])
    amount = TextField('amount', id='amount'   , validators=[DataRequired()])
    

class pending_friends_form(FlaskForm):
    user = TextField('puser', id='puser'   , validators=[DataRequired()])
    friends = TextField('pfriend', id='pfriend'   , validators=[DataRequired()])
    
    
class transactions_form(FlaskForm):
    from_id = TextField('from_id', id='from_id'   , validators=[DataRequired()])
    to_id = TextField('to_id', id='to_id'   , validators=[DataRequired()])
    amount = TextField('amount', id='amount'   , validators=[DataRequired()])
    status = TextField('status', id='status'   , validators=[DataRequired()])

    
class pending_transactions_form(FlaskForm):
    from_id = TextField('pfrom_id', id='pfrom_id'   , validators=[DataRequired()])
    to_id = TextField('pto_id', id='pto_id'   , validators=[DataRequired()])
    amount = TextField('pamount', id='pamount'   , validators=[DataRequired()]