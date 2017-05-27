import tkinter as tk
import datetime


class Controller(object):
    """Mediating Controller(Adapter) class which will help passing data between objects.

    Inherits from Python base object. Model and View can be added using methods add_view and add_model.
    This class should allow a clear separation of functionality of each class used in the project and avoid calling
    on each others data by using instance's names.
    It will be used to store and pass data between front (GUI) and backend (model).

    Args:
        object  -- Python's base object that this class inherits from.

    """

    def __init__(self):
        """Initialise the Controller.

        Attributes:
            app_data (Dict) -- Dictionary of data necessary for running each segment of the application.
                Keys:
                    var_units (tk.StringVar) -- Value of selection of units (metric / imperial).
                    var_status (tk.StringVar) -- Stores error message to be displayed in the 
                        status bar.
                    var_loc (tk.StringVar) -- Current text entered into loc_entry field by the user. 
                    error_message (Str) -- Last error message.
                    error_status (Int) -- Value -1 means an error occurred and was not cleared. 0 means all ok.
                    time (Str) -- String with date / time when call to the API was made.
                    last_call (List) -- Contains location parameter of last successful call to the API.
                    metric (Dict) -- Contains dictionaries with weather data in metric system.
                    imperial (Dict) -- Contains dictionaries with weather data in imperial system.
                        The following keys are the same in both metric and imperial dictionaries.
                        w_d_cur (Dict) -- Dictionary containing current weather report.
                        w_d_short (Dict) -- Dictionary containing short forecast (5 days / every 3 hours).
                        w_d_long (Dict) -- Dictionary containing long forecast (16 days max / daily).
            debug (Int) -- If set to 1 switches debug functions in the whole app on. Set to 0 to turn them off.
                They include displaying alignment lines to position widgets on canvas and displaying report from 
                saved files instead of contacting API. 

        """
        self.app_data = {"var_units": tk.StringVar(value="metric"),
                         "var_status": tk.StringVar(value=""),
                         "var_loc": tk.StringVar(),
                         "error_message": "",
                         "error_status": 0,
                         "time": "",
                         "last_call": [],
                         "metric": {},
                         "imperial": {},
                         }
        self.debug = 1

    def add_model(self, model):
        """Adds a model (business logic) to the Controller.
        
        Args:
            model (Report) -- Report class object which will handle all the backend operations.
        """
        self.model = model

    def add_view(self, view):
        """Adds a view (GUI) to the Controller.

        Args:
            view (WeatherApp) -- WeatherApp class object which will deal with displaying GUI.
        """
        self.view = view

    def get_report(self):
        """Obtains data for the View to display the report."""

        # Current date & time.
        self.app_data["time"] = datetime.datetime.now().strftime("%H:%M  %d/%m/%Y")
        # Get dictionaries.
        data = self.model.finish_get_report(self.app_data["var_loc"].get())

        # We expect a tuple returning from get_report. Item 0 contains error status.
        self.app_data["error_status"] = data[0]

        # Error handling.
        if self.app_data["error_status"] == -1:
            self.app_data["error_message"] = data[1]
            self.app_data["var_status"].set(self.app_data["error_message"])
            # Return to the view and display only the error in the status_bar_label.
        else:
            # Clear any error status and message upon successful response from API.
            self.app_data["var_status"].set("")
            self.app_data["error_message"] = ""

            # Copy dictionaries from data into metric and imperial dictionary.
            self.app_data["metric"] = data[1][0]["metric"]
            self.app_data["imperial"] = data[1][1]["imperial"]
            self.app_data["last_call"].append(self.app_data["var_loc"])
            # Now we are ready do display the report.
