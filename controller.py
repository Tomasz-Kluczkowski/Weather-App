import tkinter as tk
import datetime


class Controller(object):
    """Mediating Controller(Adapter) class which will help passing
    data between objects.

    Model and View can be added using methods add_view and add_model.
    This class should allow a clear separation of functionality of each 
    class used in the project and avoid calling on each others data 
    by using instance's names.
    It will be used to store and pass data between front (GUI) and 
    backend (model).
    
    """

    def __init__(self):
        """Initialise the Controller.

        :Attributes:
            app_data (dict): Dictionary of data necessary for running
            each segment of the application.
                :Keys:
                    :var_units (tk.StringVar): Value of selection of 
                        units (metric / imperial).
                    :var_status (tk.StringVar): Stores error message to
                        be displayed in the status bar.
                    :var_loc (tk.StringVar): Current text entered into
                        loc_entry field by the user. 
                    :error_message (str): Last error message.
                    :error_status (int): Value -1 means an error 
                        occurred and was not cleared. 0 means all ok.
                    :time (str): String with date / time when call to
                        the API was made.
                    local_time (str): String with local date / time 
                        when call to the API was made.
                    :api_calls (list): List of locations with successful 
                        calls to the API in current session.
                    :metric (dict): Contains dictionaries with weather
                        data in metric system.
                    :imperial (dict): Contains dictionaries with weather
                        data in imperial system.
                    :timezone (dict): Timezone offset for geolocation.
                    The following keys are the same in both metric and
                        imperial dictionaries:
                    w_d_cur (dict): Dictionary containing current
                        weather report.
                    w_d_short (dict): Dictionary containing short
                        forecast (5 days / every 3 hours).
                    w_d_long (dict): Dictionary containing long forecast
                        (16 days max / daily).
            :debug (int): If set to 1 switches debug functions in the
                whole app on. Set to 0 to turn them off. Displays
                report from saved files instead of contacting API.
            :draw_lines (int): Set to 1 to draw alignment lines on
                main_canvas.
            :model (Report): Report class object which will handle all
                the backend operations.
            :data_present (int): Confirms presence of all data from
                API.

        """
        self.app_data = {"var_units": tk.StringVar(value="metric"),
                         "var_status": tk.StringVar(value=""),
                         "var_loc": tk.StringVar(),
                         "error_message": "",
                         "error_status": 0,
                         "time": "",
                         "local_time": "",
                         "api_calls": [],
                         "metric": {},
                         "imperial": {},
                         "timezone": {}
                         }
        """:type : dict[str, any]"""

        self.debug = 0
        self.draw_lines = 0
        self.view = None
        self.model = None
        self.data_present = 0

    def add_model(self, model):
        """Adds a model (business logic) to the Controller.
        
        Args:
            model (Report): Report class object which will handle all
                the backend operations.
            
        Returns:
            None
        """

        self.model = model

    def add_view(self, view):
        """Adds a view (GUI) to the Controller.
        
        Args:
            view (WeatherApp): WeatherApp class object which will deal
                with displaying the GUI.

        Returns:
            None
        """

        self.view = view

    def get_timezone(self, lat, lon):
        """Obtains time zone data for the View to adjust the time 
        received from Open Weather to correct offset.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude

        Returns:
            None
        """
        # Get time zone data.
        data = self.model.finish_get_timezone(lat, lon)
        # We expect a tuple returning from finish_get_report.
        # Item 0 contains error status.
        self.app_data["error_status"] = data[0]
        # Error handling.
        if self.app_data["error_status"] == -1:
            self.display_error(data[1])
        else:
            self.app_data["timezone"] = data[1]

    def display_error(self, error):
        """
        
        Args:
            error (dict): Dictionary containing error data from the API.

        Returns:
            None
        """

        # Error handling.
        self.app_data["error_message"] = error
        # Return to the view and display only the error in the
        # status_bar_label.
        self.app_data["var_status"].set(self.app_data["error_message"])

    def get_report(self):
        """Obtains data for the View to display the report.

        Returns:
            None
        """

        # Get dictionaries.
        data = self.model.finish_get_report(self.app_data["var_loc"].get())

        # We expect a tuple returning from finish_get_report. Item 0
        # contains error status.
        self.app_data["error_status"] = data[0]

        # Error handling.
        if self.app_data["error_status"] == -1:
            self.display_error(data[1])
        else:
            # Clear any error status message upon successful
            # response from API.
            self.app_data["var_status"].set("")
            self.app_data["error_message"] = ""

            # Copy dictionaries from data into metric and imperial
            # dictionary.
            self.app_data["metric"] = data[1][0]["metric"]
            self.app_data["imperial"] = data[1][1]["imperial"]

            # Obtain timezone for geolocation.
            cw_link = self.app_data["metric"]["w_d_cur"]
            """:type : dict"""
            """Link to access current weather data in controller."""
            lat = cw_link["coord"]["lat"]
            lon = cw_link["coord"]["lon"]
            self.get_timezone(lat, lon)
            self.data_present = 1

            # Store location name of a successful call to the API
            #  in api_calls.
            # Check if location called is a country. (Antarctic
            # is not).
            try:
                country = ", " + cw_link["sys"]["country"]
            except KeyError:
                country = ""
            location = "{0}{1}".format(cw_link["name"], country)
            if location not in self.app_data["api_calls"]:
                self.app_data["api_calls"].append(location)
            print(self.app_data["api_calls"])

            # Current date & time.
            date = datetime.datetime.now()
            self.app_data["time"] = date.strftime("%H:%M  %d/%m/%Y")
            local_date = date + datetime.timedelta(
                hours=self.app_data["timezone"]["rawOffset"])
            self.app_data["local_time"] = local_date.strftime(
                "%H:%M  %d/%m/%Y")
            # Now we are ready do display the report.
