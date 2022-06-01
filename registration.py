import json

user_data = {  #Эту инфу нужно принимать от пользователя
    "grant_type": "refresh_token",
    "client_id": "200782",
    "client_secret": "nn9shIZOVR8krr2IcNbWNEhMKNJi0i8scfr8GpB0NwFiMEgh",
    "refresh_token": "6ab55bfcbf9ce614dfab46fdd570fbb8f191827d"
}


def new(user_data):
    with open("user_data.json", encoding="utf-8") as f:
        json_data = json.load(f)
        print(json_data)
        count = 0
        for item in json_data['users']:
            if item['client_id'] == user_data['client_id']:
                print('Такой пользователь уже существует')
                count = +1
                break
            else:
                continue

        if count == 0:
            json_data['users'].append(user_data)
        with open('user_data.json', 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=2, ensure_ascii=False)


def edit():
    pass


def info():
    pass


new(user_data)
