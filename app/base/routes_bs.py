# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import sys  
sys.path.append('../../codes')

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app.codes.ecdsa_string_latest import *
from app.codes.SHA256 import *
import random
from app import db, login_manager
from app.base import blueprint
from app.base.forms_bs import friends_form, pending_friends_form, transactions_form, pending_transactions_form
from app.base.models_bs import friend_bs, friend_requests, confirmed_transactions, pending_transactions, User_Crypto

from app.base.util import verify_pass

from datetime import date


@blueprint.route('friends_list',methods=['GET','POST'])
def generate_friends_list():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    form = friends_form(request.form)

    current_username = current_user._get_current_object().username
    
    friends_from = friend_bs.filter_by(current_username=user_id)
    
    return render_template('', friends = friends_from.friend_id, amount = friends_from.amount )

@blueprint.route('add_friend',methods=['GET','POST'])
def add_friend():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    form = friends_form(request.form)

    temp1 = request.form['user']
    temp2 = request.form['friend']
    temp3 = request.form['amount']

    user_id = temp1
    friend_id = temp2
    amount = temp3

    friend_check = User.query.filter_by(username = user_id).first()
    if not user:
        return render_template( '', msg = 'Friend does not exist to be added', form = friends_form)

    friend = friends_bs(**request.form)
    db.session.add(friend)
    db.session.commit()

    user_id = temp2
    friend_id = temp1
    amount = temp3    

    friend = friends_bs(**request.form)
    db.session.add(friend)
    db.session.commit()

    return render_template( '', msg = 'Friend added succesfully', form = friends_form)

@blueprint.route('add transaction',methods = ['GET','POST'])
def add_transaction():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    form = transactions_form(request.form)

    temp1 = request.form['from_id']
    temp2 = request.form['to_id']
    temp3 = request.form['amount']
    temp4 = request.form['status']
    from_id = temp1
    to_id = temp2
    amount = temp3
    status = temp4

    transaction = confirmed_transactions(**request.form)
    db.session.add(transaction)
    db.session.commit()

    from_id = temp2
    to_id = temp1
    amount = temp3
    status = temp4

    transaction = User(**request.form)
    db.session.add(transaction)
    db.session.commit()

    return render_template( '', msg = 'Friend added succesfully', form = transactions_form)

@blueprint.route('accept friend',methods = ['GET','POST'])
def accept_friend():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    form = pending_friends_form(request.form)

    from_id = request.form['user']
    to_id = request.form['friends']

    p_friends = friend_requests(**request.form)
    db.session.add(p_friends)
    db.sessiomn.commit()

    return_render_template( '', msg = 'Friend request accepted', form = pending_friends_form)\

@blueprint.route('pending transactions',methods = ['GET','POST'])
def pending_transactions():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    form = pending_transactions_form(request.form)

    current_username = current_user._get_current_object().username
    
    pending_transactions_form = friend_bs.filter_by(current_username=user_id)

    return render_template('', to_id = pending_transactions_form.to_id, amount = pending_transactions_form.amount )


## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500