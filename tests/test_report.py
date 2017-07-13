import pytest
from weather_backend import Report
from controller import Controller
from weather_gui import WeatherApp
app = WeatherApp()
c = Controller()
app.controller = c
r = Report(c)


def test_combo_drop_menu():
    """Test if list of locations in controller.app_data["api_calls"] is
            properly generated out of the database record."""
    r.combo_drop_menu()
    rows = r.view()
    view_list = [row[0] for row in rows]
    self.assertEqual(view_list, c.app_data["api_calls"])
    #