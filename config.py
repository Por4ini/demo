import json


with open("user_data.json", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data['tokens']:
        token = item['access_token']
        OLX_TOKEN = token  # Здесь я получаю токен с каждого зарегестрированного пользователя

BOT_TOKEN = '5565987951:AAG62U6BwKd_mkIItBf08GzCcEVeaDZi8o4'

