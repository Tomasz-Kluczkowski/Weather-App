import unittest
from weather_gui import WeatherApp


class TestWeatherApp(unittest.TestCase):
    def test_deg_conv(self):
        app = WeatherApp()
        self.assertEqual(app.begin_deg_conv(348.75), "N")
        self.assertEqual(app.begin_deg_conv(0), "N")
        self.assertEqual(app.begin_deg_conv(10), "N")
        self.assertEqual(app.begin_deg_conv(11.25), "NNE")
        self.assertEqual(app.begin_deg_conv(50), "NE")
        self.assertEqual(app.begin_deg_conv(57), "ENE")
        self.assertEqual(app.begin_deg_conv(100), "E")
        self.assertEqual(app.begin_deg_conv(123), "ESE")
        self.assertEqual(app.begin_deg_conv(140), "SE")
        self.assertEqual(app.begin_deg_conv(146.25), "SSE")
        self.assertEqual(app.begin_deg_conv(170), "S")
        self.assertEqual(app.begin_deg_conv(191.25), "SSW")
        self.assertEqual(app.begin_deg_conv(236.249999), "SW")
        self.assertEqual(app.begin_deg_conv(236.25), "WSW")
        self.assertEqual(app.begin_deg_conv(260), "W")
        self.assertEqual(app.begin_deg_conv(303.749999), "WNW")
        self.assertEqual(app.begin_deg_conv(304), "NW")
        self.assertEqual(app.begin_deg_conv(348), "NNW")
        # self.fail()

if __name__ == "__main__":
    unittest.main()
