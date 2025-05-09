import pytest

from unittest import mock
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_prediction_redirect(live_server, request_mock, fixture_from):
    options = Options()
    options.add_argument("--headless")

    response = mock.Mock()
    response.json.return_value = fixture_from("fixtures/valid_api_response.json")
    response.raise_for_status.return_value = None
    request_mock.return_value = response

    live_server.start()
    driver = webdriver.Firefox(options=options)
    driver.get(live_server.url())

    lat_input = driver.find_element(By.ID, "lat")
    lon_input = driver.find_element(By.ID, "lon")
    submit_button = driver.find_element(By.ID, "predict")

    lat_input.send_keys("12.5")
    lon_input.send_keys("12.5")

    submit_button.click()

    assert live_server.url() in driver.current_url

    driver.quit()
