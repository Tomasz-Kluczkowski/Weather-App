import pytest
from unittest import mock
from api_example import API

@pytest.fixture(scope="module")
def api_class():
    api = API()
    return api

@pytest.fixture()
def mock_response():
    response = mock.Mock()
    response.return_value.status_code = 2100
    return response


def test_get_stuff(monkeypatch, api_class, mock_response):
    monkeypatch.setattr("api_example.requests.get", mock_response)
    assert api_class.get_stuff().status_code == 200

if __name__ == "__main__":
    pytest.main()
