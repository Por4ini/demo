import json


with open("user_data.json", encoding="utf-8") as f:
    json_data = json.load(f)

    for item in json_data['tokens']:
        OLX_TOKEN = item['access_token']

BOT_TOKEN = '1919741382:AAGKh7amERxr_31v7XaPZT17U3wahRKT8Ig'