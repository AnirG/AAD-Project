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
from app.codes.settlement_algo import Settle
import random
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, MakeTransactionCrypto
from app.base.models import User, User_Crypto, Public_Ledger, Transaction_Crypto
from app.base.forms_bs import friends_form, pending_friends_form, transactions_form, pending_transactions_form
from app.base.models_bs import friends_bs, friend_requests, pending_transactions, confirmed_transactions

from app.base.util import verify_pass

from datetime import date

from sqlalchemy import or_, desc, and_

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
    return redirect('/friends_list')

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

@blueprint.route('/index_crypto',methods=['GET'])
def showDashboard():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    current_username = current_user._get_current_object().username
    user = User_Crypto.query.filter_by(username=current_username).first()
    pbk = User_Crypto.query.filter_by(username=current_username).first().public_key
    query = Public_Ledger.query.filter(or_(Public_Ledger.pbk_sender == pbk,  Public_Ledger.pbk_receiver == pbk)).order_by(Public_Ledger.id.desc())

    return render_template('index_crypto.html', net_balance = user.net_balance,query=query, pbk=pbk)


@blueprint.route('/register_crypto', methods=['GET','POST'])
def register_for_crypto():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    current_username = current_user._get_current_object().username

    if User_Crypto.query.filter_by(username=current_username).first():

        if request.method == "POST":
            user = User_Crypto.query.filter_by(username=current_username).first().private_key
            print(user, request.form['private_key'])
            if request.form['private_key'] == user:
                return redirect('/public_ledger')
            else:
                return render_template('views/register_login_crypto.html', msg_warning='Wrong private key!') 

        return render_template('views/register_login_crypto.html', msg='') 

    else:
        
        msg="need to register"

        if request.method == "POST":

            pvk, pbk = generate_KeyPair()
            id = User.query.filter_by(username=current_username).first().id
            user = User_Crypto(current_username, pvk, pbk, id)
            db.session.add(user)
            db.session.commit()
            return render_template('views/register_c.html', msg=msg, pvk=pvk) 
        return render_template('views/register_c.html', msg=msg) 
        
@blueprint.route('transaction_history',methods=['GET','POST'])
def showTransactionHistory():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    # current_username = current_user._get_current_object().username
    # pbk = User_Crypto.query.filter_by(username=current_username).first().public_key
    # query = Public_Ledger.query.filter(or_(Public_Ledger.pbk_sender == pbk,  Public_Ledger.pbk_receiver == pbk)).order_by(Public_Ledger.id.desc())
   
    # return render_template('views/transaction_history.html', query=query, pbk=pbk)
    return redirect('\index_crypto')



@blueprint.route('mining_pool',methods=['GET','POST'])
def showMiningPool():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    query = Transaction_Crypto.query.all()
    msg=""

    if request.method == "POST":
        dg = request.form['ss']
        print("dg: ", dg)
        lst=[]
        lst.append(dg)
        
        pend_trans = Transaction_Crypto.query.filter_by(digital_signature=dg).first()
        block = dg + pend_trans.pbk_sender + pend_trans.pbk_receiver + str(pend_trans.amount) + pend_trans.date + pend_trans.comments

        N = 4
        nonce="-1"
        while True:
            nonce = str(int(nonce)+1)
            hashed_block = SHA256(nonce+block)
            if str(hashed_block[0][0:N]) == "0"*N:
                break
        
        if not Public_Ledger.query.filter_by(digital_signature=dg).first():

            last_block_hash = Public_Ledger.query.order_by(Public_Ledger.id.desc()).first().current_hash

            data = Public_Ledger(pend_trans.pbk_sender,
                                pend_trans.pbk_receiver,
                                pend_trans.amount,
                                pend_trans.date, 
                                pend_trans.comments,
                                str(hashed_block[1]),
                                last_block_hash,
                                nonce,
                                dg
                                )
                                
            db.session.add(data)
            db.session.commit()

            user_sender = User_Crypto.query.filter_by(public_key=pend_trans.pbk_sender).first()
            user_sender.net_balance = str(float(user_sender.net_balance) - float(pend_trans.amount))
            db.session.commit()

            user_receiver = User_Crypto.query.filter_by(public_key=pend_trans.pbk_receiver).first()
            user_receiver.net_balance = str(float(user_receiver.net_balance) + float(pend_trans.amount))
            db.session.commit()

            obj = Transaction_Crypto.query.filter_by(digital_signature=dg).first()
            db.session.delete(obj)
            db.session.commit()

            msg = " Nonce: " + str(nonce)
            print(msg)


        return render_template('views/mining_pool.html', msg=msg, query=query, lst=lst)
    return render_template('views/mining_pool.html', msg=msg, query=query)
    
    
    



