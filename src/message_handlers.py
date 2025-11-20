import requests
from aiogram import types
from src.api_tokens import open_weather_map, time_zone  # -- Токены
from src.api_func import open_weather_map_api, time_zone_api  # -- Функции для работы с api
from src.servicec import joiner, \
    spliter  # -- Склеивание названий San Francisco -> San+Francisco и разделитель для timezone


async def weather_map(api_token: str, message: types.Message, ur_index: int):
    city_query = joiner(message.text.split(' '), ur_index)
    if not city_query:
        return IndexError  # -- Не указанный город

    try:
        # api функции
        weather_map_response = open_weather_map_api(city=city_query, token=api_token)
        weather_map_json = weather_map_response.json()

        # проверка ответа от сервера
        if weather_map_response.status_code != 200:
            return KeyError

        # api функция которая выводит инфу о time zone
        timezone = time_zone_api(weather_map_json['coord']['lon'], weather_map_json['coord']['lat'], token=time_zone)
        timezone_split = spliter(timezone['timezone']['currentLocalTime'])  # Делим текущее время
        await message.answer(f"""
City: {weather_map_json['name']}
Region: {weather_map_json['sys']['country']}
Time Zone: {timezone['timezone']['timezoneName']}
Local Time: {timezone_split[0]} : {timezone_split[1]}
Weather: {weather_map_json['weather'][0]['main']}
Description: {weather_map_json['weather'][0]['description']}
Temp °C: {weather_map_json['main']['temp']}
Feels Like °C: {weather_map_json['main']['feels_like']}
Wind Speed: {weather_map_json['wind']['speed']}
""")
    except IndexError:
        # при отсутствии данных
        return IndexError
    except KeyError:
        # не найден в api
        return KeyError
    except requests.exceptions.Timeout:
        await message.answer("Ошибка: время ожидания ответа превышено\nИзвините это не ваша проблема это наша "
                             "проблема в попытке связаться\nс серверами openweathermap")
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка: не удалось подключиться к серверу")
    except requests.exceptions.RequestException as e:
        print(f"Другая ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


async def handle_start(message: types.Message):
    await message.answer(
        '''
Привет! Я PyWeather бот
ТЫ можешь посмотреть погоду в любом городе
отправь мне комманду /weather или /w {город} или просто {город}''')


async def weather(message: types.Message):
    result = await weather_map(api_token=open_weather_map, message=message, ur_index=1)
    if result == IndexError:
        await message.reply('Вы не указали город!\n/w {город}\nили просто - \n{город}')
    elif result == KeyError:
        await message.reply('''
Комманда или город не найдены!
Чтобы посмотреть погоду в любом городе отправь мне комманду
/weather {город} или /w {город} а также можно просто
{город} ''')


async def none_command(message: types.Message):
    result = await weather_map(api_token=open_weather_map, message=message, ur_index=0)
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
