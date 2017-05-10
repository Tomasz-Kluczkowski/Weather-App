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
            status (Tuple) -- First item is the error status (-1 means error / 0 means all ok).
                Second item is an error message in case of an exception or 
                weather_dicts - list of dictionaries with all weather reports.
            
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
                status = (-1, "Unable to establish internet connection. Please connect to the internet.")
                return status
            weather_dict = response.json()
            # Had to add int(w_d["cod"]) as the output from API is int (for current) / string (for longer forecasts).
            if int(weather_dict["cod"]) != 200:
                status = (-1, "Error: {0}, {1}".format(weather_dict["cod"], weather_dict["message"]))
                return status
            else:
                status = (0, weather_dicts)
                return status