@blueprint.route('public_ledger', methods=['GET'])
def showTable():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    query = Public_Ledger.query.order_by(Public_Ledger.id.desc())
    return render_template('views/public_ledger.html', query=query)

    

# # parse the public ledger db data to html

# @blueprint.route('mine',methods=['GET','POST'])
# def mine():



@blueprint.route('make_transaction', methods=['GET','POST'])
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

                pending_amt = Transaction_Crypto.query.filter_by(pbk_sender=public_key)
                total_sum = 0
                for s in pending_amt:
                    total_sum += float(s.amount)


                if(float(user.net_balance) < float(amount) + total_sum):
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


@blueprint.route('settle',methods=['GET','POST'])
def show_friends():
    current_username = current_user._get_current_object().username
    friends_list = friends_bs.query.filter_by(user_id=current_username)

    debt_dict = {}

    if request.method == "POST":
        check_list = request.form.getlist('check_box')
        check_list.append(current_username)
        #debts_list = friends_bs.query.filter_by(user_id=current_username)

        return_array = []

        for guy_a in check_list:
            net_debt = 0
            for friend in check_list:
                if guy_a != friend:
                    foo = friends_bs.query.filter(and_(friends_bs.user_id == guy_a, friends_bs.friend_id == friend)).first()
                    if foo:
                        net_debt += int(float(foo.amount))
                    else:
                         return render_template('views/settle.html',alert_msg= guy_a + " is not friend with " + friend, friends=friends_list)

            return_array.append([guy_a, -1*net_debt])
            
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")


        settlement_data = Settle(return_array,40)[0]            # 40 can be tweaked around for the cap amount.



        for guy_a in check_list:
            net_debt = 0
            comment = "settled with "
            for friend in check_list:
                if guy_a != friend:
                    comment = comment + friend + ' '
                    obj = friends_bs.query.filter(and_(friends_bs.user_id == guy_a, friends_bs.friend_id == friend)).first()
                    obj.amount = "0"
                    db.session.commit()
                    
            data = confirmed_transactions(guy_a, '', '', today_date, comment) 
            db.session.add(data)
            db.session.commit()


        return render_template('views/settle.html',friends=friends_list, success_msg=settlement_data,)


        print(return_array)
    


    return render_template('views/settle.html',friends=friends_list)



