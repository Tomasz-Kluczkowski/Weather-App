import pytest
from unittest import mock
from weather_backend import Report
from controller import Controller
from weather_gui import WeatherApp


# Set up classes necessary for testing.
@pytest.fixture(scope="module")
def app():
    """Create WeatherApp and Controller objects."""
    _app = WeatherApp()
    controller = Controller()
    _app.controller = controller
    return _app


test_hr_x_offset_data = [("01:10", 0), ("03:00", 1), ("06:00", 2),
                         ("07:19", 2), ("09:00", 3), ("11:15", 3),
                         ("12:00", 4), ("14:21", 4), ("15:00", 5),
                         ("19:34", 6), ("21:00", 7)]


@pytest.mark.parametrize("text_time, expected", test_hr_x_offset_data)
def test_calculate_hr_x_offset(app, text_time, expected):
    """Test offset for widgets gets calculated from time in text form."""

    assert app.calculate_hr_x_offset(text_time) == expected
