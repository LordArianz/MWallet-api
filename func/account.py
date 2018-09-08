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


def add_account():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    account = Account()
    account.user_id = user.id
    db_session.add(account)
    db_session.commit()
    return json.dumps({
        'status': 'OK',
        'account': account
    })


def get_account():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'account_id' in request.form :
        account = Account.query.filter(Account.id == request.form['account_id'])
        if account is not None :
            json.dumps({
                'status': 'OK',
                'account': account
            })
        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_accounts():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    accounts = Account.query.filter(Account.user_id == user.id)
    json.dumps({
        'status': 'OK',
        'accounts': accounts
    })


def charge_account():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })
    if 'account_id' in request.form and 'value' in request.form:
        account = Account.query.filter(Account.id == request.form['account_id']).first()
        account.balance += request.form['value']
        return json.dumps({
            'status': 'OK',
            'accounts': account
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })
