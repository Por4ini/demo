import requests
import json

with open("user_data.json", encoding="utf-8") as f:
    json_data = json.load(f)
    for item in json_data['users']:
        client_id = item['client_id']
        client_secret = item['client_secret']
        refresh_token = item['refresh_token']

user_data = {
    "grant_type": "refresh_token",
    "client_id": client_id,
    "client_secret": client_secret,
    "refresh_token": refresh_token
}

response = requests.post('https://www.olx.ua/api/open/oauth/token', json=user_data).text
callback = json.loads(response)
token = 'Bearer ' + callback['access_token']
data = {
    "access_token": 'Bearer ' + callback['access_token']}
with open("user_data.json", encoding="utf-8") as f:
    json_data = json.load(f)
    print(json_data)
    count = 0
    for item in json_data['tokens']:
        if item['access_token'] == data['access_token']:
            print('Такой token уже существует')
            count = +1
            break
        else:
            continue

    if count == 0:
        json_data['tokens'].append(data)
        print(json_data)
with open('user_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(json_data, outfile, indent=2, ensure_ascii=False)
