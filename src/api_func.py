import requests


def time_zone_api(lon: float, lat: float, token):
    """ do request to timezone_api """
    response = requests.get(
        f'https://api.mapy.com/v1/timezone/coordinate?lon={lon}&lat={lat}&lang=en&apikey={token}'
    ).json()
    return response


def owm_current_api(city: str, token: str):
    """ do request to open_weather_map """
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric')


def owm_forecast_api(date: str, token: str, lat: float, lon: float):
    """ do request to open_weather_map forecast """
    return requests.get(f'https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={token}&units=metric')