@blueprint.route('friends_list',methods=['GET','POST'])
def generate_friends_list():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    
    current_username = current_user._get_current_object().username
    
    friends_form = friends_bs.query.filter_by(user_id=current_username)
    
    pending_friends_form = friend_requests.query.filter_by(user_id=current_username)
    
    pending_friends_form1 = friend_requests.query.filter_by(friend_id=current_username)
    
    friends1 = [friend.friend_id for friend in friends_form]
    print(friends1)
    friends2 = [friend.user_id for friend in pending_friends_form1]
    friends3 = [friend.friend_id for friend in pending_friends_form]
    print(friends2)
    print(friends3)
    all_users = User.query.filter( and_ (User.username != current_username, User.username not in friends1)).all()
    other_users=[]
    for ouser in all_users:
        if (ouser.username not in friends1) and (ouser.username not in friends2) and (ouser.username not in friends3) :
            other_users.append(ouser.username)
    print(other_users)
    
    
    if 'accept' in request.form:
        print ("hiiiiii")
        name_id = request.form['accept']
        print (name_id)
        
        #form = friends_form(request.form)

        user_id = current_username
        friend_id= name_id
        amount = "0"
        print(user_id)
        print("he is the user")
        
        data = friends_bs(
            user_id,
            friend_id,
            amount
        )
        data2 = friends_bs(
            friend_id,
            user_id,
            amount
        )
        #p_friend = friends_bs(**request.form)
        db.session.add(data)
        db.session.commit()
        db.session.add(data2)
        db.session.commit()
        
        obj = friend_requests.query.filter( and_(friend_requests.user_id.like(user_id), friend_requests.friend_id.like(friend_id))).first()
        db.session.delete(obj)
        db.session.commit()

        #db_config = read_db_config()
        #query = "DELETE FROM friend_requests WHERE user_id = user_id and friend_id = friend_id"

        # try:
	    #     del_request = friend_requests(**db_config)
	    #     cursor = del_request.cursor()
	    #     cursor.execute(query,(user_id),(friend_id))
	    #     del_request.commit()

        # except Error as error:
        # 	print(error)

        # finally:
        # 	cursor.close()
        # 	del_request.close()
        
    if 'decline' in request.form:
        print ("hello")
        name_id = request.form['decline']
        print (name_id)
        user_id = current_username
        friend_id= name_id
        obj = friend_requests.query.filter( and_(friend_requests.user_id.like(user_id), friend_requests.friend_id.like(friend_id))).first()
        db.session.delete(obj)
        db.session.commit()
        
    if 'search_friend' in request.form:
        tar = request.form['target_username']
        print("boo")
        print(tar)
        data = friend_requests(
            tar,
            current_username
        )
        db.session.add(data)
        db.session.commit()
    
    
    return render_template('views/friends.html', current_friend = friends_form, pending_friend = pending_friends_form, other_users = other_users)



@blueprint.route('transactions_page',methods = ['GET','POST'])
def transactions_page():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    current_username = current_user._get_current_object().username
    
    transactions_form = confirmed_transactions.query.filter(or_(confirmed_transactions.to_id == current_username, confirmed_transactions.from_id == current_username)).order_by(confirmed_transactions.id.desc())
    
    pending_transactions_form = pending_transactions.query.filter_by(to_id=current_username).order_by(pending_transactions.date_p.desc())
    
    friends_form = friends_bs.query.filter_by(user_id=current_username)
    
    print(transactions_form)
    
    if 'accept' in request.form:
        print ("hiiiiii")
        id = request.form['accept']
        trans_d = pending_transactions.query.filter_by(id=id).first()
        
        print(trans_d.amount, trans_d.from_id, trans_d.to_id)
        
        data = confirmed_transactions(
            trans_d.from_id,
            trans_d.to_id,
            trans_d.amount,
            trans_d.date_p,
            trans_d.comment
        )
        
        friend_obj = friends_bs.query.filter(and_(friends_bs.user_id == trans_d.from_id, friends_bs.friend_id == trans_d.to_id)).first()
        friend_obj.amount = str(float(friend_obj.amount) + float(trans_d.amount))
        db.session.commit()
    
        db.session.add(data)
        db.session.commit()
        
        friend_obj = friends_bs.query.filter(and_(friends_bs.user_id == trans_d.to_id, friends_bs.friend_id == trans_d.from_id)).first()
        friend_obj.amount = str(float(friend_obj.amount) - float(trans_d.amount))
        db.session.commit()
    
        db.session.add(data)
        db.session.commit()

        db.session.delete(trans_d)
        db.session.commit()

    if 'decline' in request.form:
        print ("hello")
        id = request.form['decline']
        trans_d = pending_transactions.query.filter_by(id=id).first()
        db.session.delete(trans_d)
        db.session.commit()
        
    if 'update_now' in request.form:
        print("lol")
        var = request.form['amount_inp']
        var2 = request.form['friend_name']
        var3 = request.form['comments_inp']
        print(var)
        print(var2)
        print(var3)
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")
        print(today_date)
        data_new = pending_transactions(
            current_username,
            var2,
            var,
            today_date,
            var3
        )
        db.session.add(data_new)
        db.session.commit()

    return render_template('views/transactions.html',current_username = current_username, to = pending_transactions_form, to_confirmed = transactions_form, confirmed_friendl = friends_form)

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
