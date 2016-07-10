from flask import Flask, request, jsonify
from .cardfetcher_utils import *

app = Flask('magictheslackening')

GATHERER_IMG_TPL = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={}&type=card'
CARD_NOT_FOUND_ERR_TPL = 'Whoops, looks like {} isn\'t a magic card'
MTGSTOCKS_LINK_TPL = '<{}|MTGStocks.com> price for {}'

@app.route('/cardimage', methods=['POST'])
def fetch_card_image():
    searchname = request.form['text']
    card_obj = get_card_obj(searchname)

    if not card_obj:
        return jsonify({
            'response_type': 'in_channel',
            'text': CARD_NOT_FOUND_ERR_TPL.format(searchname),
        })

    img_url = GATHERER_IMG_TPL.format(card_obj['id'])

    attachments = [{
        'fallback': card_obj['name'],
        'image_url': img_url
    }]

    resp = {
        'response_type': 'in_channel',
        'text': '',
        'attachments': attachments,
    }

    return jsonify(resp)

@app.route('/oracletext', methods=['POST'])
def fetch_oracle_text():

    searchname = request.form['text']

    print(searchname)

    card_obj = get_card_obj(searchname)

    if not card_obj:
        return jsonify({
            'response_type': 'in_channel',
            'text': CARD_NOT_FOUND_ERR_TPL.format(searchname),
        })

    print(card_obj)

    card_attachment = {
        'fallback': card_obj['name'],
        'title': card_obj['name'],
        'fields': [
            {
                'title': 'Mana Cost',
                'value': format_mana(card_obj['manaCost']),
                'short': True
            },
            {
                'title': 'Types',
                'value': '{} - {}'.format(card_obj['type'], card_obj['subType']),
                'short': True
            },
            {
                'title': 'Text',
                'value': format_mana(card_obj['description']),
                'short': False
            }
        ]
    }

    if 'Creature' in card_obj['type']:
        card_attachment['fields'].append({
            'title': 'P/T',
            'value': '{}/{}'.format(card_obj['power'], card_obj['toughness']),
            'short': True
        })
    if 'Planeswalker' in card_obj['type']:
        card_attachment['fields'].append({
            'title': 'Loyalty',
            'value': card_obj['loyalty'],
            'short': True
        })


    resp = {
        'response_type': 'in_channel',
        'text': '',
        'attachments': [card_attachment],
    }

    return jsonify(resp)

@app.route('/cardprice', methods=['POST'])
def fetch_card_price():
    searchname = request.form['text']

    args = searchname.split(':')[:2]
    card_obj = get_card_price(*args)

    if not card_obj:
        return jsonify({
            'response_type': 'in_channel',
            'text': CARD_NOT_FOUND_ERR_TPL.format(searchname),
        })

    prices = card_obj['prices']

    card_attachment = {
        'fallback': card_obj['name'],
        'title': card_obj['name'],
        'fields': [
            {
                'title': 'Set',
                'value': card_obj['set'],
                'short': True
            },
            {
                'title': 'Average',
                'value': prices['avg'],
                'short': True
            }
        ]
    }

    if not card_obj['promo']:
        card_attachment['fields'].extend(
            [
                {
                    'title': 'Low',
                    'value': prices['low'],
                    'short': True
                },
                {
                    'title': 'High',
                    'value': prices['high'],
                    'short': True
                }
            ]
        )

    resp = {
        'response_type': 'in_channel',
        'text': '',
        'attachments': [card_attachment],
    }

    return jsonify(resp)


