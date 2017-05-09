import requests
import os
import string
import datetime
from tkinter import *

"""
# TODO: introduce tkinter GUI to the app for ease of use. Start from current weather.
def question():
    user_answer = ""
    while user_answer not in ["y", "yes", "n", "no"]:
        user_answer = input("Do you want to try again? ")
        if user_answer.lower() in ["y", "yes"]:
            _ = os.system("cls")
            return True
        elif user_answer.lower() in ["n", "no"]:
            return False
        else:
            # TODO: trying to use ANSI escape code to clear screen and add colors but it does not work
            _ = os.system("cls")
            continue

def clear_screen():
    _ = os.system("cls")

# here we get rid of unwanted accidentally typed characters
punctuation = string.punctuation
translator = str.maketrans('', '', string.punctuation)
time_conv = datetime.datetime.fromtimestamp

w_d = {}
response = {}
api_key = "fa730d41d41ae83226a227a150d927ac"
base_url = "http://api.openweathermap.org/data/2.5/{0}?q={1}&units=metric&APPID="
forecast_type = None

# file_handle = open("weather_dict.txt", "w")
while not response:
    clear_screen()
    # TODO: MAIN MENU - CURRENT, DAILY, 5 DAY FORECAST. UNIT SELECTION (METRIC, STANDARD, IMPERIAL).
    # TODO: TEMP ETC. PLOTTING FROM MATPLOTLIB
    while forecast_type not in ["c", "d", "f"]:
        clear_screen()
        print("MAIN MENU")
        forecast_type = input("Please select forecast type. Press  c for current,"
                              " d for 5 days 3 hours report, f for 16 days daily forecast: ")

    if forecast_type == "c":
        forecast_type = "weather"
    elif forecast_type == "d":
        forecast_type = "forecast"
    else:
        forecast_type = "forecast/daily"

    location = input("Please enter location: ")
    location = location.translate(translator)

    try:
        response = requests.get(base_url.format(forecast_type, location) + api_key)
    except requests.exceptions.ConnectionError:
        print("Unable to establish connection. Please connect to the internet")
        if question():
            continue
        else:
            break

    w_d = response.json()
    # had to add int(w_d["cod]) as the output from API is int (for current) or string (for longer forecasts)
    if int(w_d["cod"]) != 200:
        print("Error: {0}".format(w_d["cod"]), w_d["message"], "\n")
        if question():
            continue
        else:
            break
    print()
    print("Weather report for: {0}, {1}, lon: {2}, lat: {3}\n".
          format(w_d["name"], w_d["sys"]["country"],
                 w_d["coord"]["lon"], w_d["coord"]["lat"]))

    print("Weather type: {0}, {1}".format(w_d["weather"][0]["main"].lower(), w_d["weather"][0]["description"]))
    print("Cloud coverage: {0}%".format(w_d["clouds"]["all"]))
    print("Current temperature: {0} degC".format(w_d["main"]["temp"]))
    print("Current minimum temperature: {0} degC".format(w_d["main"]['temp_min']))
    print("Current maximum temperature: {0} degC".format(w_d["main"]['temp_max']))
    print("Pressure: {0} hPa".format(w_d["main"]["pressure"]))
    print("Humidity: {0}%".format(w_d["main"]["humidity"]))
    print("Visibility: {0} m".format(w_d["visibility"]))
    print()
    print("Wind speed: {0} m/s".format(w_d["wind"]["speed"]))
    print("Wind direction: {0} deg".format(w_d["wind"]["deg"]))
    print()
    print("Sunrise at: {0}".format(time_conv(w_d["sys"]["sunrise"]).strftime("%H:%M")))
    print("Sunset at: {0}".format(time_conv(w_d["sys"]["sunset"]).strftime("%H:%M")))
"""


# create a weather display class inheriting from tkinter window object TK
class WeatherApp(Tk):

    def __init__(self):
        super().__init__()
        self.title("The Weather App")
        self.var_units = StringVar(value="metric")
        self.var_report_type = StringVar(value="current")
        self.report_buttons = []
        self.units_buttons = []

        # layout design
        self.l1 = Label(self, text="Location name")
        self.l1.grid(row=0, column=0)

        self.e1_val = StringVar()
        self.e1 = Entry(self, textvariable=self.e1_val)
        self.e1.grid(row=0, column=1)

        self.l2 = Label(self, text="Latitude")
        self.l2.grid(row=0, column=2)

        self.e2_val = StringVar()
        self.e2 = Entry(self, textvariable=self.e2_val)
        self.e2.grid(row=0, column=3)

        self.l3 = Label(self, text="Longitude")
        self.l3.grid(row=0, column=4)

        self.e3_val = StringVar()
        self.e3 = Entry(self, textvariable=self.e3_val)
        self.e3.grid(row=0, column=5, sticky=E)

        self.b1 = Button(self, text="Get report", command=self.get_report)
        self.b1.grid(row=0, column=6, sticky=W)

        self.b2 = Button(self, text="Close", command=self.close_app)
        self.b2.grid(row=0, column=7, sticky=W)

        self.t1 = Text(self, height=20, width=71)
        self.t1.grid(row=1, rowspan=20, column=0, columnspan=6)

        # report type section
        self.l4 = Label(self, text="Report type")
        self.l4.grid(row=1, column=6, sticky=W)

        # report type radio button
        for row, name in zip(range(2, 5), ["current", "forecast", "forecast/daily"]):
            self.report_buttons.append(Radiobutton(self, text=name, variable=self.var_report_type, value=name,
                              command=self.set_report_type))
            self.report_buttons[row-2].grid(row=row, column=6, sticky=W)

        # units type section
        self.l5 = Label(self, text="Units type")
        self.l5.grid(row=5, column=6, sticky=W)

        # units type radio button
        for row, name in zip(range(6, 9), ["metric", "imperial", "standard"]):
            self.units_buttons.append(Radiobutton(self, text=name, variable=self.var_units, value=name,
                              command=self.set_units))
            self.units_buttons[row-6].grid(row=row, column=6, sticky=W)

    def set_report_type(self):
        self.t1.insert(END, self.var_report_type.get())

    def set_units(self):
        self.t1.insert(END, self.var_units.get())

    def get_report(self):
        pass

    def close_app(self):
        self.destroy()


app = WeatherApp()
app.mainloop()
