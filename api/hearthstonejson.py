import requests
import json

def call_api():
    req = requests.get("https://api.hearthstonejson.com/v1/latest/frFR/cards.json")
    if req.status_code == 200:
        print('DB updating...')
        with open('db_hearthstone.json', 'w') as file:
            json.dump(req.json(), file, ensure_ascii=False, separators=(',', ':'))
        print('End Updating.')
    else:
        print(f'Strange request status code : {req.status_code}')

def save_battlegrounds_cards():
    print('DB updating...')
    with open('db_battlegrounds_extended.json', 'r') as file:
        data = json.load(file)
    battlegrounds_cards = set(data.keys())

    with open('db_hearthstone.json', 'r') as file:
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


    with open('db_battlegrounds.json', 'w') as file:
        json.dump(lst, file, indent=1, ensure_ascii=False)
    print(f'{len(battlegrounds_cards)} dbfId non trouvés') # 23
    print(f'{len(unknow_dbfId)} éléments inconnus') # 186
    for dbfId, name in unknow_dbfId.items():
        print(f'  {dbfId}, {name}')

    ret = []
    for key, value in data.items():
        value['dbfId'] = value.get('dbfId', key)
        ret.append({**value, **dic.get(key, {})})
    with open('db_HStat.json', 'w') as file:
        json.dump(ret, file, indent=1, ensure_ascii=False)
    print('End Updating.')
