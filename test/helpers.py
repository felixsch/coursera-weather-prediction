import json
import pytest

def read_fixture_file(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        pytest.fail(f"Test data file not found: {file_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Error decoding JSON from file: {file_path}")
