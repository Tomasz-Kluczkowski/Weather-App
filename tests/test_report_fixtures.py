import pytest
from unittest import mock
import shutil
import appdirs
import os
from weather_backend import Report
from controller import Controller
from weather_gui import WeatherApp


@pytest.fixture(scope="module", autouse=True)
def remove_dirs(app_directories):
    """Delete application folders before testing."""
    for path in app_directories.values():
        shutil.rmtree(path, ignore_errors=True)


def test_dirs_removed(app_directories):
    """Test if application folders have been removed."""
    for path in app_directories.values():
        assert os.path.exists(path) is False


@pytest.fixture(scope="module")
def app_directories():
    """Generate dictionary with paths to the application folders."""
    user_dirs = appdirs.AppDirs("Weather_App", "")
    local_app_dir = user_dirs.user_data_dir
    data_dirs = {"Database": "", "Debug": ""}
    for sub_dir in data_dirs:
        path = os.path.join(local_app_dir, sub_dir)
        data_dirs[sub_dir] = path
    return data_dirs


@pytest.fixture(scope="function")
def fetch_location(report):
    report.cur.execute("SELECT Location FROM locations")
    rows = report.cur.fetchall()
    rows = [row[0] for row in rows]
    return rows


@pytest.fixture(scope="function")
def fetch_all(report):
    report.cur.execute("SELECT * FROM locations")
    rows = report.cur.fetchall()
    rows = {row[0]: row[1] for row in rows}
    return rows


# Set up classes necessary for testing.
@pytest.fixture(scope="module")
def app():
    """Create WeatherApp and Controller objects."""
    _app = WeatherApp()
    controller = Controller()
    _app.controller = controller
    return _app


@pytest.fixture(scope="module")
def report(app):
    """Create Report object."""
    _report = Report(app.controller)
    return _report

def test_insert_new(report):
    """Insert new data into an empty database."""
    report.insert("London, GB")

    

def test_app_folders(app_directories):
    """Test if application folders / files are present after creating
    the Report object."""
    for path in app_directories.values():
        assert os.path.isdir(path) is True


def test_new_exists(fetch_location, fetch_all):
    """Test if data was inserted properly into an empty database."""
    assert fetch_location[0] == "London, GB"
    assert len(fetch_all) == 1


@pytest.mark.parametrize("location", ["Szczecin, PL", "Krakow, PL",
                                      "Wroclaw, PL", "Torun, PL"])
def test_multi_insert(report, location):
    """Insert more data into the database."""
    report.insert(location)


def test_multi_exists(fetch_location):
    """Test if all locations were inserted. Remember that we pull
    them out (using fetch_location) in an alphabetical order 
    (by default)."""
    assert fetch_location == ["Krakow, PL", "London, GB",
                              "Szczecin, PL", "Torun, PL",
                              "Wroclaw, PL"]


def test_num_of_calls(fetch_all):
    """Test if each location has num_of_calls = 1 after being 
    inserted only once."""
    for location, num_of_calls in fetch_all.items():
        assert num_of_calls == 1


def test_insert_again(report):
    """Insert already present data into the database."""
    report.insert("London, GB")


def test_num_of_calls_increased(fetch_all):
    """Test if location "London, GB" has num_of_calls = 2 after being 
    inserted twice."""
    # for location, num_of_calls in fetch_all.items():
    #     if location == "London, GB":
    assert fetch_all["London, GB"] == 2


def test_combo_drop_menu(app, report):
    """Test if list of locations in controller.app_data["api_calls"] is
    properly generated out of the database record."""
    report.combo_drop_menu()
    rows = report.view()
    view_list = [row[0] for row in rows]
    assert view_list == app.controller.app_data["api_calls"]


def test_add_more(report):
    """Insert more data to increase num_of_calls."""
    report.insert("Torun, PL")
    report.insert("Torun, PL")
    report.insert("Torun, PL")
    report.insert("Torun, PL")
    report.insert("London, GB")
    report.insert("London, GB")
    report.insert("Wroclaw, PL")
    report.insert("Wroclaw, PL")
    report.insert("Szczecin, PL")


def test_view_order(report):
    """Test if report.view gets locations ordered by num_of_calls."""
    rows = report.view()
    view_list = [row[0] for row in rows]
    assert view_list == ['Torun, PL', 'London, GB', 'Wroclaw, PL',
                         'Szczecin, PL', 'Krakow, PL']



def test_open_weather_api(monkeypatch, report):
    """Test contacting Open Weather API with a positive response 200."""
    location = "London"
    expected_dict = {"test": 1, "test2": {"test20": 2, "test3": [3, 4]}}
    mock_response = mock.Mock()
    mock_response.status_code.return_value = 200
    mock_response.json.return_value = expected_dict

    monkeypatch.setattr("weather_backend.requests.get", mock_response)
    response_dict = report.open_weather_api(location)
    assert response_dict == expected_dict
    report.open_weather_api.assert_called_once_with(location)

test_deg_conv_data = [(348.75, "N"), (0, "N"), (10, "N"), (11.25, "NNE"),
                      (50, "NE"), (57, "ENE"), (100, "E"), (123, "ESE"),
                      (140, "SE"), (146.25, "SSE"), (170, "S"),
                      (191.25, "SSW"), (236.249999, "SW"), (236.25, "WSW"),
                      (260, "W"), (303.749999, "WNW"), (304, "NW"),
                      (348, "NNW")]

@pytest.mark.parametrize("wind_dir_deg, expected", test_deg_conv_data)
def test_finish_deg_conv(report, wind_dir_deg, expected):
    """Test degree to cardinal direction conversion."""
    assert report.finish_deg_conv(wind_dir_deg) == expected

if __name__ == "__main__":
    pytest.main()
