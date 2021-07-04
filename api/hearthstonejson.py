import requests
import json

def call_api():
    req = requests.get("https://api.hearthstonejson.com/v1/latest/frFR/cards.json")
    if req.status_code == 200:
        print('DB updating...')
        with open('bdd.json', 'w') as file:
            json.dump(req.json(), file, ensure_ascii=False, separators=(',', ':'))
    else:
        print(f'Strange request status code : {req.status_code}')

