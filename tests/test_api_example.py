import pytest
from unittest import mock
from api_example import API

@pytest.fixture(scope="module")
def api_class():
    return API()


def test_get_stuff(monkeypatch, api_class):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    monkeypatch.setattr("api_test.requests.get", mock_response)
    assert api_class.get_stuff().status_code == 200

if __name__ == "__main__":
    pytest.main()
