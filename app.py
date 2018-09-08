from flask import Flask , Response, request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Noobs!'


# User //


@app.route('/api/user/request_sms', methods=['POST'])
def request_sms():
    from func import user
    resp = Response(user.request_sms())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/user/verify_sms', methods=['POST'])
def verify_sms():
    from func import user
    resp = Response(user.verify_sms())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/user/signup', methods=['POST'])
def signup():
    from func import user
    resp = Response(user.signup())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/user/login', methods=['POST'])
def login():
    from func import user
    resp = Response(user.login())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/user/get_user', methods=['POST'])
def get_user():
    from func import user
    resp = Response(user.get_user())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/user/get_data', methods=['POST'])
def get_data():
    from func import user
    resp = Response(user.get_data())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Card //


@app.route('/api/card/add_card', methods=['POST'])
def add_card():
    from func import card
    resp = Response(card.add_card())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/card/get_card', methods=['POST'])
def get_card():
    from func import card
    resp = Response(card.get_card())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/card/get_cards', methods=['POST'])
def get_cards():
    from func import card
    resp = Response(card.get_cards())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/card/remove_card', methods=['POST'])
def remove_card():
    from func import card
    resp = Response(card.remove_card())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Factor //


@app.route('/api/factor/add_factor', methods=['POST'])
def add_factor():
    from func import factor
    resp = Response(factor.add_factor())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/factor/participate_factor', methods=['POST'])
def participate_factor():
    from func import factor
    resp = Response(factor.participate_factor())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/factor/complete_factor', methods=['POST'])
def complete_factor():
    from func import factor
    resp = Response(factor.complete_factor())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/factor/get_factor', methods=['POST'])
def get_factor():
    from func import factor
    resp = Response(factor.get_factor())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/factor/get_factors', methods=['POST'])
def get_factors():
    from func import factor
    resp = Response(factor.get_factors())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Account //


@app.route('/api/account/add_account', methods=['POST'])
def add_account():
    from func import account
    resp = Response(account.add_account())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/account/charge_account', methods=['POST'])
def charge_account():
    from func import account
    resp = Response(account.charge_account())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/account/get_account', methods=['POST'])
def get_account():
    from func import account
    resp = Response(account.get_account())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/account/get_accounts', methods=['POST'])
def get_accounts():
    from func import account
    resp = Response(account.get_accounts())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Transactions //


@app.route('/api/transaction/participate_transaction', methods=['POST'])
def participate_transaction():
    from func import transaction
    resp = Response(transaction.participate_transaction())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/transaction/add_transaction', methods=['POST'])
def add_transaction():
    from func import transaction
    resp = Response(transaction.add_transaction())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/transaction/get_transaction', methods=['POST'])
def get_transaction():
    from func import transaction
    resp = Response(transaction.get_transaction())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/transaction/get_transactions', methods=['POST'])
def get_transactions():
    from func import transaction
    resp = Response(transaction.get_transactions())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Investments //


@app.route('/api/investment/add_investment', methods=['POST'])
def add_investment():
    from func import investment
    resp = Response(investment.add_investment())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/investment/get_investment', methods=['POST'])
def get_investment():
    from func import investment
    resp = Response(investment.get_investment())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/investment/get_investments', methods=['POST'])
def get_investments():
    from func import investment
    resp = Response(investment.get_investments())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run()
