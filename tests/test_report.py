import pytest
from weather_backend import Report
from controller import Controller
from weather_gui import WeatherApp


# Set up classes necessary for testing.
app = WeatherApp()
controller = Controller()
app.controller = controller
report = Report(controller)


def test_combo_drop_menu():
    """Test if list of locations in controller.app_data["api_calls"] is
            properly generated out of the database record."""
    report.combo_drop_menu()
    rows = report.view()
    view_list = [row[0] for row in rows]
    assert view_list == controller.app_data["api_calls"]

if __name__ == "__main__":
    pytest.main()
