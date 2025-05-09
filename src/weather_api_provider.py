import requests
import json

class WeatherAPIError(Exception):
    pass

class WeatherProvider:
    OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"

    def prediction_for(self, lat, lon):
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean",
            "forecast_days": 7
        }

        response = requests.get(self.OPEN_METEO_API_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise WeatherAPIError(data["reason"])

        return self._unpack_response_data(data)

    def _unpack_response_data(self, data):
        daily = data["daily"]

        result = {}
        for i, day in enumerate(daily["time"]):
            result[day] = {
                "min": daily["temperature_2m_min"][i],
                "mean": daily["temperature_2m_mean"][i],
                "max": daily["temperature_2m_max"][i]
            }
        return result
