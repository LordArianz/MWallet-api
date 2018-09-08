from flask import request
from db.models import *
from db.connection import db_session
import json


def check_token():
    if 'token' not in request.form:
        return None
    tmp_token = Token.query.filter(Token.token == request.form['token']).first()
    return tmp_token.user if tmp_token is not None else None


def add_card():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'card_num' in request.form and 'cvv2' in request.form and 'name' in request.form \
            and 'exp_date' in request.form :
        card = Card()
        card.card_num = request.form['card_num']
        card.cvv2 = request.form['cvv2']
        card.exp_date = request.form['exp_date']
        card.name = request.form['name']
        card.user_id = user.id
        db_session.add(card)
        db_session.commit()
        return json.dumps({
            'status': 'OK',
            'card': card
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_card():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'card_id' in request.form:
        card = Card.query.filter(Card.id == request.form['card_id'])
        if card is not None:
            return json.dumps({
                'status': 'OK',
                'card': card
            })
        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })

    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })


def get_cards():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    cards = Card.query.filter(Card.user_id == user.id)
    return json.dumps({
        'status': 'OK',
        'cards': cards
    })


def remove_card():
    user = check_token()
    if user is None:
        return json.dumps({
            'status': 'ERROR',
            'code': 'BAD_TOKEN'
        })

    if 'card_id' in request.form :
        card = Card.query.filter(Card.id == request.form['card_id'])
        if card is not None:
            db_session.remove(card)
            db_session.commit()
            return json.dumps({
                'status': 'OK'
            })
        return json.dumps({
            'status': 'ERROR',
            'code': 'NOT_FOUND'
        })
    return json.dumps({
        'status': 'ERROR',
        'code': 'BAD_REQUEST'
    })
