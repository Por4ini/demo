import asyncio
from get_message import get_info
from config import OLX_TOKEN, BOT_TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types
import json
#___________________________________
# Бот которые собрает информацию из user_data и отправляет пользователю. Нужно дописать регистрацию, пока хз как через телегу принимать сообщения.
#__________________________________
OLX_TOKEN = OLX_TOKEN
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Начнем работу')


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Добавь пользователя командой  /registration\nПроверь активных пользователей командой /info\nЗапусти оповещение командой /go")


@dp.message_handler(commands=['go'])
async def go(message: types.Message):
    while True:

        with open("user_data.json", encoding="utf-8") as f:
            json_data = json.load(f)
            for item in json_data['tokens']:  #Хочу что бы отрабатывал сперва один токен, затем второй. Сейчас отрабатывает только первый!
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
                        await message
                    with open('user_data.json', 'r+') as f:
                        item['send'] = 'true'
                        f.seek(0)
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
                        f.truncate()
                print('процесс идет')


@dp.message_handler(commands=['registration'])
async def registration(message: types.Message):
    await bot.send_message(message.from_user.id, 'Эта функция еще не готова!')
    user_data = {}

    # with open('user_data.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(user_data, outfile, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    loop = asyncio.get_event_loop()
    loop.create_task(go(45))
