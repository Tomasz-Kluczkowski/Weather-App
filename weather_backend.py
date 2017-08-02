import sqlite3
import requests
import string
import datetime
import json
import calendar
import appdirs
import os


class Report(object):
    """Model class for application.
    
    This class will be used to call APIs, gather and modify data for
    displaying in the GUI.
    Inherits from Python base object. Model is allowed to directly 
    communicate only with the Controller. 
    All the backend (business logic) will be carried out here.

    """

    def __init__(self, controller):
        """Initialize Report class.

        Args:
            controller (Controller): controller object which will 
            store all the data required by each segment of the 
            application.
        
        :Attributes:
        :v_link (dict): Link to access variables in controller.
        :conn (sqlite3.Connection): Database object
        :cur (sqlite3.Cursor): Database cursor.
        :data_dirs (dict[str, str]): Data directories for the
            application.
        
        """
        self.controller = controller
        self.v_link = self.controller.app_data
        """:type : dict"""

        # Create necessary application folders in 
        # C:\Users\User\AppData\Local
        user_dirs = appdirs.AppDirs("Weather_App", "")
        local_app_dir = user_dirs.user_data_dir
        self.data_dirs = {"Database": "",
                          "Debug": ""}
        for sub_dir in self.data_dirs:
            path = os.path.join(local_app_dir, sub_dir)
            self.data_dirs[sub_dir] = path
            os.makedirs(path, exist_ok=True)

        # Establish database connection.
        self.conn = sqlite3.connect(os.path.join(self.data_dirs["Database"],
                                                 "locations.db"))
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS locations("
                         "Location TEXT NOT NULL UNIQUE, "
                         "Num_of_calls INT NOT NULL DEFAULT 0, "
                         "Units TEXT DEFAULT 'metric')")
        self.conn.commit()
        # Initial list of locations from previous use of the app for
        # loc_combobox ordered by amount of previous calls.
        self.combo_drop_menu()

    def finish_get_report(self, location):
        """Obtain data in json format from Open Weather / Geonames and 
        store it in appropriate dictionaries / variables.

        Args:
            location (str): String containing location typed into  
            loc_entry by the user.

        Returns:
            Status (tuple), first item is the error status 
                (-1 means error / 0 means all ok).
                Second item is an error message in case of an exception or
                weather_dicts - list of dictionaries with all weather reports.
        """
        # We must remove any gibberish from location string before
        # making a call to the API.
        # For this translate function is the best tool.
        punctuation = string.punctuation
        translator = str.maketrans("", "", punctuation)
        location = location.translate(translator)

        # Get dictionaries.
        data = self.open_weather_api(location)

        # We expect a tuple returning from finish_get_report. Item 0
        # contains error status.
        self.v_link["error_status"] = data[0]

        # Error handling.
        if self.v_link["error_status"] == -1:
            self.controller.display_error(data[1])
        else:
            # Copy dictionaries from data into metric and imperial
            # dictionary.
            self.v_link["metric"] = data[1][0]["metric"]
            self.v_link["imperial"] = data[1][1]["imperial"]

            # Obtain timezone for geolocation.
            cw_link = self.controller.app_data["metric"]["w_d_cur"]
            """:type : dict"""
            """Link to access current weather data in controller."""
            lat = cw_link["coord"]["lat"]
            lon = cw_link["coord"]["lon"]

            # Get time zone data.
            data = self.geonames_api(lat, lon)
            # We expect a tuple returning from finish_get_report.
            # Item 0 contains error status.
            self.v_link["error_status"] = data[0]
            # Error handling.
            if self.v_link["error_status"] == -1:
                self.controller.display_error(data[1])
            else:
                self.v_link["timezone"] = data[1]

            self.controller.data_present = True

            # Store location name of a successful call to the API
            # in api_calls.
            # Check if location called is a country. (Antarctic
            # is not).
            try:
                country = ", " + cw_link["sys"]["country"]
            except KeyError:
                country = ""
            location = "{0}{1}".format(cw_link["name"], country)
            self.insert(location)
            # Build a current list of locations for loc_combobox
            # ordered by amount of previous calls.
            self.combo_drop_menu()

            # Current date & time.
            date = datetime.datetime.now()
            self.v_link["time"] = date.strftime("%H:%M  %d/%m/%Y")
            local_date = date + datetime.timedelta(
                hours=self.v_link["timezone"]["rawOffset"])
            self.v_link["local_time"] = local_date.strftime(
                "%H:%M  %d/%m/%Y")
            if self.v_link["error_status"] == 0:
                self.v_link["var_status"].set("")
                self.controller.display_report()
                # Now we are ready do display the report.

    def geonames_api(self, lat, lon):
        """Contacts geonames.org to get the timezone based on lat (latitude)
        and lon (longitude) given.
        
        Args:
            lat (float): Latitude for the location.
            lon (float): Longitude for the location.

        Returns:
            Status (tuple[int, str | dict), first item is the error status 
                (-1 means error / 0 means all ok).
                Second item is an error message (str) in case of an 
                exception or time_zone (dict).
            """

        base_url = "http://api.geonames.org/timezoneJSON?lat={0}&lng={1}&username={2}"
        # Please register your unique user name at:
        # www.geonames.org/login
        user_name = "tomasz_kluczkowski"
        if self.controller.debug == 0:
            try:
                response = requests.get(base_url.format(lat, lon, user_name))

            except requests.exceptions.ConnectionError:
                status = (-1,
                          "Unable to establish internet connection."
                          " Please connect to the internet.")

                return status

            time_zone = response.json()
            # Error handling.
            if "status" in time_zone:
                status = (-1,
                          "Error: {0}, {1}".format(
                              time_zone["status"]["value"],
                              time_zone["status"]["message"]))

                return status
            else:
                path = os.path.join(self.data_dirs["Debug"],
                                    "time_zone.json")
                # Save data in a file for debug purposes.
                self.save_file(time_zone, path)
        else:
            # Load files from debug folder.
            path = os.path.join(self.data_dirs["Debug"], "time_zone.json")
            status = self.load_file(path)
            return status

        status = (0, time_zone)

        return status

    def open_weather_api(self, location):
        """Contact open weather API to obtain data in json format.

        Args:
            location (str): String containing location typed into  
            loc_entry by the user.

        Returns:
            Status (tuple[int, str | dict]), first item is the error status 
                (-1 means error / 0 means all ok).
                Second item is an error message (str) in case of an 
                exception or weather_dicts - list of dictionaries with 
                all weather reports.
        """

        # Key obtained from Open Weather. Required to make any calls
        # to their API.
        # Please register at:
        # https://home.openweathermap.org/users/sign_up
        api_key = "fa730d41d41ae83226a227a150d927ac"

        # Base URL used to get weather reports. Notice formatting
        # placeholders for report type, location and units.
        # {0} - space for report type, {1} - space for location,
        # {2} - space for units.

        base_url = "http://api.openweathermap.org/data/2.5/{0}?q={1}{2}&APPID="

        # Prefix required to let API know what units are requested by
        # the user.
        units_prefix = "&units="

        # List of dictionaries which will store all the data returned
        # from API call.
        unit_dicts = [{"metric": {}}, {"imperial": {}}]
        unit_types = ["metric", "imperial"]
        # List of report types accepted by the API.
        report_types = ["weather", "forecast", "forecast/daily"]
        keys = ["w_d_cur", "w_d_short", "w_d_long"]
        # Switch debug to 1 in controller to load a set of data for a
        # city without contacting the API via internet.

        for unit_dict, unit_type in zip(unit_dicts, unit_types):
            for report_type, key in zip(report_types, keys):
                if self.controller.debug == 0:
                    try:
                        response = requests.get(base_url.
                                                format(report_type, location,
                                                       units_prefix
                                                       + unit_type)
                                                + api_key)
                    except requests.exceptions.ConnectionError:
                        status = (-1,
                                  "Unable to establish internet connection."
                                  " Please connect to the internet.")
                        return status
                    weather_dict = response.json()
                    if response.status_code != 200:
                        status = (-1,
                                  "Error: {0}, {1}".format(weather_dict["cod"],
                                                           weather_dict[
                                                               "message"]))
                        return status
                    else:
                        # Save data files for debug purposes.
                        unit_dict[unit_type][key] = weather_dict
                        path = os.path.join(self.data_dirs["Debug"],
                                            unit_type + "_" + key + ".json")
                        self.save_file(weather_dict, path)
                else:
                    # Load files from debug folder.
                    path = os.path.join(self.data_dirs["Debug"],
                                        unit_type + "_" + key + ".json")
                    status = self.load_file(path)
                    if status[0] == -1:
                        return status
                    unit_dict[unit_type][key] = status[1]
        status = (0, unit_dicts)
        return status

    @staticmethod
    def load_file(path):
        """
        
        Args:
            path (str): path to the file.

        Returns:
            status (tuple[int, dict | str]): at position zero we have an
            error code (-1 means error, 0 - all ok). At index 1 we have
            the data (dict) loaded from the json file or in case of an
            error string with the error code.
        """
        try:
            with open(path, "r") as file:
                status = (0, json.load(file))
                return status
        except FileNotFoundError:
            status = (-1, "Cannot find: {0}".format(path))
            return status

    @staticmethod
    def save_file(data, path):
        """
        
        Args:
            data (dict): data to be saved in json format.
            path (str): path to the file.

        Returns:
            None
        """
        with open(path, "w") as file:
            json.dump(data, file)

    def finish_get_time(self, unix_time, dst_offset):
        """Converts time from unix format to a human readable one.

        Args:
            dst_offset: (bool) Set to True to offset time received from
                open weather API by daylight savings time.
            unix_time (int): Time given in seconds from beginning of the
                epoch as on unix machines.

        Returns:
            time (str): Time in Hour:Minute format.
        """
        if dst_offset:
            dst_offset = self.v_link["timezone"]["dstOffset"] * 3600
        else:
            dst_offset = 0
        time = datetime.datetime.utcfromtimestamp(
            unix_time + dst_offset).strftime("%H:%M")
        return time

    def finish_get_date(self, unix_time, dst_offset):
        """Converts date from unix time to string.

        Args:
            dst_offset: (bool) Set to True to offset time received from
                open weather API by daylight savings time.
            unix_time (int): Time given in seconds from beginning of the
                epoch as on unix machines.

        Returns:
            name_of_day (str): Name of the day on date.
            date_str (str): Date in string representation.
        """
        if dst_offset:
            dst_offset = self.v_link["timezone"]["dstOffset"] * 3600
        else:
            dst_offset = 0

        date = datetime.datetime.utcfromtimestamp(unix_time + dst_offset)
        date_str = date.strftime("%d/%m/%Y")
        name_of_day = calendar.day_name[date.weekday()]
        return name_of_day, date_str

    @staticmethod
    def finish_deg_conv(wind_dir_deg):
        """Converts meteorological degrees to cardinal directions.

        Args:
            wind_dir_deg (float): Wind direction in meteorological 
                degrees.

        Returns:
            wind_dir_cardinal (str): Wind direction in cardinal 
                direction.
        """
        directions = {(348.75, 360): "N",
                      (0, 11.25): "N",
                      (11.25, 33.75): "NNE",
                      (33.75, 56.25): "NE",
                      (56.25, 78.75): "ENE",
                      (78.75, 101.25): "E",
                      (101.25, 123.75): "ESE",
                      (123.75, 146.25): "SE",
                      (146.25, 168.75): "SSE",
                      (168.75, 191.25): "S",
                      (191.25, 213.75): "SSW",
                      (213.75, 236.25): "SW",
                      (236.25, 258.75): "WSW",
                      (258.75, 281.25): "W",
                      (281.25, 303.75): "WNW",
                      (303.75, 326.25): "NW",
                      (326.25, 348.75): "NNW"}

        for interval, wind_dir_cardinal in directions.items():
            if interval[0] <= wind_dir_deg < interval[1]:
                return wind_dir_cardinal

    def combo_drop_menu(self):
        """Build a list of locations for loc_combobox ordered by 
        amount of previous calls.
        
        Returns:
            None
        """
        rows = self.view()
        self.v_link["api_calls"] = []
        for row in rows:
            self.v_link["api_calls"].append(row[0])

    def insert(self, location):
        """Insert a row into locations.db.
        
        Args:
            location (str): 

        Returns:
            None
        """
        local_conn = sqlite3.connect(os.path.join(self.data_dirs["Database"],
                                                  "locations.db"))
        local_cur = local_conn.cursor()

        try:
            local_cur.execute("INSERT INTO locations (Location) VALUES (?)",
                              (location,))
        except sqlite3.IntegrityError:
            pass
        local_cur.execute("UPDATE locations SET Num_of_calls"
                          " = Num_of_calls + 1 WHERE Location = ?",
                          (location,))
        local_conn.commit()
        local_conn.close()

    def view(self):
        """
        
        Returns:
            rows (list[tuple])
        """
        local_conn = sqlite3.connect(os.path.join(self.data_dirs["Database"],
                                                  "locations.db"))
        local_cur = local_conn.cursor()

        local_cur.execute(
            "SELECT Location FROM locations ORDER BY Num_of_calls DESC LIMIT 10")
        rows = local_cur.fetchall()
        local_conn.close()
        return rows

    def __del__(self):
        """Closes connection to locations.db when application is turned
        off.

        Returns:
            None
        """
        self.conn.close()

        # More database  methods which can be used in the future should
        # the need arise.
        # def search(self, location):
        #     self.cur.execute("SELECT * FROM locations WHERE Location=?,
        # (location))
        #     rows = self.cur.fetchall()
        #     return rows

        # def delete(self, location):
        #     self.cur.execute("DELETE FROM locations WHERE Location=?",
        # (location,))
        #     self.conn.commit()

        # def update(self, location):
        #     self.cur.execute("UPDATE locations SET Location=?, (location, ))
        #     self.conn.commit()
