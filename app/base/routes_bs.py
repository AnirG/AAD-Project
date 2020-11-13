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
from app.base.models_bs import """ fill it        """

from app.base.util import verify_pass

from datetime import date


""" fill it """

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