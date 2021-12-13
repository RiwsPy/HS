import requests
import json

def call_external_api(url: str):
    return requests.get(url)

def call_api():
    req = call_external_api("https://api.hearthstonejson.com/v1/latest/frFR/cards.json")
    if req.status_code == 200:
        print('DB updating...')
        with open('db/hearthstone.json', 'w') as file:
            json.dump(req.json(), file, ensure_ascii=False, separators=(',', ':'))
        print('End Updating.')
    else:
        print(f'Unexpected request status code : {req.status_code}')

def save_battlegrounds_cards():
    print('DB updating...')
    with open('db/battlegrounds_extended.json', 'r') as file:
        my_data = json.load(file)
    battlegrounds_dbfId = set(my_data)

    with open('db/hearthstone.json', 'r') as file:
        all_cards = json.load(file)
    all_to_battlegrounds = []
    card_data = {}
    unknow_dbfId = {}
    for card in all_cards:
        dbfId = card['dbfId']
        if str(dbfId) in battlegrounds_dbfId:
            battlegrounds_dbfId.discard(str(dbfId))
            card_data[str(dbfId)] = card
            all_to_battlegrounds.append(card)
        elif card['set'] == "BATTLEGROUNDS" and card.get('battlegroundsSkinParentId') is None:
            unknow_dbfId[dbfId] = card['name']


    with open('db/battlegrounds.json', 'w') as file:
        json.dump(all_to_battlegrounds, file, indent=1, ensure_ascii=False)

    for dbfId, name in unknow_dbfId.items():
        print(f'  {dbfId}, {name}')
    print(f'{len(battlegrounds_dbfId)} dbfId non trouvés') # 18
    print(f'{len(unknow_dbfId)} éléments non implantés') # 291

    ret = []
    for dbfId, value in my_data.items():
        value['dbfId'] = int(value.get('dbfId', dbfId))
        if 'mechanics' in value and 'mechanics' in card_data.get(dbfId, {}):
            card_data[dbfId]['mechanics'].extend(value['mechanics'])
        ret.append({**value, **card_data.get(dbfId, {})})

    ## PATCH
    print('PATCH')
    patchs = {58424: {'battlegroundsNormalDbfId':59687}}
    for dbfId, data in patchs.items():
        for card in ret:
            if card['dbfId'] == dbfId:
                for attr, value in data.items():
                    print(card['name'], f'- {attr} : {card[attr]} > {value}')
                    card[attr] = value
    print('END PATCH')

    with open('db/HStat.json', 'w') as file:
        json.dump(ret, file, indent=1, ensure_ascii=False)
    print('End Updating.')
