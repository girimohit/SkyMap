from django.shortcuts import render
import datetime
import requests

# forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"


def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    )

    foreurl = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city2", None)

        weather_data1, daily_forecast1 = WeatherDetails(
            city1, API_KEY, current_weather_url, foreurl
        )

        if city2:
            weather_data2, daily_forecast2 = WeatherDetails(
                city2, API_KEY, current_weather_url, foreurl
            )
        else:
            (weather_data2, daily_forecast2) = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecast1": daily_forecast1,
            "weather_data2": weather_data2,
            "daily_forecast2": daily_forecast2,
        }

        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def WeatherDetails(city, api_key, current_weather_url, foreurl):
    # foreurl = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    response = requests.get(current_weather_url.format(city, api_key)).json()

    if "coord" in response:
        lat = round(response["coord"]["lat"])
        lon = round(response["coord"]["lon"])
    else:
        lat, lon = 13.41, 52.52
    forecast_response = requests.get(foreurl.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperture": round(response["main"]["temp"] - 273.15),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"],
    }

    daily_forecasts = []

    for daily_data in forecast_response["list"][:5]:
        daily_forecasts.append(
            {
                "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
                "min_temp": round(daily_data["main"]["temp_min"] - 273.15, 2),
                "max_temp": round(daily_data["main"]["temp_max"] - 273.15, 2),
                "description": daily_data["weather"][0]["description"],
                "icon": daily_data["weather"][0]["icon"],
            }
        )

    return weather_data, daily_forecasts
