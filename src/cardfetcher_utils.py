import requests
import re

'''
Query a web API for a card with the given name
Implementation subject to change as various MTG APIs are created and destroyed
Should always return a JSON in the mtgdb.info format:

*id                 Integer     : multiverse Id
*name               String      : name of the card
*description        String      : the cards actions
*manaCost           String      : the description of mana to cast spell
*type               String      : the type of card
*subType            String      : subtype of card
*power              Integer     : attack strength
*toughness          Integer     : defense strength
*loyalty            Integer     : loyalty points usually on planeswalkers


* indicates properties that are currently in use and must be present in the returned json
'''
def get_card_obj(cardname):

    query_url = 'https://api.deckbrew.com/mtg/cards?name={}'.format(cardname)
    r = requests.get(query_url)

    if (r.status_code != requests.codes.ok) or (not r.json()):
        return None

    api_json = next((card for card in r.json() if card['name'].lower() == cardname.lower()), None)

    if (api_json is None):
        if (len(r.json()) > 0):
            api_json = r.json()[0]
        else:
            return None

    formatted_json = {
        'id': api_json['editions'][0]['multiverse_id'],
        'name': api_json['name'],
        'description': api_json['text'],
        'manaCost': api_json['cost'],
        'type': (' ').join(api_json.get('types', [])).title(),
        'subType': (' ').join(api_json.get('subtypes', [])).title(),
        'power': api_json.get('power', ''),
        'toughness': api_json.get('toughness', ''),
        'loyalty': api_json.get('loyalty', '')
    }

    return formatted_json


def get_card_price(cardname, setname=None):
    query_url = 'http://mtg-price-fetcher.us-west-1.elasticbeanstalk.com/cards'
    params = {'name': cardname }

    if (setname):
        params['set'] = setname

    r = requests.get(query_url, params)

    if (r.status_code != requests.codes.ok) or (not r.json()):
        return None

    return r.json()


# replaces all manacost sequences (denoted by characters or numbers wrapped in {})
# with the appropriate manacost emoticons
def format_mana(string):
    return re.sub(r'\{(.+?)\}', format_mana_symbol, string)

# accepts a mana/tap symbol in gathererer "curly brace" format and
# returns the equivalent slack-emoji formatted symbol
def format_mana_symbol(match):
    sym = match.group(0).lower()
    sym = re.sub(r'[{}]', '', sym)

    if (len(sym) == 3 and sym[1] == '/'):
        sym = re.sub(r'\/', '', sym)

    if (len(sym) == 2 and sym[1] == 'p'):
        sym = sym[::-1]

    if (sym == 't'):
        return ':tap:'
    elif (sym == 'q'):
        return ':untap:'
    else:
        return ':{}mana:'.format(sym)
