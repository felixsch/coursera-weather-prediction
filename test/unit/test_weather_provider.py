import pytest
import requests
import json
import os

from unittest import mock
from helpers import read_fixture_file
from weather_api_provider import WeatherProvider, WeatherAPIError

@pytest.fixture()
def request_mock():
    with mock.patch('requests.get') as m:
        yield m

@pytest.fixture
def valid_api_response():
    path = os.path.join(os.path.dirname(__file__), "valid_api_response.json")
    yield read_fixture_file(path)

@pytest.fixture
def invalid_api_response():
    path = os.path.join(os.path.dirname(__file__), "invalid_api_response.json")
    yield read_fixture_file(path)

def test_weather_provider_prediction_for(request_mock, valid_api_response):
    response = mock.Mock()
    response.json.return_value = valid_api_response
    response.raise_for_status.return_value = None
    request_mock.return_value = response

    provider = WeatherProvider()

    data = provider.prediction_for(12.5, 12.5)

    assert len(data) == 7
    assert data["2025-05-08"]["min"] == 22.7


def test_weather_provider_prediction_for_invalid(request_mock, invalid_api_response):
    response = mock.Mock()
    response.json.return_value = invalid_api_response
    response.raise_for_status.return_value = None
    request_mock.return_value = response

    provider = WeatherProvider()

    try:
        # out of range
        data = provider.prediction_for(10000, 12.5)
    except WeatherAPIError as err:
        assert "Latitude must be in range" in str(err)
