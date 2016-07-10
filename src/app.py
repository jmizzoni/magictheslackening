from flask import Flask, request, jsonify
from .cardfetcher_utils import *

app = Flask('magictheslackening')

@app.route('/cardimage')
def fetch_card_image():
    resp = {
        'resptype': 'card image',
    }

    return jsonify(resp)

@app.route('/oracletext')
def fetch_oracle_text():
    resp = {
        'resptype': 'oracle text',
    }

    return jsonify(resp)

@app.route('/cardprice')
def fetch_card_price():
    resp = {
        'resptype': 'card price'
    }

    return jsonify(resp)


