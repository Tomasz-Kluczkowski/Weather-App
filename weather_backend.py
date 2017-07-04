import sqlite3
import requests
import string
import datetime
import json
import calendar


class Report(object):
    """This class will be used to call APIs, gather 
    and modify data for displaying in the GUI.
       
    Inherits from Python base object. This is our Model. 
    Model is allowed to directly communicate only with the Controller. 
    All the backend (business logic) will be carried out here.

    """

    # TODO: Introduce database to store locations checked by the user
    # TODO: in  the past
    # TODO: This should only be passed to the database if the response
    # TODO: from the API is 200 (valid location was entered)

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
        
        """

        self.controller = controller
        self.v_link = self.controller.app_data
        # Establish database connection.
        self.conn = sqlite3.connect("Database\\locations.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS locations("
                         "Location TEXT NOT NULL UNIQUE, "
                         "Num_of_calls INT NOT NULL DEFAULT 0)")
        self.conn.commit()

    def finish_get_timezone(self, lat, lon):
        """

        Args:
            lat (float): Latitude
            lon (float): Longitude

        Returns:
             Status (tuple):, first item is the error status 
                (-1 means error / 0 means all ok).
                Second item is an error message in case of an exception
                or time_zone (dict) - Timezone data for geolocation 
                after a successful call to the API.
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
                with open("Debug\\time_zone", "w") as file:
                    json.dump(time_zone, file)
        else:
            with open("Debug\\time_zone", "r") as file:
                time_zone = json.load(file)

        status = (0, time_zone)
        return status

    def finish_get_report(self, location):
        """Obtain data in json format from Open Weather and store it 
        in appropriate dictionaries.

        Args:
            location (str): String containing location typed into  
            loc_entry by the user.

        Returns:
            Status (tuple), first item is the error status 
                (-1 means error / 0 means all ok).
                Second item is an error message in case of an exception or
                weather_dicts - list of dictionaries with all weather reports.
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

        # We must remove any gibberish from location string before
        # making a call to the API.
        # For this translate function is the best tool.
        punctuation = string.punctuation
        translator = str.maketrans("", "", punctuation)
        location = location.translate(translator)

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
                        unit_dict[unit_type][key] = weather_dict
                        with open("Debug\\" + unit_type
                                          + "_" + key, "w") as file:
                            json.dump(weather_dict, file)
                else:
                    with open("Debug\\" + unit_type + "_" + key, "r") as file:
                        unit_dict[unit_type][key] = json.load(file)
        status = (0, unit_dicts)
        return status

        # # Store location name of a successful call to the API
        # #  in api_calls.
        # # Check if location called is a country. (Antarctic
        # # is not).
        # cw_link = self.controller.app_data["metric"]["w_d_cur"]
        #
        # try:
        #     country = ", " + cw_link["sys"]["country"]
        # except KeyError:
        #     country = ""
        # location = "{0}{1}".format(cw_link["name"], country)
        # self.insert(location)
        # if location not in self.controller.app_data["api_calls"]:
        #     self.controller.app_data["api_calls"].append(location)
        #
        # # Current date & time.
        # date = datetime.datetime.now()
        # self.controller.app_data["time"] = date.strftime("%H:%M  %d/%m/%Y")
        # local_date = date + datetime.timedelta(
        #     hours=self.controller.app_data["timezone"]["rawOffset"])
        # self.controller.app_data["local_time"] = local_date.strftime(
        #     "%H:%M  %d/%m/%Y")
        # # Now we are ready do display the report.


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

    def insert(self, location):
        try:
            self.cur.execute("INSERT INTO locations (Location) VALUES (?)",
                             (location,))
        except sqlite3.IntegrityError:
            print("already in the table") # remove after tests
        self.cur.execute("UPDATE locations SET Num_of_calls"
                         " = Num_of_calls + 1 WHERE Location = ?", (location,))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM book")
        rows = self.cur.fetchall()
        return rows

    def search(self, title="", author="", year="", isbn=""):
        self.cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM book WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, title, author, year, isbn):
        self.cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
