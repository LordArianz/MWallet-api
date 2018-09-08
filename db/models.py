import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base
#from db.jalali import Gregorian
import json


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(16))
    last_name = Column(String(32))
    phone = Column(String(11))
    password = Column(String(64))
    email = Column(String(32))
    level = Column(Integer, default=1)
    two_step = Column(Boolean, default=False)

    def toJSON(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'password': self.password,
            'email': self.email,
            'level': self.level
        }


class Token(Base):
    __tablename__ = 'tokens'
    token = Column(String(64), primary_key=True)
    create = Column(DateTime, default=datetime.datetime.utcnow())
    access = Column(DateTime, default=datetime.datetime.utcnow())
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', foreign_keys=[user_id])

    def toJSON(self):
        return {
            'token': self.token,
            'create': self.create,
            'access': self.access,
            'user_id': self.user_id,
            'user': self.user.toJSON()
        }

class TempUser(Base):
    __tablename__ = 'tempusers'
    id = Column(Integer, primary_key=True)
    phone = Column(String(11))
    code = Column(String(6))
    hash_string = Column(String(64))
    used = Column(Boolean , default=False)
    verified = Column(Boolean , default=False)

    def toJSON(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'code': self.code,
            'hash_string': self.hash_string,
            'used': self.used,
            'verified': self.verified
        }


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    card_num = Column(String(20))
    cvv2 = Column(Integer)
    exp_date = Column(String(10))
    name = Column(String(32))
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', foreign_keys=[user_id])

    def toJSON(self):
        return {
            'id': self.id,
            'card_num': self.card_num,
            'cvv2': self.cvv2,
            'exp_date': self.exp_date,
            'name': self.name,
            'user_id': self.user_id,
            'user': self.user.toJSON()
        }


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', foreign_keys=[user_id])
    balance = Column(Integer, default=0)
    blocked_balance = Column(Integer, default=0)

    def toJSON(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.toJSON(),
            'balance': self.balance,
            'blocked_balance': self.blocked_balance
        }


class Investment(Base):
    __tablename__ = 'investments'
    id = Column(Integer, primary_key=True)
    value = Column(Integer, default=0)
    broker = Column(String(16))
    current_profit = Column(Float , default=0)
    account_id = Column(Integer, ForeignKey(Account.id))
    account = relationship('Account', foreign_keys=[account_id])

    def toJSON(self):
        return {
            'id': self.id,
            'value': self.value,
            'broker': self.broker,
            'current_profit': self.current_profit,
            'account_id': self.account_id,
            'account': self.account
        }

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    snd_acc_id = Column(Integer, ForeignKey(Account.id))
    snd_acc = relationship('Account', foreign_keys=[snd_acc_id])
    rcv_acc_id = Column(Integer , ForeignKey(Account.id))
    rcv_acc = relationship('Account', foreign_keys=[rcv_acc_id])
    value = Column(String(16) , default=0)
    creation_time = Column(DateTime, default=datetime.datetime.utcnow())

    def toJSON(self):
        return {
            'id': self.id,
            'value': self.value,
            'snd_acc_id': self.snd_acc_id,
            'snd_acc': self.snd_acc.toJSON(),
            'rcv_acc_id': self.rcv_acc_id,
            'rcv_acc': self.rcv_acc.toJSON(),
            'creation_time': self.creation_time
        }

class TransactionToken(Base):
    __tablename__ = 'transaction_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    creation_time = Column(DateTime , default=datetime.datetime.utcnow())
    public_key = Column(String(64))
    private_key = Column(String(64))

    def toJSON(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id,
            'creation_time': self.creation_time,
            'public_key': self.public_key,
            'private_key': self.private_key
        }


class Factor(Base):
    __tablename__ = 'factors'
    id = Column(Integer, primary_key=True)
    snd_acc_id = Column(Integer, ForeignKey(Account.id))
    snd_acc = relationship('Account', foreign_keys=[snd_acc_id])
    rcv_acc_id = Column(Integer , ForeignKey(Account.id) , nullable=True)
    rcv_acc = relationship('Account' , foreign_keys=[rcv_acc_id])
    transaction_id = Column(Integer , ForeignKey(Transaction.id))
    value = Column(Integer, default=0)
    details = Column(String(128))
    create_time = Column(DateTime, default=datetime.datetime.utcnow())
    pay_time = Column(DateTime, nullable=True)
    tried = Column(Boolean , default=False)
    successfull = Column(Boolean, default=False)

    def toJSON(self):
        return {
            'value': self.value,
            'snd_acc_id': self.snd_acc_id,
            'snd_acc': self.snd_acc.toJSON(),
            'rcv_acc_id': self.rcv_acc_id,
            'rcv_acc': self.rcv_acc.toJSON(),
            'creation_time': self.create_time,
            'transaction_id': self.transaction_id,
            'details': self.details,
            'pay_time': self.pay_time,
            'tried': self.tried,
            'successfull': self.successfull
        }






