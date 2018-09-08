from flask import request
from db.models import *
from db.connection import db_session
import datetime
from Crypto.PublicKey import RSA
from Crypto import Random
import json
from hashlib import sha256

TOKEN_KEY = "89buy[egv9hngqty%$#@&D#@Y&E*Hhasaso8u985(&*%^gbnudy1c7hy&YH*&@ECQE"


def check_token():
    if 'token' not in request.form:
        return None
    tmp_token = Token.query.filter(Token.token == request.form['token']).first()
    return tmp_token.user if tmp_token is not None else None


def participate_transaction():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    transaction_token = TransactionToken()
    transaction_token.user_id = user.id
    transaction_token.token = sha256(user.id + str(datetime.datetime.utcnow()) + TOKEN_KEY).hexdigest()

    db_session.add(transaction_token)
    db_session.commit()

    return json.dumps({
        'status': 'OK',
        'transaction_token': transaction_token.token,
        'public_key': ''
    })


def add_transaction():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'rcv_acc_id' in request.form and 'snd_acc_id' and 'value' in request.form:
        sender_account = Account.query.filter(Account.id == request.form['snd_acc_id'])
        receiver_account = Account.query.filter(Account.id == request.form['rcv_acc_id'])
        balance = sender_account.value - sender_account.blocked_balance
        if balance >= request.form['value']:
            sender_account.value -= request.form['value']
            receiver_account.value += request.form['value']
            transaction = Transaction()
            transaction.snd_acc_id = request.form['snd_acc_id']
            transaction.rcv_acc_id = request.form['rcv_acc_id']
            transaction.value = request.form['value']
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
        'code': 'BAD_REQUEST'
    })


def get_transaction():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'transaction_id' in request.form:
        transaction = Transaction.query.filter(Transaction.id == request.form['transaction_id']).first()
        if transaction is not None:
            return json.dumps({
                'status': 'OK',
                'transaction': transaction
            })
        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_transactions():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    transactions = Transaction.query.filter(Transaction.snd_acc == user.id)
    transactions += Transaction.query.filter(Transaction.rcv_acc_id == user.id)
    return json.dumps({
        'status': 'OK',
        'transactions': transactions
    })