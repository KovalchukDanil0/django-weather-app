import requests
from django.http import HttpRequest
from django.shortcuts import render


def parse_weather_code(code: int):
    weather_description = "Not Available"

    match code:
        case 0:
            weather_description = "Clear sky"
        case 1:
            weather_description = "Mainly clear"
        case 2:
            weather_description = "Partly cloudy"
        case 3:
            weather_description = "Overcast"
        case 45:
            weather_description = "Fog"
        case 48:
            weather_description = "Depositing rime fog"
        case 51:
            weather_description = "Drizzle: light"
        case 53:
            weather_description = "Drizzle: moderate"
        case 55:
            weather_description = "Drizzle: dense intensity"
        case 56:
            weather_description = "Freezing Drizzle: light"
        case 57:
            weather_description = "Freezing Drizzle: dense intensity"
        case 61:
            weather_description = "Rain: slight"
        case 63:
            weather_description = "Rain: moderate"
        case 65:
            weather_description = "Rain: heavy intensity"
        case 66:
            weather_description = "Freezing Rain: light"
        case 67:
            weather_description = "Freezing Rain: heavy intensity"
        case 71:
            weather_description = "Snow fall: slight"
        case 73:
            weather_description = "Snow fall: moderate"
        case 75:
            weather_description = "Snow fall: heavy intensity"
        case 77:
            weather_description = "Snow grains"
        case 80:
            weather_description = "Rain showers: slight"
        case 81:
            weather_description = "Rain showers: moderate"
        case 82:
            weather_description = "Rain showers: violent"
        case 85:
            weather_description = "Snow showers slight"
        case 86:
            weather_description = "Snow showers heavy"
        case 95:
            weather_description = " Thunderstorm: Slight or moderate"
        case 96:
            weather_description = "Thunderstorm slight"
        case 99:
            weather_description = "Thunderstorm heavy hail"

    return weather_description


def index(request: HttpRequest, template_name="app/home.html"):
    ip_address = request.META.get("REMOTE_ADDR")

    ip_info = requests.get(f"http://ip-api.com/json/{ip_address}").json()

    print(ip_info)

    try:
        lat = ip_info["lat"]
        lon = ip_info["lon"]
        timezone = ip_info["timezone"]
    except KeyError:
        lat = 0
        lon = 0
        timezone = "GMT"

    open_meteo = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&timezone={timezone}&current=temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m"
    ).json()

    try:
        temperature = int(open_meteo["current"]["temperature_2m"])
        weather_code = open_meteo["current"]["weather_code"]
        humidity = open_meteo["current"]["relative_humidity_2m"]
        wind_speed = open_meteo["current"]["wind_speed_10m"]

        temperature_unit = open_meteo["current_units"]["temperature_2m"]
        wind_speed_unit = open_meteo["current_units"]["wind_speed_10m"]
    except KeyError:
        temperature = 0
        weather_code = 0
        humidity = 0
        wind_speed = 0

        temperature_unit = "°C"
        wind_speed_unit = "km/h"

    weather_description = parse_weather_code(weather_code)

    args = {
        "temperature": temperature,
        "timezone": timezone,
        "weather_description": weather_description,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "temperature_unit": temperature_unit,
        "wind_speed_unit": wind_speed_unit,
    }
    return render(request, template_name, args)
