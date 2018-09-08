from flask import request
from db.models import *
from db.connection import db_session
from Crypto.PublicKey import RSA
from Crypto import Random
import datetime
import json
from hashlib import sha256



TOKEN_KEY = "89buy[egv9hngqty%$#@&D#@Y&E*Hhasudy1c7hy&YH*&@ECQE"

def check_token():
    if 'token' not in request.form:
        return None
    tmp_token = Token.query.filter(Token.token == request.form['token']).first()
    return tmp_token.user if tmp_token is not None else None


def add_factor():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })
    if 'rcv_acc_id' in request.form and 'value' in request.form and 'details' in request.form :
        factor = Factor()
        factor.rcv_acc_id = request.form['rcv_acc_id']
        factor.value = request.form['value']
        factor.details = request.form['details']
        db_session.add(factor)
        db_session.commit()
        return json.dumps({
            'status': 'OK',
            'factor': factor
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def participate_factor():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })
    if 'snd_acc_id' in request.form and 'factor_id' in request.form :
        factor = Factor.query.filter(Factor.id == request.form['factor_id'])
        if factor is not None:
            factor.snd_acc_id = request.form['snd_acc_id']
            factor.tried = True
            factor.pay_time = datetime.datetime.utcnow()
            db_session.commit()

            # random_generator = Random.new().read
            # key = RSA.generate(1024, random_generator)

            transaction_token = TransactionToken()
            transaction_token.user_id = user.id
            transaction_token.token = sha256(user.id + str(datetime.datetime.utcnow()) + TOKEN_KEY).hexdigest()

            db_session.add(transaction_token)
            db_session.commit()

            return json.dumps({
                'status': 'OK',
                'factor': factor,
                'transaction_token': transaction_token.token,
                'public_key' : ''
            })

        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def complete_factor():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })
    if 'factor_id' in request.form:
        factor = Factor.query.filter(Factor.id == request.form['factor_id'])
        if factor is not None:
            sender_account = Factor.snd_acc
            receiver_account = Factor.rcv_acc
            balance = sender_account.value - sender_account.blocked_balance
            if balance >= factor.value:
                sender_account.value -= factor.value
                receiver_account.value += factor.value
                factor.successfull = True
                transaction = Transaction()
                transaction.snd_acc_id = factor.snd_acc_id
                transaction.rcv_acc_id = factor.rcv_acc_id
                transaction.value = factor.value
                transaction.factor_id = factor.id
                db_session.add(transaction)
                db_session.commit()

                return json.dumps({
                    'status': 'OK',
                    'transaction': transaction
                })

            return json.dumps({
                'status': 'ERROR',
                'code': 'NOT_ENOUGH_BALANCE'
            })

        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_factor():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'factor_id' in request.form:
        factor = Factor.query.filter(Factor.id == request.form['factor_id']).first()
        if factor is not None:
            return json.dumps({
                'status': 'OK',
                'factor': factor
            })
        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_factors():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    factors = Factor.query.filter(Factor.snd_acc_id == user.id)
    return json.dumps({
        'status': 'OK',
        'factors': factors
    })