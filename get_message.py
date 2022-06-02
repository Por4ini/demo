import requests
import json


def get_info(token):
    headers = {"Authorization": token,
               "Version": "v 2"}

    response = requests.get('https://www.olx.ua/api/partner/users/me', headers=headers).text
    my_info = json.loads(response)
    my_name = my_info['data']['name']
    my_phone = my_info['data']['phone']
    response = requests.get('https://www.olx.ua/api/partner/threads', headers=headers).text
    chats = json.loads(response)['data']
    for item in chats:
        if item['unread_count'] >= 1:

            interlocutor_id = item['interlocutor_id']
            id = item['id']
            advert_id = item['advert_id']
            link_user = f'https://www.olx.ua/api/partner/users/{interlocutor_id}'
            res = requests.get(link_user, headers=headers).text
            info_user = json.loads(res)['data']
            name = info_user['name']  # имя отправителя
            link_advert = f'https://www.olx.ua/api/partner/adverts/{advert_id}'
            res2 = requests.get(link_advert, headers=headers).text
            info_advert = json.loads(res2)['data']
            title = info_advert['title']

            res1 = requests.get(f'https://www.olx.ua/api/partner/threads/{id}/messages', headers=headers).text
            get_text = json.loads(res1)
            for item in get_text['data']:
                mess_id = item['id']
                text = item['text']  # получаю текст сообщения
                created_at = item['created_at']

            value = {
                'title': title,
                'id': mess_id,
                'name': name,
                'text': text,
                'created_at': created_at,
                'my_name': my_name,
                'phone': my_phone,
                'send': 'false',
            }

            with open("user_data.json", encoding="utf-8") as f:
                json_data = json.load(f)
                value_id = value['id']
            count = 0
            for i_id in json_data['message']:
                if value_id == i_id['id']:
                    count = +1
                    break
                else:
                    continue
            if count == 0:
                json_data['message'].append(value)
                with open('user_data.json', 'w', encoding='utf-8') as outfile:
                    json.dump(json_data, outfile, indent=2, ensure_ascii=False)
            else:
                pass


