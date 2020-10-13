# -*- encoding: utf-8 -*-
 
import hashlib, binascii, os
import bcrypt

def hash_pass(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password,salt)
    return hashed

def verify_pass(provided_password, stored_password):
    provided_password = provided_password.encode('utf-8')
    return bcrypt.checkpw(provided_password, stored_password)