import asyncio
from aiogram.dispatcher import FSMContext
from states import register
import time
from get_message import get_info
from config import BOT_TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from registration import new, del_user, refresh_token
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Погнали')


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Добавь пользователя командой  /register\nПроверь активных пользователей командой /info\nЗапусти оповещение командой /go\nЧто бы удалить аккаунт Введи /del\n Если что то не рабоатет то /error укажет на ошибку\nУдачи")


@dp.message_handler(commands=['go'])
async def go(message: types.Message):
    while True:

        await asyncio.sleep(10)
        print('|')
        refresh_token()

        with open("user_data.json", encoding="utf-8") as f:
            json_data = json.load(f)
            for item in json_data['tokens']:
                token = item['access_token']
                get_info(token)
                for item in json_data['message']:
                    if item['send'] == 'false':
                        name = item['name']
                        text = item['text']
                        created_at = item['created_at']
                        my_name = item['my_name']
                        phone = item['phone']
                        title = item['title']

                        await bot.send_message(message.from_user.id,
                                               f'{title}\nКому: {my_name}|{phone}\nВ: {created_at}\nОт: {name}\nСообщение:  {text}')
                    elif item['send'] == 'true':
                        continue
                    else:
                        continue
                    with open('user_data.json', 'r+') as f:
                        item['send'] = 'true'
                        f.seek(0)
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
                        f.truncate()


@dp.message_handler(commands=['go'])
async def go_token(message: types.Message):
    while True:
        await asyncio.sleep(2)
        refresh_token()


@dp.message_handler(commands=['register'])
async def register_(message: types.Message):
    await message.answer('Введи client_id')
    await register.test1.set()


#
@dp.message_handler(state=register.test1)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text
    #
    await state.update_data(test1=answer)
    await message.answer('Client_secret')
    await register.test2.set()


#
@dp.message_handler(state=register.test2)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(test2=answer)
    await message.answer('Refresh_token')
    await register.test3.set()


@dp.message_handler(state=register.test3)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(test3=answer)

    data = await state.get_data()
    test1 = data.get('test1')
    test2 = data.get('test2')
    test3 = data.get('test3')
    await message.answer(f'client_id--{test1}\n client_secret{test2}\nrefresh_token{test3}')

    user_data = {
        "grant_type": "refresh_token",
        "client_id": f"{test1}",
        "client_secret": f"{test2}",
        "refresh_token": f"{test3}"
    }
    new(user_data)
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
    print("Новый в семье")
    await state.finish()


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    with open("user_data.json", encoding="utf-8") as f:
        json_data = json.load(f)
        for item in json_data['users']:
            client_id = item['client_id']
            client_secret = item['client_secret']
            refresh_token = item['refresh_token']
            await bot.send_message(message.from_user.id, f"Аккаунт:\n"
                                                         f"client_id:   {client_id}\nclient_secret:  {client_secret}\nrefresh_token:  {refresh_token}")
            print("Пошла инфа")


@dp.message_handler(commands=['del'])
async def delete_(message: types.Message):
    await message.answer('Введи client_id')
    await register.del1.set()


@dp.message_handler(state=register.del1)
async def delete_(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(del1=answer)
    data = await state.get_data()
    del1 = data.get('del1')
    del_user(del1)
    print("-1")
    await state.finish()


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    await message.answer('Что дальше делаем?')


@dp.message_handler(commands=['error'])
async def error(message: types.Message):
    await message.answer('Пора обновить токены')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(go())

    except KeyError:
        asyncio.ensure_future(error())


    except NameError:
        asyncio.ensure_future(register_())
    finally:
        loop.close(stop())
