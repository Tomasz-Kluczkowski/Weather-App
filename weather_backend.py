import requests
import string
import datetime


class Report(object):
    """This class will be used to call Open Weather API and gather data for displaying in the GUI.
        It has no base class and therefore inherits from Python base object.
    
    Args:
        object (object) -- The class inherits from Python base object.
    """

    # TODO: Introduce database to store locations checked by the user in the past.
    # TODO: This should only be passed to the database if the response from the API is 200 (valid location was entered)
    # TODO: Have to add then a combobox/list (?) with selection of previous locations or replace entry box with combobox.

    def __init__(self):
        """Initialize Report class.
        
        Attributes:
            w_d_cur (Dict) -- Dictionary containing current weather report.
            w_d_short (Dict) -- Dictionary containing short forecast (5 days / every 3 hours).
            w_d_long (Dict) -- Dictionary containing long forecast (16 days max / daily).
        """
        self.w_d_cur = {}
        self.w_d_short = {}
        self.w_d_long = {}

    def get_report(self, location, units):
        """Obtain data in json format from Open Weather and store it in appropriate dictionaries.
        
        Args:
            location (Str) -- String containing location typed into loc_entry by the user.
            units (Str) -- String containing unit system selection from unit buttons.
        Returns:
            error
            data
        """

        # Key obtained from Open Weather. Required to make any calls to their API.
        api_key = "fa730d41d41ae83226a227a150d927ac"
        # Base URL used to get weather reports. Notice formatting placeholders for report type, location and units.
        # {0} - space for report type, {1} - space for location, {2} - space for units.
        base_url = "http://api.openweathermap.org/data/2.5/{0}?q={1}{2}&APPID="
        # We must remove any gibberish from location string before making a call to the API.
        # For this translate function is the best tool.

        punctuation = string.punctuation
        translator = str.maketrans("", "", punctuation)
        location = location.translate(translator)

        # Prefix required to let API know what units are requested by the user.
        units_prefix = "&units="

        # List of report types accepted by the API.
        report_types = ["weather", "forecast", "forecast/daily"]
        # List of dictionaries which will store all the data returned from API call.
        weather_dicts = [self.w_d_cur, self.w_d_short, self.w_d_long]

        for report_type, weather_dict in zip(report_types, weather_dicts):
            try:
                response = requests.get(base_url.format(report_type, location,
                                                        units_prefix + units) + api_key)
            except requests.exceptions.ConnectionError:
                # TODO: HANDLE ERRORS PROPERLY
                status = requests.exceptions.ConnectionError
                return "Unable to establish connection. Please connect to the internet"
            weather_dict = response.json()

        # had to add int(w_d["cod]) as the output from API is int (for current) or string (for longer forecasts)
        if any(weather_dicts["cod"]) != 200:
        # if int(self.w_d_cur["cod"]) != 200:

            self.var_status.set("Error: {0}, {1}".format(self.w_d["cod"], self.w_d["message"]))
        else:
            self.display_report()

    def display_report(self):
        """ Displays report converting data from self.w_d dictionary. 
        Unfortunately the API has major differences in data structure for each type of the 
        forecast and one method of extracting data for each cell does not work."""
        # clean the error/status bar
        self.var_status.set("")
        self.time_conv = datetime.datetime.fromtimestamp
        if self.var_units.get() == "metric":
            self.temp_unit = "degC"
            self.speed_unit = "m/s"
        elif self.var_units.get() == "imperial":
            self.temp_unit = "degF"
            self.speed_unit = "mile/hr"
        # Current weather report
        if self.var_report_type.get() == "weather":
            self.t1.config(state=NORMAL)
            self.t1.delete(1.0, END)
            self.t1.insert(END, ("Weather report for: {0}, {1}, lon: {2}, lat: {3}\n".
                                 format(self.w_d["name"], self.w_d["sys"]["country"],
                                        self.w_d["coord"]["lon"], self.w_d["coord"]["lat"])))
            self.t1.insert(END, "Weather type: {0}, {1}\n".format(self.w_d["weather"][0]["main"].lower(),
                                                                  self.w_d["weather"][0]["description"]))
            self.t1.insert(END, "Cloud coverage: {0}%\n".format(self.w_d["clouds"]["all"]))
            self.t1.insert(END, "Current temperature: {0} {1}\n".format(self.w_d["main"]["temp"], self.temp_unit))
            self.t1.insert(END, "Current minimum temperature: {0} {1}\n".format(self.w_d["main"]['temp_min'],
                                                                                self.temp_unit))
            self.t1.insert(END, "Current maximum temperature: {0} {1}\n".format(self.w_d["main"]['temp_max'],
                                                                                self.temp_unit))
            self.t1.insert(END, "Pressure: {0} hPa\n".format(self.w_d["main"]["pressure"]))
            self.t1.insert(END, "Humidity: {0}%\n".format(self.w_d["main"]["humidity"]))
            self.t1.insert(END, "Visibility: {0} m\n".format(self.w_d["visibility"]))
            self.t1.insert(END, "Wind speed: {0} {1}\n".format(self.w_d["wind"]["speed"], self.speed_unit))
            self.t1.insert(END, "Wind direction: {0} deg\n".format(self.w_d["wind"]["deg"]))
            for name in ["rain", "snow"]:
                try:
                    self.t1.insert(END,
                                   "{0} volume for last 3 hours: {1:.4} mm".format(name.title(), self.w_d[name]["3h"]))
                except KeyError:
                    pass
            self.t1.insert(END, "Sunrise at: {0}\n".format(self.time_conv(self.w_d["sys"]["sunrise"]).
                                                           strftime("%H:%M")))
            self.t1.insert(END, "Sunset at: {0}\n".format(self.time_conv(self.w_d["sys"]["sunset"]).strftime("%H:%M")))
            self.t1.config(state=DISABLED)
        # 5 days / 3 hrs report
        elif self.var_report_type.get() == "forecast":
            self.t1.config(state=NORMAL)
            self.t1.delete(1.0, END)
            self.t1.insert(END, ("Weather report for: {0}, {1}, lon: {2}, lat: {3}\n\n".
                                 format(self.w_d["city"]["name"], self.w_d["city"]["country"],
                                        self.w_d["city"]["coord"]["lon"], self.w_d["city"]["coord"]["lat"])))
            for item in self.w_d["list"]:
                self.t1.insert(END, "Forecast at: {0}\n".format(item["dt_txt"]))
                self.t1.insert(END, "Weather type: {0}, {1}\n".format(item["weather"][0]["main"].lower(),
                                                                      item["weather"][0]["description"]))
                self.t1.insert(END, "Cloud coverage: {0}%\n".format(item["clouds"]["all"]))
                self.t1.insert(END, "Temperature: {0} {1}\n".format(item["main"]["temp"], self.temp_unit))
                self.t1.insert(END, "Minimum temperature: {0} {1}\n".format(item["main"]['temp_min'], self.temp_unit))
                self.t1.insert(END, "Maximum temperature: {0} {1}\n".format(item["main"]['temp_max'], self.temp_unit))
                self.t1.insert(END, "Pressure: {0} hPa\n".format(item["main"]["pressure"]))
                self.t1.insert(END, "Humidity: {0}%\n".format(item["main"]["humidity"]))
                self.t1.insert(END, "Wind speed: {0} {1}\n".format(item["wind"]["speed"], self.speed_unit))
                self.t1.insert(END, "Wind direction: {0} deg\n".format(item["wind"]["deg"]))
                for name in ["rain", "snow"]:
                    try:
                        self.t1.insert(END,
                                       "{0} volume for last 3 hours: {1:.4} mm".format(name.title(), item[name]["3h"]))
                    except KeyError:
                        pass
                self.t1.insert(END, "\n\n")
            self.t1.config(state=DISABLED)
        # 16 days / daily report
        else:
            self.t1.config(state=NORMAL)
            self.t1.delete(1.0, END)
            self.t1.insert(END, ("Weather report for: {0}, {1}, lon: {2}, lat: {3}\n\n".
                                 format(self.w_d["city"]["name"], self.w_d["city"]["country"],
                                        self.w_d["city"]["coord"]["lon"], self.w_d["city"]["coord"]["lat"])))
            for item in self.w_d["list"]:
                self.t1.insert(END,
                               "Forecast on: {0}\n".format(self.time_conv(item["dt"]).strftime("%d/%m/%Y at %H:%M")))
                self.t1.insert(END, "Weather type: {0}, {1}\n".format(item["weather"][0]["main"].lower(),
                                                                      item["weather"][0]["description"]))
                self.t1.insert(END, "Cloud coverage: {0}%\n".format(item["clouds"]))
                self.t1.insert(END, "\nTemperatures during the day:\n")
                for name, temp_type in zip(["morning", "day", "evening", "night", "minimum", "maximum"],
                                           ["morn", "day", "eve", "night", "min", "max"]):
                    self.t1.insert(END, "\t{0} {1} {2}\n".format(name, item["temp"][temp_type], self.temp_unit))

                self.t1.insert(END, "\nPressure: {0} hPa\n".format(item["pressure"]))
                self.t1.insert(END, "Humidity: {0}%\n".format(item["humidity"]))
                self.t1.insert(END, "Wind speed: {0} {1}\n".format(item["speed"], self.speed_unit))
                self.t1.insert(END, "Wind direction: {0} deg\n".format(item["deg"]))
                for name in ["rain", "snow"]:
                    try:
                        self.t1.insert(END, "{0} volume for last 3 hours: {1:.4} mm".format(name.title(), item[name]))
                    except KeyError:
                        pass
                self.t1.insert(END, "\n\n")
            self.t1.config(state=DISABLED)
