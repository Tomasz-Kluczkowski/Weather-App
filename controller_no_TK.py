# import tkinter as tk


class Controller(object):
    """Controller(Adapter) class which will help passing data between objects.

    Inherits from tk.TK object (main window). 
    This class should allow a clear separation of functionality of each class used in the project and avoid calling
    on each others data by using instance's name.
    Will be used to store and pass data between front (GUI) and backend (model).

    Args:
        tk.TK  -- base class for the Controller class.

    """

    def __init__(self):
        """Initialise the controller.

        Attributes:
            app_data (Dict) -- Dictionary o data necessary for running each segment of the application.
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

        # super().__init__()
        self.app_data = {"var_units": "metric",
                         "var_status": "",
                         "var_loc": "",
                         "error_message": "",
                         "error_status": 0,
                         "w_d_cur": {},
                         "w_d_short": {},
                         "w_d_long": {}
                         }