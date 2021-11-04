import requests
import json

def call_api():
    req = requests.get("https://api.hearthstonejson.com/v1/latest/frFR/cards.json")
    if req.status_code == 200:
        print('DB updating...')
        with open('db/hearthstone.json', 'w') as file:
            json.dump(req.json(), file, ensure_ascii=False, separators=(',', ':'))
        print('End Updating.')
    else:
        print(f'Strange request status code : {req.status_code}')

def save_battlegrounds_cards():
    print('DB updating...')
    with open('db/battlegrounds_extended.json', 'r') as file:
        data = json.load(file)
    battlegrounds_cards = set(data.keys())

    with open('db/hearthstone.json', 'r') as file:
        all_cards = json.load(file)
    lst = []
    dic = {}
    unknow_dbfId = {}
    for card in all_cards:
        dbfId = card['dbfId']
        if str(dbfId) in battlegrounds_cards:
            battlegrounds_cards.discard(str(dbfId))
            dic[str(dbfId)] = card
            lst.append(card)
        elif card['set'] == "BATTLEGROUNDS":
            unknow_dbfId[dbfId] = card['name']


    with open('db/battlegrounds.json', 'w') as file:
        json.dump(lst, file, indent=1, ensure_ascii=False)
    print(f'{len(battlegrounds_cards)} dbfId non trouvés') # 19
    print(f'{len(unknow_dbfId)} éléments inconnus') # 186 > 168 > 353
    for dbfId, name in unknow_dbfId.items():
        print(f'  {dbfId}, {name}')

    ret = []
    for key, value in data.items():
        value['dbfId'] = int(value.get('dbfId', key))
        if 'mechanics' in value and 'mechanics' in dic.get(key, {}):
            dic[key]['mechanics'].extend(value['mechanics'])
        ret.append({**value, **dic.get(key, {})})
    with open('db/HStat.json', 'w') as file:
        json.dump(ret, file, indent=1, ensure_ascii=False)
    print('End Updating.')
