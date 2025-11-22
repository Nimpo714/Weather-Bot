from aiogram import types
from src.api_tokens import open_weather_map_token  # -- Токены
from src.main_message import weather_map


async def handle_start(message: types.Message):
    await message.answer(
        '''
Привет! Я PyWeather бот
ТЫ можешь посмотреть погоду в любом городе
отправь мне комманду /weather или /w {город} или просто {город}''')


async def weather(message: types.Message):
    result = await weather_map(api_token=open_weather_map_token, message=message, ur_index=1)
    if result == IndexError:
        await message.reply('Вы не указали город!\n/w {город}\nили просто - \n{город}')
    elif result == KeyError:
        await message.reply('''
Комманда или город не найдены!
Чтобы посмотреть погоду в любом городе отправь мне комманду
/weather {город} или /w {город} а также можно просто
{город} ''')


async def none_command(message: types.Message):
    result = await weather_map(api_token=open_weather_map_token, message=message, ur_index=0)
    if result == KeyError:
        await message.reply('''
Комманда или город не найдены!
Чтобы посмотреть погоду в любом городе отправь мне комманду
/weather {город} или /w {город} а также можно просто
{город} ''')


# все комманды для main.py
def register_handlers(dp):
    dp.register_message_handler(handle_start, commands=['start'])
    dp.register_message_handler(weather, commands=['weather', 'w'])
    dp.register_message_handler(none_command)
