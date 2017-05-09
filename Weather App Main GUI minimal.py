import requests
import string
import datetime
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


# TODO: TEMP ETC. PLOTTING FROM MATPLOTLIB
# TODO: ADD OPTION TO CHOOSE HOW MANY DAYS REPORT (using spinbox)
# TODO: CONVERT RADIO BUTTONS TO COMBOBOXES (they look nicer)
# TODO: ADD error/status bar at the bottom to display errors etc.


class WeatherApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("The Weather App")
        self.config(bg="#CAE4D8", bd=4, relief="groove", highlightbackground="#CAE4D8", highlightcolor="#CAE4D8")
        # self.wm_attributes("-transparentcolor", "#CAE4D8")
        self.geometry("1000x800")
        self.resizable(width=FALSE, height=FALSE)
        self.var_units = StringVar(value="metric")
        self.var_report_type = StringVar(value="weather")
        self.var_status = StringVar(value="")
        self.report_buttons = []
        self.units_buttons = []

        # self.attributes("-alpha", 0.7)

        # Theme definition
        self.style = Style()
        self.style.theme_use('default')
        # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

        # Style definitions
        # COLORS USED:
        # morning sky:  #CAE4D8
        # honey:        #DCAE1D
        # cerulean:     #00303F
        # mist:         #7A9D96
        self.style.configure("my.TLabel", foreground="#00303F", background="#CAE4D8", borderwidth=0, relief="flat",
                             padding=0)
        self.style.configure("my.TEntry", foreground="#00303F", borderwidth=2, relief="groove", padding=3)
        self.style.configure("my.TButton", foreground="#00303F", background="#DCAE1D", borderwidth=2, relief="flat",
                             padding=2)
        self.style.configure("clear.TButton", foreground="#00303F", background="#CAE4D8", borderwidth=0, relief="flat",
                             padding=(0, 0, 4, 0), width=1, anchor=CENTER)
        self.style.map("clear.TButton", background=[("active", "#CAE4D8")], foreground=[("pressed", "#CAE4D8")])

        self.style.configure("my.TFrame", background="#CAE4D8")
        self.style.configure("my.TText", background="#7A9D96", fg="#DCAE1D")

        # LAYOUT DESIGN

        #main background image
        self.image = Image.open(r"Resources\Images\main_bg.jpg")
        self.image_conv = ImageTk.PhotoImage(self.image)
        self.main_bg_img = self.image_conv
        # self.background_label = Label(self, image=self.main_bg_img)
        # self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LOCATION FRAME
        self.loc_frame = Frame(self, style="my.TFrame")
        # self.loc_frame.place(x=25, y=25)
        self.loc_frame.grid(row=0, column=0, padx=(5, 5), pady=(10, 4), sticky=EW)

        # location label
        self.location_img = PhotoImage(file=r"Resources\Labels\location.png")
        self.l1 = Label(self.loc_frame, text="Location name", style="my.TLabel", image=self.location_img,
                        compound=CENTER)
        self.l1.grid(row=0, column=0, padx=4, pady=4, sticky=W)

        # location entry
        self.e1_val = StringVar()
        self.e1 = tk.Entry(self.loc_frame, textvariable=self.e1_val, background="#CAE4D8", fg="#00303F", width=40)
        # self.e1 = Entry(self.loc_frame, textvariable=self.e1_val, width=70, style="my.TEntry")
        self.e1.focus()
        self.e1.grid(row=0, column=1, padx=0, pady=4, sticky=NSEW)

        # clear location text button
        self.button_clear_normal_img = PhotoImage(file=r"Resources\Buttons\clear_entry_normal.png")
        self.button_clear_hover_img = PhotoImage(file=r"Resources\Buttons\clear_entry_hover.png")
        self.b3 = Button(self.loc_frame, text="X", image=self.button_clear_normal_img, compound=CENTER,
                         command=self.clear_loc_entry, style="clear.TButton")
        self.b3.grid(row=0, column=2, sticky=W, padx=0, pady=0)
        self.b3.bind("<Return>", self.clear_loc_entry)
        self.b3.bind("<Enter>", self.hover_clear_button)
        self.b3.bind("<Leave>", self.normal_clear_button)

        # # MAIN DISPLAY FRAME
        # self.main_frame = Frame(self.background_label, style="my.TFrame")
        # self.main_frame.grid(row=1, column=0)
        # MAIN DISPLAY AREA CANVAS
        self.main_canvas = Canvas(self, bg="#DCAE1D", borderwidth=2, relief="groove", highlightbackground="#CAE4D8", highlightcolor="#CAE4D8")
        self.main_canvas.grid(row=1, column=0, padx=(5, 5), pady=(2, 2), sticky=NSEW)
        # self.image = Image.open(r"Resources\Images\canvas_bg.jpg")
        # self.image_conv = ImageTk.PhotoImage(self.image)
        # self.canvas_bg_img = self.image_conv
        self.main_canvas.create_image(0, 0, image=self.main_bg_img, anchor=NW)

        self.image = Image.open(r"Resources\Labels\location.png")
        self.image_conv = ImageTk.PhotoImage(self.image)
        self.canvas_img_1 = self.image_conv
        self.main_canvas.create_image(20, 20, image=self.canvas_img_1, anchor=NW)

        canvas_text = self.main_canvas.create_text(20, 12, text="test text", fill="#DCAE1D", anchor=NW)

        self.metric_button = Button(self.main_canvas, text="degC")
        self.metric_button.place(x=380, y=100)


        # # MAIN BUTTON FRAME
        # self.button_frame = Frame(self, style="my.TFrame")
        # # self.button_frame.place(x=200, y=25)
        # self.button_frame.grid(row=0, column=4, padx=(25, 25), pady=(25, 4), sticky=NSEW)
        #
        # # get report button
        # self.button_img_normal = PhotoImage(file=r"Resources\Labels\location.png")
        # self.button_img_hover = PhotoImage(file=r"Resources\Buttons\blank_1_hover.png")
        # self.b1 = Button(self.button_frame, image=self.button_img_normal, compound=CENTER, text="Get report",
        #                  command=self.get_report, style="my.TButton")
        # self.b1.bind("<Enter>", self.hover_button)
        # self.b1.bind("<Leave>", self.normal_button)
        # self.b1.grid(row=0, column=3, padx=0, sticky=W)
        #
        # # close app button
        # self.b2 = Button(self.button_frame, text="Close", command=self.close_app, style="my.TButton")
        # self.b2.grid(row=0, column=7, padx=4, sticky=E)

        # # TEXT BOX FRAME
        # self.text_frame = Frame(self, style="my.TFrame")
        # self.text_frame.grid(row=1, column=0, padx=(25, 25), pady=(0, 25), sticky=W)
        #
        # # main text box
        # self.t1 = Text(self.text_frame, state=DISABLED, height=20, width=55, borderwidth=5, bg="#7A9D96")
        # self.t1.grid(row=0, rowspan=20, column=0, sticky=NSEW)
        #
        # # status / error bar
        # self.l_status = Label(self.text_frame, textvariable=self.var_status, width=30, style="my.TLabel")
        # self.l_status.grid(row=21, column=0, pady=4, sticky=W)

        # # SELECTION FRAME
        # self.selection_frame = Frame(self, style="my.TFrame")
        # self.selection_frame.grid(row=1, column=4, padx=4, sticky=N)
        #
        # #["weather", "forecast", "forecast/daily"] REPORT TYPE SECTION
        # self.l4 = Label(self.selection_frame, text="Report type", style="my.TLabel")
        # self.l4.grid(row=2, column=6, columnspan=2, sticky=N)
        #
        # # report type radio button
        # for row, name, value in zip(range(3, 6), ["current", "5 days every 3 hours", "7 days, daily"],
        #                             ):
        #     self.report_buttons.append(
        #         Radiobutton(self.selection_frame, text=name, variable=self.var_report_type, value=value,
        #                     command=self.set_report_type))
        #     self.report_buttons[row - 3].grid(row=row, column=7, pady=4, sticky=W)
        #
        # # UNITS TYPE SECTION
        # self.l5 = Label(self.selection_frame, text="Units type", style="my.TLabel")
        # self.l5.grid(row=6, column=6, columnspan=2, sticky=N)
        #
        # # units type radio button
        # for row, name, value in zip(range(7, 9), ["metric", "imperial"], ["metric", "imperial"]):
        #     self.units_buttons.append(Radiobutton(self.selection_frame, text=name, variable=self.var_units, value=value,
        #                                           command=self.set_units))
        #     self.units_buttons[row - 7].grid(row=row, column=7, pady=4, sticky=W)

        self.bind("<Return>", self.get_report)

    def clear_loc_entry(self, *args):
        self.e1.delete(0, END)
        self.e1.focus()

    def hover_button(self, *args):
        self.b1.configure(image=self.button_img_hover)

    def normal_button(self, *args):
        self.b1.configure(image=self.button_img_normal)

    def hover_clear_button(self, *args):
        self.b3.configure(image=self.button_clear_hover_img)

    def normal_clear_button(self, *args):
        self.b3.configure(image=self.button_clear_normal_img)

    def set_report_type(self):
        pass

    def set_units(self):
        pass

    def get_report(self, *args):
        """ Obtain json weather report"""
        self.w_d = {}
        response = {}
        api_key = "fa730d41d41ae83226a227a150d927ac"
        base_url = "http://api.openweathermap.org/data/2.5/{0}?q={1}{2}&APPID="
        punctuation = string.punctuation
        translator = str.maketrans('', '', punctuation)
        location = self.e1_val.get()
        location = location.translate(translator)
        if self.var_units.get() == "":
            units_prefix = ""
        else:
            units_prefix = "&units="
        try:
            response = requests.get(base_url.format(self.var_report_type.get(), location,
                                                    units_prefix + self.var_units.get()) + api_key)
        except requests.exceptions.ConnectionError:
            self.var_status.set("Unable to establish connection. Please connect to the internet")
            return

        self.w_d = response.json()
        # had to add int(w_d["cod]) as the output from API is int (for current) or string (for longer forecasts)
        if int(self.w_d["cod"]) != 200:
            self.t1.config(state=NORMAL)
            self.t1.delete(1.0, END)
            self.t1.config(state=DISABLED)
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

    def close_app(self):
        self.destroy()


app = WeatherApp()
app.mainloop()
