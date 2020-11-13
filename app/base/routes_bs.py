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