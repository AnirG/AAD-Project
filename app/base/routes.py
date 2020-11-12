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
from app.base.forms import LoginForm, CreateAccountForm, MakeTransactionCrypto
from app.base.models import User, User_Crypto, Public_Ledger, Transaction_Crypto

from app.base.util import verify_pass

from datetime import date

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', msg='Username already registered', form=create_account_form)

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', msg='Email already registered', form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', msg='User created please <a href="/login">login</a>', form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


# Crypto Implementations

@blueprint.route('/register_for_crypto', methods=['GET','POST'])
def register_for_crypto():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    if request.method == "POST":

        current_username = current_user._get_current_object().username

        if User_Crypto.query.filter_by(username=current_username).first():
           return render_template('views/pay.html', msg='Already Registered!') 


        pvk, pbk = generate_KeyPair()
        id = User.query.filter_by(username=current_username).first().id
       # print(type(pvk), type(pbk), id)
        user = User_Crypto(current_username, pvk, pbk, id)
        db.session.add(user)
        db.session.commit()


        return render_template('views/pay.html', msg='Registered!')
    else:
        return render_template('views/pay.html')

@blueprint.route('mining_pool',methods=['GET'])
def showMiningPool():
    print("haha")
    query = Transaction_Crypto.query.all()
    dg = []
    list_query=[]
    for i in query:
        # print("Digital signature: ",i.digital_signature)
        # print("public key sender: ",i.pbk_sender)
        # print("public key receiver: ",i.pbk_receiver)
        # print("amount: ",i.amount)
        # print("date: ",i.date)
        # print("comments: ",i.comments)
        dg.append(i.digital_signature)

    

    return render_template('views/mining_pool.html', list=dg, query=query)



# @blueprint.route('public_ledger', methods=['GET'])
# def showTable():

# # parse the public ledger db data to html

# @blueprint.route('mine',methods=['GET','POST'])
# def mine():



@blueprint.route('make_transaction_aaa', methods=['GET','POST'])
def createTransaction():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    form = MakeTransactionCrypto(request.form)

    # if User_Crypto.query.filter_by(username=current_username).first():
    #     return render_template('views/make_transaction.html', msg='Make an account dumbass!') 

    current_username = current_user._get_current_object().username

    user = User_Crypto.query.filter_by(username=current_username).first()

   # print(form['private_key'])
    msg_success=""
    msg_warning=""
        
    if 'update_now' in request.form:

        public_key = request.form.get('public_key')    # hardcoded
        private_key = request.form.get('private_key')
        amount = request.form.get('amount')      # integer
        receiver_public_key = request.form.get('receiver_public_key')

        recepient_user = User_Crypto.query.filter_by(public_key=receiver_public_key).first()


        if not recepient_user or recepient_user == user:
            msg_warning = "Invalid receiver public key!"

        comments = request.form.get('comments')
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")
        message = public_key + receiver_public_key + amount + today_date + comments
        
        if not msg_warning:
            try:
                digital_sig = create_Signature(message, private_key)

                if(float(user.net_balance) < float(amount)):
                    msg_warning = "Funds insufficient!"
#            
                elif verify_Signature(message, digital_sig, public_key):
                    data = Transaction_Crypto(public_key, receiver_public_key, amount, today_date, comments, digital_sig)
                    db.session.add(data)
                    db.session.commit()

                    msg_success="Added to the miner pool!"

                else:
                    msg_warning="Invalid private key!"
            except:
                msg_warning="Invalid private key!"
                
        #digital_sig = create_Signature(message, private_key)

    
    return render_template('views/make_transaction.html', form=MakeTransactionCrypto, public_key = user.public_key, msg_success=msg_success, msg_warning=msg_warning)


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
