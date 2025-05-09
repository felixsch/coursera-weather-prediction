import json
import pytest
import os

from unittest import mock
from app import app as app_def

@pytest.fixture(scope="session")
def app():
    app_def.config["TESTING"] = True
    with app_def.app_context():
        yield app_def

@pytest.fixture()
def request_mock():
    with mock.patch('requests.get') as m:
        yield m

@pytest.fixture
def fixture_from():
    yield lambda file: read_fixture_file(
        os.path.join(os.path.dirname(__file__), file)
    )

def read_fixture_file(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        pytest.fail(f"Test data file not found: {file_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Error decoding JSON from file: {file_path}")
