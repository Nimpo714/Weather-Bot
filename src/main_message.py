import requests
from aiogram import types
from src.api_tokens import time_zone_token  # -- Токен
from src.api_func import owm_current_api, time_zone_api  # -- Функции для работы с api
from src.servicec import joiner, spliter, f_e


async def weather_map(api_token: str, message: types.Message, ur_index: int, emoji_dec):
    """ main message from bot """
    city_query = joiner(message.text.split(' '), ur_index)
    if not city_query:
        return IndexError  # -- Не указанный город

    try:
        # api функции
        weather_map_response = owm_current_api(city=city_query, token=api_token)
        weather_map_json = weather_map_response.json()

        # проверка ответа от сервера
        if weather_map_response.status_code != 200:
            return KeyError

        # api функция которая выводит инфу о time zone
        timezone = time_zone_api(weather_map_json['coord']['lon'], weather_map_json['coord']['lat'], token=time_zone_token)
        timezone_split = spliter(timezone['timezone']['currentLocalTime'])  # Делим текущее время

        #  -- main message
        await message.answer(f"""
{f_e(emoji_dec[0])} City: {weather_map_json['name']}
{f_e(emoji_dec[1])} Region: {weather_map_json['sys']['country']}
{f_e(emoji_dec[2])} Time Zone: {timezone['timezone']['timezoneName']}
{f_e(emoji_dec[3])} Local Time: {timezone_split[0]} : {timezone_split[1]}
{f_e(emoji_dec[4])} Weather: {weather_map_json['weather'][0]['main']}
{f_e(emoji_dec[5])} Description: {weather_map_json['weather'][0]['description']}
{f_e(emoji_dec[6])} Temp[ °C: {weather_map_json['main']['temp']}
{f_e(emoji_dec[7])} Feels Like °C: {weather_map_json['main']['feels_like']}
{f_e(emoji_dec[8])} Wind Speed: {weather_map_json['wind']['speed']}
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
