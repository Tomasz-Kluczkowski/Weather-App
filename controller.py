import tkinter as tk


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
                    :scrollbar_offset (tuple): Tuple of float values 
                    representing scrollbar's offset.
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
                         "scrollbar_offset": (0, 0),
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

        self.debug = 1
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

    def get_time(self, unix_time, dst_offset):
        """Contacts model to obtain time converted from unix format to
        human readable one. 
        
        Args:
            dst_offset: (bool) Set to True to offset time received from
                open weather API by daylight savings time.
            unix_time (int): Time given in seconds from beginning of the
                epoch as on unix machines.

        Returns:
            time (str): Time in Hour:Minute format.
        """

        time = self.model.finish_get_time(unix_time, dst_offset)
        return time

    def get_date(self, unix_time, dst_offset):
        """Contact model to convert date from unix time to string.

                Args:
                    dst_offset: (bool) Set to True to offset time received from
                        open weather API by daylight savings time.
                    unix_time (int): Time given in seconds from beginning of the
                        epoch as on unix machines.

                Returns:
                    name_of_day (str): Name of the day on date.
                    date_str (str): Date in string representation.
                """

        name_of_day, date_str = self.model.finish_get_date(unix_time,
                                                           dst_offset)
        return name_of_day, date_str

    def deg_conv(self, wind_dir_deg):
        """Contacts model to convert meteorological degrees to
                cardinal directions.

                Args:
                    wind_dir_deg (float): Wind direction in meteorological 
                        degrees.

                Returns:
                    wind_dir_cardinal (str): Wind direction in cardinal 
                        direction.
                """

        wind_dir_cardinal = self.model.finish_deg_conv(wind_dir_deg)
        return wind_dir_cardinal

    def get_report(self):
        """Contact model to obtain data for the View to display
         the report.

        Returns:
            None
        """

        self.model.finish_get_report(self.app_data["var_loc"].get())

    def display_error(self, error):
        """Updates the View to display error.
        
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

    def display_report(self):
        """Ask view to finalise displaying the report on main_canvas.
        
        Returns:
            None
        """
        self.view.display_report()

    def show_display(self, display):
        """Call to the view to bring forward currently selected display.

        Returns:
            None
        """
        self.view.show_display(display)

    def update_buttons(self):
        """Call to the view to synchronise buttons across all displays.
        
        Returns:
            None
        """
        self.view.update_buttons()
