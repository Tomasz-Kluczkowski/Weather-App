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
    rows = {row[1]: row[2] for row in rows}
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
    expected_dict = {"key1": "val1", "key2": "val2"}
    mock_response = mock.Mock()
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = expected_dict
    monkeypatch.setattr("weather_backend.requests.get", mock_response)
    returned = report.open_weather_api(location)
    assert type(returned) == tuple
    assert mock_response.call_count == 6
    assert returned[0] == 0
    assert returned[1] == [{"metric": {"w_d_cur": expected_dict,
                                       "w_d_short": expected_dict,
                                       "w_d_long": expected_dict}},
                           {"imperial": {"w_d_cur": expected_dict,
                                         "w_d_short": expected_dict,
                                         "w_d_long": expected_dict}}]


def test_open_weather_api_bad_response(monkeypatch, report):
    """Test contacting Open Weather API with a response 400."""
    location = "London"
    expected_dict = {"cod": 400, "message": "error_test"}
    mock_response = mock.Mock()
    mock_response.return_value.status_code = 400
    mock_response.return_value.json.return_value = expected_dict
    monkeypatch.setattr("weather_backend.requests.get", mock_response)
    returned = report.open_weather_api(location)
    assert type(returned) == tuple
    assert mock_response.call_count == 1
    assert returned[0] == -1
    assert returned[1] == "Error: {0}, {1}".format(
        expected_dict["cod"], expected_dict["message"])


def test_open_weather_api_connection_error(report):
    """Test contacting Open Weather API with no internet connection."""
    location = "London"
    returned = report.open_weather_api(location)
    assert returned[0] == -1
    assert returned[1] == "Unable to establish internet connection." \
                          " Please connect to the internet."


def test_geonames_api(monkeypatch, report):
    """Test contacting Open Weather API with a positive response 200."""
    lat = 50
    lon = 0
    base_url = "http://api.geonames.org/timezoneJSON?lat={0}&lng={1}&username={2}"
    user_name = "tomasz_kluczkowski"
    expected_dict = {"key1": "val1", "key2": "val2"}
    mock_response = mock.Mock()
    mock_response.return_value.json.return_value = expected_dict
    monkeypatch.setattr("weather_backend.requests.get", mock_response)
    returned = report.geonames_api(lat, lon)
    assert returned[1] == expected_dict
    assert returned[0] == 0
    mock_response.assert_called_once_with(
        base_url.format(lat, lon, user_name))


def test_geonames_api_error_response(monkeypatch, report):
    """Test contacting geonames API with an error message from
    API."""
    lat = 50
    lon = 0
    expected_dict = {"status": {"value": 10, "message": "test_error"},
                     "key1": "val1", "key2": "val2"}
    mock_response = mock.Mock()
    mock_response.return_value.json.return_value = expected_dict
    monkeypatch.setattr("weather_backend.requests.get", mock_response)
    returned = report.geonames_api(lat, lon)
    assert returned[1] == "Error: {0}, {1}".format(
        expected_dict["status"]["value"],
        expected_dict["status"]["message"])
    assert returned[0] == -1


def test_geonames_api_no_internet_connection(report):
    """Test contacting geonames API with no internet connection."""
    lat = 50
    lon = 0
    returned = report.geonames_api(lat, lon)
    assert returned[0] == -1
    assert returned[1] == "Unable to establish internet connection. Please " \
                          "connect to the internet."


test_deg_conv_parameters = [(348.75, "N"), (0, "N"), (10, "N"), (11.25, "NNE"),
                            (50, "NE"), (57, "ENE"), (100, "E"), (123, "ESE"),
                            (140, "SE"), (146.25, "SSE"), (170, "S"),
                            (191.25, "SSW"), (236.249999, "SW"),
                            (236.25, "WSW"),
                            (260, "W"), (303.749999, "WNW"), (304, "NW"),
                            (348, "NNW")]


@pytest.mark.parametrize("wind_dir_deg, expected", test_deg_conv_parameters)
def test_finish_deg_conv(report, wind_dir_deg, expected):
    """Test degree to cardinal direction conversion."""
    assert report.finish_deg_conv(wind_dir_deg) == expected


# Parameters: unix time, dst offset bool, dst offset value, expected day of
# the week and date
test_finish_get_date_parameters = {(1504697560, True, 1, ("Wednesday",
                                                          "06/09/2017")),
                                   (1504656000, False, 10, ("Wednesday",
                                                            "06/09/2017")),
                                   (1504655999, False, 0, ("Tuesday",
                                                           "05/09/2017")),
                                   (1504652400, True, 1, ("Wednesday",
                                                          "06/09/2017")),
                                   (1504652399, True, 1, ("Tuesday",
                                                          '05/09/2017')),
                                   (1504648800, True, 1, ("Tuesday",
                                                          "05/09/2017")),
                                   (1504648800, True, 2, ("Wednesday",
                                                          "06/09/2017")),
                                   (1504569600, True, -1, ("Monday",
                                                           "04/09/2017"))
                                   }


@pytest.mark.parametrize("unix_time, dst_offset_bool, dst_offset_value, "
                         "expected",
                         test_finish_get_date_parameters)
def test_finish_get_date(report, unix_time, dst_offset_bool,
                         dst_offset_value, expected):
    """Test converting unix time to date and day of the week"""
    report.v_link["timezone"]["dstOffset"] = dst_offset_value
    assert report.finish_get_date(unix_time, dst_offset_bool) == expected

# Parameters: unix time, dst offset bool, dst offset value, expected time in
#  H:m
test_finish_get_time_parameters = {(1504697560, True, 1, "12:32"),
                                   (1504656000, False, 10, "00:00"),
                                   (1504655999, False, 0, "23:59"),
                                   (1504652400, True, 1, "00:00"),
                                   (1504652399, True, 1, "23:59"),
                                   (1504648800, True, 1, "23:00"),
                                   (1504648800, True, 2, "00:00"),
                                   (1504569600, True, -1, "23:00")
                                   }

@pytest.mark.parametrize("unix_time, dst_offset_bool, dst_offset_value, "
                         "expected",
                         test_finish_get_time_parameters)
def test_finish_get_time(report, unix_time, dst_offset_bool,
                         dst_offset_value, expected):
    """Test converting unix time to H:m"""
    report.v_link["timezone"]["dstOffset"] = dst_offset_value
    assert report.finish_get_time(unix_time, dst_offset_bool) == expected


if __name__ == "__main__":
    pytest.main()
