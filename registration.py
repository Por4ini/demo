import json
import requests


def new(user_data):
    with open("user_data.json", encoding="utf-8") as f:
        json_data = json.load(f)
        count = 0
        for item in json_data['users']:
            if item['client_id'] == user_data['client_id']:
                count = +1
                break
            else:
                continue

        if count == 0:
            json_data['users'].append(user_data)
        with open('user_data.json', 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=2, ensure_ascii=False)


def refresh_token():
    with open('user_data.json') as outfile:
        json_data = json.load(outfile)
        json_data['tokens'].clear()

    with open('user_data.json', 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, indent=2, ensure_ascii=False)
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
            data = {
                "access_token": 'Bearer ' + callback['access_token']}
            with open("user_data.json", encoding="utf-8") as f:
                json_data = json.load(f)
                count = 0
                for item in json_data['tokens']:
                    if item['access_token'] == data['access_token']:
                        count = +1
                        break
                    else:
                        continue

                if count == 0:
                    json_data['tokens'].append(data)
            with open('user_data.json', 'w', encoding='utf-8') as outfile:
                json.dump(json_data, outfile, indent=2, ensure_ascii=False)


def del_user(del1):
    with open("user_data.json", encoding="utf-8") as f:
        json_data = json.load(f)

    for item in json_data['users']:

        if item['client_id'] != del1:
            item_id = item['client_id']
            with open('buffer_data.json', encoding='utf-8') as f:
                buffer_data = json.load(f)
                count = 0
                for item in buffer_data['users']:
                    if item['client_id'] == item_id:
                        count = +1
                    else:
                        continue
                if count == 0:
                    buffer_data['users'].append(item)
                with open('buffer_data.json', 'w', encoding='utf-8') as outfile:
                    json.dump(buffer_data, outfile, indent=2, ensure_ascii=False)
        else:
            continue

    with open('user_data.json') as outfile:
        json_data = json.load(outfile)
        json_data['users'].clear()
        with open('user_data.json', 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=2, ensure_ascii=False)
    with open("buffer_data.json", encoding="utf-8") as f:
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
        with open("user_data.json", encoding="utf-8") as f:
            json_data = json.load(f)
            json_data['users'].append(user_data)
            with open('user_data.json', 'w', encoding='utf-8') as outfile:
                json.dump(json_data, outfile, indent=2, ensure_ascii=False)

    with open("buffer_data.json", encoding="utf-8") as f:
        buf_data = json.load(f)
        buf_data['users'].clear()
    with open('buffer_data.json', 'w', encoding='utf-8') as outfile:
        json.dump(buf_data, outfile, indent=2, ensure_ascii=False)
