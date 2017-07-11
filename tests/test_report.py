import unittest
from weather_backend import Report
from controller import Controller
from weather_gui import WeatherApp
app = WeatherApp()
c = Controller()
app.controller = c
r = Report(c)

class TestReport(unittest.TestCase):

    def setUp(self):
        pass
    # def test_finish_get_report(self):
    #     self.fail()
    #
    # def test_geonames_api(self):
    #     self.fail()
    #
    # def test_open_weather_api(self):
    #     self.fail()
    #
    # def test_finish_get_time(self):
    #     self.fail()
    #
    # def test_finish_get_date(self):
    #     self.fail()
    #
    # def test_finish_deg_conv(self):
    #     self.fail()

    def test_combo_drop_menu(self):
        r.combo_drop_menu()
        rows = r.view()
        view_list = [row[0] for row in rows]
        self.assertEqual(view_list, c.app_data["api_calls"])
        # self.fail()

    # def test_insert(self):
    #     self.fail()
    #
    # def test_view(self):
    #     self.fail()

if __name__ == "__main__":
    unittest.main()