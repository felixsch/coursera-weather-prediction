import pytest
import requests
import json

from unittest import mock
from weather_api_provider import WeatherProvider, WeatherAPIError

def test_weather_provider_prediction_for(request_mock, fixture_from):
    response = mock.Mock()
    response.json.return_value = fixture_from("fixtures/valid_api_response.json")
    response.raise_for_status.return_value = None
    request_mock.return_value = response

    provider = WeatherProvider()

    data = provider.prediction_for(12.5, 12.5)

    assert len(data) == 7
    assert data["2025-05-08"]["min"] == 22.7


def test_weather_provider_prediction_for_invalid(request_mock, fixture_from):
    response = mock.Mock()
    response.json.return_value = fixture_from("fixtures/invalid_api_response.json")
    response.raise_for_status.return_value = None
    request_mock.return_value = response

    provider = WeatherProvider()

    try:
        # out of range
        data = provider.prediction_for(10000, 12.5)
    except WeatherAPIError as err:
        assert "Latitude must be in range" in str(err)
