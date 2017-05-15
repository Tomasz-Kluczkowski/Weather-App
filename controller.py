import tkinter as tk


class Controller(object):
    """Controller(Adapter) class which will help passing data between objects.

    Inherits from Python base object. 
    This class should allow a clear separation of functionality of each class used in the project and avoid calling
    on each others data by using instance's name.
    Will be used to store and pass data between front (GUI) and backend (model).

    Args:
        object  -- Python's base object that this class inherits from.

    """

    def __init__(self):
        """Initialise the controller. Give it link to the model and the view.

        Attributes:
            model (Report) -- Report type object. Will carry out all the business logic.
            view (WeatherApp) -- WeatherApp type object. This is our GUI.
            app_data (Dict) -- Dictionary of data necessary for running each segment of the application.
                Keys:
                    var_units (tk.StringVar) -- Value of selection of units (metric / imperial).
                    var_status (tk.StringVar) -- Stores error message to be displayed in the 
                        status bar.
                    var_loc (tk.StringVar) -- Current text entered into loc_entry field by the user. 
                    error_message (Str) -- Last error message.
                    error_status (Int) -- Value -1 means an error occurred and was not cleared. 0 means all ok.
                    w_d_cur (Dict) -- Dictionary containing current weather report.
                    w_d_short (Dict) -- Dictionary containing short forecast (5 days / every 3 hours).
                    w_d_long (Dict) -- Dictionary containing long forecast (16 days max / daily).

        """
        self.app_data = {"var_units": tk.StringVar(value="metric"),
                         "var_status": tk.StringVar(value=""),
                         "var_loc": tk.StringVar(),
                         "error_message": "",
                         "error_status": 0,
                         "w_d_cur": {},
                         "w_d_short": {},
                         "w_d_long": {}
                         }

    def add_model(self, model):
        """Adds a model (business logic) to the controller
        
        Args:
            model (Report) -- report class object which will handle all the backend operations.
        """
        # noinspection PyAttributeOutsideInit
        self.model = model

    def add_view(self, view):
        """Adds a view (GUI) to the controller

        Args:
            view (WeatherApp) -- WeatherApp class object which will deal with displaying GUI.
        """
        # noinspection PyAttributeOutsideInit
        self.view = view

    def request_report(self, location, units):
        """Obtains data for the View to display the report."""
