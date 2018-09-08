from flask import request
from db.models import *
from db.connection import db_session
import datetime
import json
from hashlib import sha256
from validate_email import validate_email


PASSWORD_KEY = "DHUIHF27^&*@!HD*(!)@#UWIJDPOACQW)(@HF#*QWU_D(JQSPEIUFHQE(*!@"
TOKEN_KEY = "duuSY&D#@Y&E*Hhasudy1c7hy&YH*&@ECQE"


def check_username(user):
    return 3 < len(user) < 50 and User.query.filter(User.username == user).first() is None


def check_email(mail):
    return validate_email(mail) and User.query.filter(User.email == mail).first() is None


def check_token():
    if 'token' not in request.form:
        return None
    tmp_token = Token.query.filter(Token.token == request.form['token']).first()
    return tmp_token.user if tmp_token is not None else None


def request_sms():
    if 'phone' in request.form:
        temp = TempUser()
        temp.phone = request.form['phone']
        temp.code = '452629'
        temp.hash_string = sha256(request.form['phone'] + str(datetime.datetime.utcnow()) + TOKEN_KEY).hexdigest()
        db_session.add(temp)
        db_session.commit()
        return json.dumps({
            'status': 'OK',
            'hash_string': temp.hash_string
        })
    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def verify_sms():
    if 'verification_code' in request.form and 'hash_string' in request.form:
        temp = TempUser.query.filter(TempUser.hash_string == request.form['hash_string']).first()
        if temp is None:
            return json.dumps({
                'status': 'ERROR',
                'code': 'WRONG_HASH'
            })
        if request.form['verification_code'] == temp.code:
            temp.verified = True
            db_session.commit()
            user = User.query.filter(User.phone == temp.phone).first()
            if user is not None:
                return json.dumps({
                    'status': 'OK',
                    'hash_string': temp.hash_string
                })
            else:
                return json.dumps({
                    'status': 'SIGNUP',
                    'hash_string': temp.hash_string
                })
        return json.dumps({
            'status': 'ERROR',
            'code': 'WRONG_CODE'
        })
    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def login():
    if 'sha256password' in request.form and 'hash_string' in request.form:
        tmp_user = TempUser.query.filter(TempUser.hash_string == request.form['hash_string']).first()
        if tmp_user is None:
            return json.dumps({
                'status': 'ERROR',
                'code': 'NO_SUCH_LOGIN'
            })
        if not tmp_user.verified :
            return json.dumps({
                'status': 'ERROR',
                'code': 'PHONE_NOT_VERIFIED'
            })
        user = User.query.filter(User.phone == tmp_user.phone).first()
        if user is None :
            return json.dumps({
                'status': 'ERROR',
                'code': 'SIGNUP_FIRST'
            })
        if user.password == sha256(request.form['sha256password'] + PASSWORD_KEY).hexdigest():
            token = Token()
            token.token = sha256(user.username + str(user.id) + str(datetime.datetime.utcnow()) + TOKEN_KEY).hexdigest()
            token.user_id = user.id
            user.last_seen = datetime.datetime.utcnow()
            tmp_user.used = True
            db_session.add(token)
            db_session.commit()
            return json.dumps({
                'status': 'OK',
                'user_id': user.id,
                'token': token.token
            })
        return json.dumps({
            'status': 'ERROR',
            'error': 'WRONG_USER' if user is None else 'WRONG_PASS'
        })
    return json.dumps({
        'status': 'ERROR',
        'error': 'BAD_INPUT'
    })


def signup():
    if 'hash_string' in request.form and 'first_name' in request.form and 'last_name' in request.form \
            and 'sha256password' in request.form:
        temp = TempUser.query.filter(TempUser.hash_string == request.form['hash_string']).first()
        if temp is None:
            return json.dumps({
                'status': 'ERROR',
                'code': 'NO_SUCH_LOGIN'
            })
        if not temp.verified:
            return json.dumps({
                'status': 'ERROR',
                'code': 'PHONE_NOT_VERIFIED'
            })
        user = User.query.filter(User.phone == temp.phone).first()
        if user is not None:
            return json.dumps({
                'status': 'ERROR',
                'code': 'ALREADY_SIGNED_UP'
            })
        temp.used = True
        user = User()
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.password = request.form['sha256password']
        user.phone = temp.phone
        db_session.add(user)
        db_session.commit()
        token = Token()
        token.user_id = user.id
        token.token = sha256(user.phone + str(user.id) + str(datetime.datetime.utcnow()) + TOKEN_KEY).hexdigest()
        db_session.add(token)
        db_session.commit()
        account = Account()
        account.user_id = user.id
        db_session.add(account)
        db_session.commit()
        return json.dumps({
            'status': 'OK',
            'user_id': token.user_id,
            'token': token.token
        })
    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_user():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    token = Token.query.filter(Token.token == request.form['token']).first()
    return json.dumps({
        'status': 'OK',
        'user': token.user.toJSON()
    })


def get_data():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })
    cards = array_to_json_array(Card.query.filter(Card.user_id == user.id).limit(10))
    accounts = array_to_json_array(Account.query.filter(Account.user_id == user.id).limit(10))
    factors = array_to_json_array(Factor.query.filter(Factor.snd_acc_id == user.id).limit(10))
    return json.dumps({
        'status': 'OK',
        'user': user.toJSON(),
        'cards': cards,
        'accounts': accounts,
        'factors': factors,
    })


def array_to_json_array(arr):
    json_array = []
    for element in arr :
        json_array.append(element.toJSON())

    return json_array