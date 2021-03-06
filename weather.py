# Author: Alan Cunningham
# Date 30/05/2016

import requests
import json
from datetime import datetime
import configparser
import random

class Weather:
    result = None


    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.py')
        url = "https://api.forecast.io/forecast/"

        api_key = config.get('weather', 'api_key')
        lon = config.get('weather', 'location_lon')
        lat = config.get('weather', 'location_lat')
        units = config.get('weather', 'units')

        # Make the initial weather request
        request_url = url + api_key + "/" + lat + "," + lon + "?units=" + units
        r = requests.get(request_url)
        resp = requests.get(url=request_url)
        self.result = json.loads(resp.text)
        print('TIMEZONE: %s' % self.result['timezone'])

        self.suggest_clothes()

    def get_current_weather(self):
        current_weather = self.result["currently"]
        return current_weather

    def get_daily_weather(self):
        daily_weather = self.result["daily"]["data"][0]
        return daily_weather

    def get_hourly_weather(self):
        hourly_weather = self.result["hourly"]["data"]
        for keys in hourly_weather:
            keys["time"] = self.convert_epoch(keys["time"])
        return hourly_weather

    def convert_epoch(self, epoch_time):
        converted = datetime.fromtimestamp(epoch_time).strftime('%H:%M')
        return converted

    # Suggest clothes based on the weather.
    def suggest_clothes(self):
        suggestions = []
        daily = self.get_daily_weather()

        # Average weather of the day
        avg_temp = (daily["apparentTemperatureMin"] + daily[
            "apparentTemperatureMax"]) / 2
        rain_chance = daily["precipProbability"]

        # We should extract these out into something configurable
        # Temperature based
        if avg_temp < 10:
            suggestions.append("a coat")
        elif avg_temp >= 10 and avg_temp < 17:
            suggestions.append("a jumper or a shirt")
        elif avg_temp >= 17 and avg_temp < 20:
            suggestions.append("a t-shirt and jeans")
        else:
            suggestions.append("a t-shirt and shorts")
        # Rain
        if rain_chance > 0.4:
            suggestions.append(". Probably best to bring your umbrella too")

        intro = [
            "I'd suggest you wear",
            "I'd recommend you wear"
        ]
        suggestion = intro[random.randint(0, len(intro)-1)] + "".join(suggestions)
        return suggestion


    def get_weather_string(self):
        daily_weather = self.get_daily_weather()
        summary = daily_weather['summary']
        chance_of_rain = int(daily_weather['precipProbability'] * 100)
        full_weather = "Today will be %s with a %s percent chance of rain. %s" \
                       % (
                           summary, chance_of_rain, self.suggest_clothes())
        return full_weather