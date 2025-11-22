import requests
from aiogram import types
from src.api_tokens import open_weather_map_token, time_zone_token  # -- Токены
from src.api_func import owm_current_api, time_zone_api  # -- Функции для работы с api
from src.servicec import joiner, \
    spliter  # -- Склеивание названий San Francisco -> San+Francisco и разделитель для timezone


async def weather_map(api_token: str, message: types.Message, ur_index: int):
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
