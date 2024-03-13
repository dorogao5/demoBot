import openmeteo_requests
import requests

import requests_cache
import time as tm
from retry_requests import retry


def get_weather(city_name):
    # get city location
    try:
        city_data = requests.get(
            f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json').json()
        results = city_data['results'][0]
        city_latitude = results['latitude']
        city_longitude = results['longitude']
    except KeyError:
        return 'Вы ввели некорректное название города'

    # Set up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city_latitude,
        "longitude": city_longitude,
        "current": ["apparent_temperature", "precipitation", "wind_speed_10m"],
        "hourly": ["temperature_2m", "precipitation"],
        "timezone": "Europe/Moscow",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_apparent_temperature = int(current.Variables(0).Value())
    current_precipitation = current.Variables(1).Value()
    current_wind_speed_10m = int(current.Variables(2).Value())

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
    weather = f'время  темп  осадки\n'
    h = tm.localtime().tm_hour
    for i in range(24):
        temperature = str(int(hourly_temperature_2m[i]))
        if i > h:
            weather += f'{i}:00    {temperature}°C    {int(hourly_precipitation[i])} \n'

    text = (f"Погода сейчас:\nТемпература на улице: {current_apparent_temperature} °C\n"
            f"Осадки: {current_precipitation} \n"
            f"Скорость ветра: {current_wind_speed_10m} м/с  \n\n" + weather)
    return text
