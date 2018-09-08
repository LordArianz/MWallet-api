from flask import request
from db.models import *
from db.connection import db_session
import datetime
import json


def check_token():
    if 'token' not in request.form:
        return None
    tmp_token = Token.query.filter(Token.token == request.form['token']).first()
    return tmp_token.user if tmp_token is not None else None


def add_investment():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })
    if 'card_num' in request.form and 'cvv2' in request.form and 'name' in request.form \
            and 'exp_date' in request.form:
        pass

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_investment():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'investment_id' in request.form:
        investment = Investment.query.filter(Investment.id == request.form['investment_id']).first()
        return json.dumps({
            'status': 'OK',
            'code': investment
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_investments():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    investments = Investment.query.filter(Investment.account.user_id == user.id)
    return json.dumps({
        'status': 'OK',
        'code': investments
    })