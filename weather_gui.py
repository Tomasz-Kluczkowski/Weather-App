# Title: Weather App
# Author: Tomasz Kluczkowski
# email: tomaszk1@hotmail.co.uk

import platform
import tkinter as tk
import tkinter.ttk as tkk
from PIL import Image, ImageTk
from weather_backend import Report
from controller import Controller


# TODO: See if autocompletion is possible in the entry field.
# TODO: Add set to default location after successful call has been made.
# TODO: Add mousewheel movement for MAC and LINUX. (needs testing)
# TODO: Add temperature graphs in bokeh / matplotlib.
# TODO: Add 16 day daily report.

class WeatherApp(tk.Tk):
    """Generates graphic user interface for the weather application.
    
    Inherits from tk.TK object (main window).    
    We will apply Model-View-Controller(Adapter) architecture to the 
    project to decouple each segment from the other. The View has no 
    direct contact with the Model and vice versa. All communication is
    done via the Controller. 
    Due to the nature of tkinter library we have to initialise a root
    Tk object to which StringVar type variables and all the GUI elements
    are connected. Since there can be only one Tk object we have to 
    create the WeatherApp class object first (it inherits from TK
    object) and then inside the class call Controller and Report
    classes. 
    Controller class will have access then to the same Tk object as the 
    WeatherApp class. 
    
    Args:
        tk.TK (tk.TK): base class for the WeatherApp class. Tkinter main 
            window "root" object.
    
    """

    def __init__(self):
        """Initializes WeatherApp class.
        
        :Attributes:
        :system (str): Platform on which application is run.
        :controller (Controller): Controller class object used for 
            passing data between the View (weather_gui) and the Model
            (weather_backend).
        :v_link (dict): Link to access variables in controller.
        :dusty (str): color definition in hex number.
        :lavender (str): color definition in hex number.
        :overcast (str): color definition in hex number.
        :paper (str): color definition in hex number.
        :font (str): font definition.
        :title (str): Main window title displayed when using 
            application.
        :loc_frame (tk.Frame): Location frame, parent of all top bar 
            objects.
        :loc_label (tk.Label): Location label.
        :loc_entry (tk.Entry): Location entry object. Here user can 
            input data which will be passed to var_loc.
        :search_button (HoverButton): Search for weather report button.
        :metric_button (HoverButton): Metric units (degC, m/s) selection
            button.
        :imperial_button (HoverButton): Imperial units (degF / mile/hr) 
            selection button.
        :main_canvas (tk.Canvas): Main canvas on which all of the 
            weather report will be visualised.
        :canvas_bg_img (PIL.ImageTk.PhotoImage): Main canvas background 
            image. It is a conversion of a .jpg image using PIL module.
        """

        super().__init__()

        self.system = platform.system()
        # Add Controller to the WeatherApp class instance.
        controller = Controller()
        self.controller = controller
        self.v_link = self.controller.app_data


        # Add main application instance as a View to the Controller.
        # At this stage since we use self updating special tkinter
        # variables we do not need to call on the view for updates.
        # self.controller.add_view(self)

        # Create a Report object for backend operations.
        report = Report(self.controller)
        # Add it as a Model to the Controller class object.
        self.controller.add_model(report)

        # Color palette used:
        self.dusty = "#96858F"
        self.lavender = "#6D7993"
        self.overcast = "#9099A2"
        self.paper = "#D5D5D5"
        # Icon color: #a0cff1 (light blue)
        # #00d3ff (true blue)
        self.font = ("Arial", -18)

        # Configure main window.
        self.title("The Weather App")
        self.config(bg=self.paper, bd=2, relief="groove")
        # Get screen size.
        s_width = self.winfo_screenwidth()
        # s_height = self.winfo_screenheight()
        # Center application window.
        self.geometry("+{0}+0".format(int(s_width / 2) - 400))
        # Prevent resizing.
        self.resizable(width=tk.FALSE, height=tk.FALSE)

        # GUI style definitions.

        # Widget styles.
        # Themes: 'winnative', 'clam', 'alt', 'default',
        # 'classic', 'vista', 'xpnative'
        style = tkk.Style()
        if self.system == "Windows":
            theme = "vista"
        else:
            theme = "clam"
        style.theme_use(theme)
        style.configure("my.TCombobox",
                        fieldbackground=self.paper,
                        foreground="black",
                        )
        self.option_add("*TCombobox*Listbox.font", self.font)
        frame_cnf = {"bg": self.overcast, "bd": 2, "relief": "groove"}
        label_cnf = {"fg": "black", "bg": self.dusty, "bd": 2, "padx": 4,
                     "pady": 9, "font": self.font, "relief": "groove"}
        clear_cnf = {"bg": self.lavender, "fg": "black",
                     "activebackground": self.dusty,
                     "activeforeground": self.paper, "padx": 2, "pady": 2,
                     "anchor": tk.CENTER, "font": self.font,
                     "relief": "groove"}
        self.button_released_cnf = {"fg": "black", "bg": self.lavender,
                                    "activebackground": self.dusty,
                                    "activeforeground": self.paper, "bd": 2,
                                    "padx": 2, "pady": 2, "anchor": tk.CENTER,
                                    "width": 2, "font": self.font,
                                    "relief": "raised"}

        self.button_pushed_cnf = {"fg": self.paper, "bg": self.dusty,
                                  "activebackground": self.lavender,
                                  "activeforeground": "black", "bd": 2,
                                  "padx": 2, "pady": 2, "anchor": tk.CENTER,
                                  "width": 2, "font": self.font,
                                  "relief": "sunken"}
        canvas_cnf = {"bg": self.paper, "bd": 2, "width": 900, "height": 550,
                      "background": "darkblue",
                      "highlightbackground": self.paper,
                      "highlightcolor": self.paper, "relief": "groove"}

        # LAYOUT DESIGN.

        # Location frame.
        loc_frame = tk.Frame(self, **frame_cnf)
        loc_frame.grid(row=0, column=0, padx=(2, 2), pady=(2, 2),
                       sticky=tk.EW)

        # Location label.
        loc_label = tk.Label(loc_frame, text="Location name:", **label_cnf)
        loc_label.grid(row=0, column=0, padx=(4, 4), pady=(4, 5),
                       sticky=tk.NSEW)

        self.loc_combobox = tkk.Combobox(loc_frame,
                                         textvariable=self.v_link["var_loc"],
                                         font=self.font,
                                         width=75,
                                         style="my.TCombobox",
                                         postcommand=self.loc_postcommand,
                                         )
        self.loc_combobox.focus()
        self.loc_combobox.grid(row=0, column=1, padx=(0, 0), pady=(4, 5),
                               sticky=tk.NSEW)
        self.loc_combobox.bind("<Return>", lambda e: self.begin_get_report())
        self.loc_combobox.bind("<Key>", lambda e: self.clear_error_message())

        # Search button.
        self.search_img = tk.PhotoImage(
            file="Resources/Buttons/magnifier-tool.png")
        search_button = HoverButton(loc_frame, controller,
                                    "Press to get a weather report.",
                                    clear_cnf, image=self.search_img,
                                    command=lambda: self.begin_get_report())
        search_button.grid(row=0, column=2, sticky=tk.NSEW, padx=(0, 4),
                           pady=(4, 5))
        # Press Enter to get report.
        search_button.bind("<Return>", lambda e: self.begin_get_report())

        # Metric units button.
        self.metric_button = HoverButton(loc_frame, controller,
                                         "Press to change units to metric.",
                                         self.button_pushed_cnf,
                                         text=u"\N{DEGREE SIGN}C",
                                         command=lambda: self.metric_pushed())
        self.metric_button.grid(row=0, column=3, padx=(2, 4), pady=(4, 5),
                                sticky=tk.NSEW)

        # Imperial units button.
        self.imperial_button = \
            HoverButton(loc_frame, controller,
                        "Press to change units to imperial.",
                        self.button_released_cnf,
                        text=u"\N{DEGREE SIGN}F",
                        command=lambda: self.imperial_pushed())
        self.imperial_button.grid(row=0, column=4, padx=(2, 4), pady=(4, 5),
                                  sticky=tk.NSEW)

        # Canvas frame to put canvas and scrollbar into.
        canvas_frame = tk.Frame(self, **frame_cnf)
        canvas_frame.grid(row=1, column=0, columnspan=5, padx=(2, 2),
                          pady=(2, 2), sticky=tk.EW)
        canvas_frame.columnconfigure(0, weight=4)

        # Main display area canvas.
        self.main_canvas = tk.Canvas(canvas_frame, **canvas_cnf)
        self.main_canvas.grid(row=0, column=0, padx=(0, 0), pady=(0, 2),
                              sticky=tk.NSEW)
        # self.main_canvas.focus_set()

        # Scrollbar.
        self.yscrollbar = tk.Scrollbar(canvas_frame)
        self.yscrollbar.grid(row=0, column=1, padx=(2, 0), pady=(0, 0),
                             sticky=tk.NS)
        self.yscrollbar.config(command=self.main_canvas.yview)

        self.main_canvas.config(yscrollcommand=self.yscrollbar.set)
        image = Image.open("Resources/Images/main_background.jpg")
        # image = image.resize((image.size[0] * 2, image.size[1] * 2),
        # PIL.Image.ANTIALIAS)
        image_conv = ImageTk.PhotoImage(image)
        self.canvas_bg_img = image_conv
        self.main_canvas.create_image(0, 0, image=self.canvas_bg_img,
                                      anchor=tk.NW)

        # Error/Status Bar.
        status_bar_label = tk.Label(self,
                                    textvariable=self.v_link["var_status"],
                                    **label_cnf)
        status_bar_label.grid(row=2, column=0, padx=(2, 2), pady=(0, 2),
                              sticky=tk.NSEW)
        status_bar_label.configure(relief="sunken")
        self.update_geometry()

        # Application icon. Linux does not display it at all.
        if self.system == "Windows":
            self.iconbitmap("app_icon48x48.ico")
        # img_icon = ImageTk.PhotoImage(file="app_icon48x48.ico")
        # self.tk.call("wm", "iconphoto", self._w, img_icon)

    def update_geometry(self):
        """Update and resize application window to use the maximum 
        vertical space available
        
        Returns:
            None
        """
        self.update()
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        c_width = self.winfo_reqwidth()
        c_height = s_height - self.main_canvas.winfo_rooty()*2 - 6
        self.geometry("+{0}+0".format(int(s_width / 2) - int(c_width / 2)))
        self.main_canvas.config(height=c_height)
        # Useful dimension info below.
        # print("screen_width:", self.winfo_screenwidth())
        # print("screen_height:", self.winfo_screenheight())
        # print("main window size:", self.winfo_geometry())
        # print("canvas size:", self.main_canvas.winfo_geometry())
        # print("top decoration:", self.winfo_rooty())
        # print("left edge:", self.winfo_rootx())
        # print("top decoration canvas:", self.main_canvas.winfo_rooty())
        # print("left edge canvas:", self.main_canvas.winfo_rootx())
        # print("main window required width:", self.winfo_reqwidth())
        # print("main window required height:", self.winfo_reqheight())

    def metric_pushed(self):
        """Activates metric units and changes the look of the units buttons.

        Returns:
            None
        """

        self.imperial_button.configure(**self.button_released_cnf)
        self.metric_button.configure(**self.button_pushed_cnf)
        # If button is pushed when there is a report already on the
        # screen and no errors registered - change units but don't call
        # the API.
        if self.v_link["var_units"].get() == "imperial":
            self.v_link["var_units"].set("metric")

            if self.controller.data_present == 1 \
                    and self.v_link["error_status"] == 0:
                self.display_report()

    def imperial_pushed(self):
        """Activates imperial units and changes the look of the units
        buttons.

        Returns:
            None
        """

        self.metric_button.configure(**self.button_released_cnf)
        self.imperial_button.configure(**self.button_pushed_cnf)
        # If button is pushed when there is a report already on the
        # screen and no errors registered - change units but don't call
        # the API.
        if self.v_link["var_units"].get() == "metric":
            self.v_link["var_units"].set("imperial")

            if self.controller.data_present == 1 \
                    and self.v_link["error_status"] == 0:
                self.display_report()

    def clear_error_message(self):
        """Clears error messages from status_bar_label after user starts
        to correct an invalid location name.

        Returns:
            None
        """

        if self.v_link["error_status"] == -1:
            self.v_link["var_status"].set("")
            self.v_link["error_status"] = 0

    def begin_get_time(self, unix_time, dst_offset=True):
        """Contact controller to convert time from unix format to a human 
        readable one.

        Args:
            dst_offset: (bool) Set to True to offset time received from
                open weather API by daylight savings time.
            unix_time (int): Time given in seconds from beginning of the
                epoch as on unix machines.

        Returns:
            time (str): Time in Hour:Minute format.
        """

        time = self.controller.get_time(unix_time, dst_offset)
        return time

    def begin_get_date(self, unix_time, dst_offset=True):
        """Contact controller to convert date from unix time to string.

        Args:
            dst_offset: (bool) Set to True to offset time received from
                open weather API by daylight savings time.
            unix_time (int): Time given in seconds from beginning of the
                epoch as on unix machines.

        Returns:
            name_of_day (str): Name of the day on date.
            date_str (str): Date in string representation.
        """

        name_of_day, date_str = self.controller.get_date(unix_time, dst_offset)
        return name_of_day, date_str

    @staticmethod
    def calculate_hr_x_offset(text_time):
        """
        
        Args:
            text_time (str): Time in text form.

        Returns:
            hr_x_offset (int): Offset value necessary to display the 
            next column of text.
        """

        hours = int(text_time.split(":")[0])

        hr_intervals = {(0, 3): 0,
                        (3, 6): 1,
                        (6, 9): 2,
                        (9, 12): 3,
                        (12, 15): 4,
                        (15, 18): 5,
                        (18, 21): 6,
                        (21, 24): 7}

        for interval, hr_x_offset in hr_intervals.items():
            if interval[0] <= hours < interval[1]:
                return hr_x_offset

    def begin_deg_conv(self, wind_dir_deg):
        """Contacts controller to convert meteorological degrees to
        cardinal directions.
        
        Args:
            wind_dir_deg (float): Wind direction in meteorological 
                degrees.

        Returns:
            wind_dir_cardinal (str): Wind direction in cardinal 
                direction.
        """

        wind_dir_cardinal = self.controller.deg_conv(wind_dir_deg)
        return wind_dir_cardinal

    def begin_get_report(self):
        """Begin getting data for the weather report to display it on 
        the main_canvas.
        The call goes to the Controller first. Then to the Model.

        Returns:
            None
        """

        # Do nothing if no location is entered.
        if self.v_link["var_loc"].get() == "":
            return
        # Request a report using a Mediating Controller.
        self.controller.get_report()
        # Upon a successful contact with the API display the result in
        # the GUI.
        if self.v_link["error_status"] == 0:
            self.display_report()

    def mouse_wheel(self, event):
        """Allows movement of main_canvas using the mouse wheel.
        
        Args:
            event (tkinter.event): Tkinter event object.   

        Returns:
            None
        """

        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def move_canvas_up(self):
        """Scroll main_canvas when Up arrow key is pressed.
        
        Returns:
            None
        """
        self.main_canvas.yview_scroll(-1, "units")

    def move_canvas_down(self):
        """Scroll main_canvas when Down arrow key is pressed.

        Returns:
            None
        """

        self.main_canvas.yview_scroll(1, "units")

    def loc_postcommand(self):
        """Updates the list of items to display in the loc_combobox.
        
        Returns:
            None
        """
        self.loc_combobox["values"] = self.v_link["api_calls"]

    def loc_key_focus(self):
        """Set keyboard focus back to loc_combobox. Select any text
        entered to allow easy deletion.
        
        Returns:
            None
        """
        self.loc_combobox.focus_set()
        self.loc_combobox.select_range(0, tk.END)

    def display_report(self):
        """Display results of the API call in the main_canvas.

        Returns:
            None
        """

        # Initial setup.
        # Delete a previous report if existing on canvas.
        self.main_canvas.delete("main", "hourly")
        self.main_canvas.yview_moveto(0.0)
        # Take keyboard focus from loc_combobox if left mouse button
        # clicked on yscrollbar or main_canvas or if escape pressed
        #  when entering text in loc_combobox.
        self.yscrollbar.bind("<Button-1>",
                             lambda e: self.yscrollbar.focus_set())
        self.main_canvas.bind("<Button-1>",
                              lambda e: self.main_canvas.focus_set())
        self.loc_combobox.bind("<Escape>",
                               lambda e: self.main_canvas.focus_set())

        # Set mouse wheel and arrow keys up / down to control canvas
        # scrolling.
        self.yscrollbar.bind("<MouseWheel>", self.mouse_wheel)
        self.yscrollbar.bind("<Up>", lambda e: self.move_canvas_up())
        self.yscrollbar.bind("<Down>", lambda e: self.move_canvas_down())
        self.main_canvas.bind("<MouseWheel>", self.mouse_wheel)
        # Mouse wheel scroll for Linux.
        self.main_canvas.bind(
            '<4>', lambda e: self.main_canvas.yview_scroll(-1, 'units'))
        self.main_canvas.bind(
            '<5>', lambda e: self.main_canvas.yview_scroll(1, 'units'))
        self.main_canvas.bind("<Up>", lambda e: self.move_canvas_up())
        self.main_canvas.bind("<Down>", lambda e: self.move_canvas_down())
        # Restore keyboard focus to loc_combobox when enter pressed in
        # main_canvas or yscrollbar.
        self.main_canvas.bind("<Return>",
                              lambda e: self.loc_key_focus())
        self.yscrollbar.bind("<Return>",
                             lambda e: self.loc_key_focus())

        # Units system to display report in.
        units = self.v_link["var_units"].get()

        # Config parameters for main section (current weather).
        main_cnf = {"tags": "main", "fill": self.paper, "anchor": tk.NW}
        cent_cnf = {"tags": "main", "fill": self.paper, "anchor": tk.W}
        img_nw_cnf = {"tags": "main", "anchor": tk.NW}

        # Config parameters for hourly section.
        hr_w_cnf = {"tags": "hourly", "fill": self.paper, "anchor": tk.W}
        # hr_n_cnf = {"tags": "hourly", "fill": self.paper, "anchor": tk.N}
        hr_ne_cnf = {"tags": "hourly", "fill": self.paper, "anchor": tk.NE}
        hr_nw_cnf = {"tags": "hourly", "fill": self.paper, "anchor": tk.NW}
        # hr_center_cnf = {"tags": "hourly", "fill": self.paper,
        #                  "anchor": tk.CENTER}
        hr_img_n_cnf = {"tags": "hourly", "anchor": tk.N}
        hr_img_nw_cnf = {"tags": "hourly", "anchor": tk.NW}

        # Font sizes
        h0 = ("Arial", -50)
        h1 = ("Arial", -40)
        h2 = ("Arial", -25)
        h3 = ("Arial", -20)
        h4 = ("Arial", -18)

        # Icon size and color.
        icon_color = "true-blue"
        icon_size = "26px"
        icon_prefix = "Resources/Icons/Parameters/Icons-" + icon_size + "-" \
                      + icon_color + "/"

        # Display location information.
        # Start coordinates in pixels of the report title.
        x1 = 10
        y1 = 4

        if self.controller.draw_lines == 1:
            # Draw coordinate lines to help in item placement.
            # Vertical lines.
            for i in range(1, 250):
                self.main_canvas.create_line(i * 10, 0, i * 10, 2500,
                                             fill="blue")
            # Horizontal lines.
            for i in range(1, 250):
                self.main_canvas.create_line(0, i * 10, 1000, i * 10,
                                             fill="blue")

        cw_link = self.controller.app_data[units]["w_d_cur"]
        """Link to access current weather data in controller."""

        # Title.
        # Check if location called is in a country. (Antarctic is not).
        try:
            country = ", " + cw_link["sys"]["country"]
        except KeyError:
            country = ""
        title_text = "Report for: {0}{1}".format(cw_link["name"], country)
        title = CanvasText(self.main_canvas, (x1, y1), text=title_text,
                           font=h1, **main_cnf)

        # Date.
        date_text = "Received at: {0}\nLocal time: {1}".format(
            self.v_link["time"], self.v_link["local_time"])
        date = CanvasText(self.main_canvas, rel_obj=title, rel_pos="BL",
                          offset=(2, -1), text=date_text, font=h2, **main_cnf)

        # Geo-coords.
        coords_text = "Lon: {0}, Lat: {1}".format(cw_link["coord"]["lon"],
                                                  cw_link["coord"]["lat"])
        coords = CanvasText(self.main_canvas, rel_obj=date, rel_pos="BL",
                            offset=(1, 2), text=coords_text, font=h2,
                            **main_cnf)

        # Draw a current weather icon.
        icon_path = "Resources/Icons/Weather/" \
                    + cw_link["weather"][0]["icon"] + ".png"
        # Images have to be added as attributes or otherwise they get
        # garbage collected and will not display at all.
        self.cur_icon = CanvasImg(self.main_canvas, icon_path, rel_obj=coords,
                                  rel_pos="BL", offset=(2, 42), **img_nw_cnf)

        # Current temperature.
        if self.v_link["var_units"].get() == "metric":
            sign = "C"
        else:
            sign = "F"
        cur_temp_text = "{0:.1f}\N{DEGREE SIGN}{1}".format(
            cw_link["main"]["temp"],
            sign)

        cur_temp = CanvasText(self.main_canvas, rel_obj=self.cur_icon,
                              rel_pos="CR", offset=(5, -2),
                              text=cur_temp_text, font=h0, **cent_cnf)

        # Max temperature.
        max_temp_text = "max: {0:.1f}\N{DEGREE SIGN}{1}".format(
            cw_link["main"]['temp_max'],
            sign)
        max_temp = CanvasText(self.main_canvas, rel_obj=cur_temp, rel_pos="TR",
                              offset=(15, 5),
                              text=max_temp_text, font=h3, **main_cnf)

        # Min temperature.
        min_temp_text = "min: {0:.1f}\N{DEGREE SIGN}{1}".format(
            cw_link["main"]['temp_min'],
            sign)
        min_temp = CanvasText(self.main_canvas, rel_obj=cur_temp, rel_pos="BR",
                              offset=(15, -27),
                              text=min_temp_text, font=h3, **main_cnf)

        # Weather description.
        w_desc_text = "{0}".format(
            cw_link["weather"][0]["description"].capitalize())
        w_desc = CanvasText(self.main_canvas, rel_obj=cur_temp, rel_pos="BL",
                            offset=(3, -2),
                            text=w_desc_text, font=h2, **main_cnf)

        # Pressure.
        max_temp_bounds = self.main_canvas.bbox(max_temp.id_num)
        icon_path = icon_prefix + "atmospheric_pressure.png"
        self.pressure_img = CanvasImg(self.main_canvas, icon_path,
                                      coordinates=(450, max_temp_bounds[1]),
                                      offset=(0, 0), **img_nw_cnf)
        pressure_text = "{0:.1f} hPa".format(cw_link["main"]["pressure"])
        pressure = CanvasText(self.main_canvas, rel_obj=self.pressure_img,
                              rel_pos="CR", offset=(5, 0),
                              text=pressure_text, font=h2, **cent_cnf)

        # Cloud coverage.
        icon_path = icon_prefix + "cloud.png"
        self.clouds_img = CanvasImg(self.main_canvas, icon_path,
                                    rel_obj=w_desc,
                                    rel_pos="BL", offset=(0, 3), **img_nw_cnf)
        clouds_cnf = {"tags": "main", "fill": self.paper, "anchor": tk.W}
        clouds_text = "{0}%".format(
            cw_link["clouds"]["all"])
        clouds = CanvasText(self.main_canvas, rel_obj=self.clouds_img,
                            rel_pos="CR", offset=(5, 0),
                            text=clouds_text, font=h2, **clouds_cnf)

        # Humidity.
        icon_path = icon_prefix + "humidity.png"
        self.humidity_img = CanvasImg(self.main_canvas, icon_path,
                                      rel_obj=self.pressure_img,
                                      rel_pos="BL", offset=(0, 4),
                                      **img_nw_cnf)
        humidity_text = "{0}%".format(cw_link["main"]["humidity"])
        humidity = CanvasText(self.main_canvas, rel_obj=self.humidity_img,
                              rel_pos="CR", offset=(5, 0),
                              text=humidity_text, font=h2, **cent_cnf)

        # Wind speed.
        icon_path = icon_prefix + "windsock_filled.png"
        self.wind_img = CanvasImg(self.main_canvas, icon_path,
                                  rel_obj=self.humidity_img,
                                  rel_pos="BL", offset=(0, 4), **img_nw_cnf)
        if self.v_link["var_units"].get() == "metric":
            speed_unit = "m/s"
        else:
            speed_unit = "mile/hr"
        wind_text = "{0:.1f} {1}".format(cw_link["wind"]["speed"], speed_unit)
        wind = CanvasText(self.main_canvas, rel_obj=self.wind_img,
                          rel_pos="CR", offset=(5, 0),
                          text=wind_text, font=h2, **cent_cnf)

        # Wind direction.
        icon_path = icon_prefix + "wind_rose.png"
        self.wind_dir_img = CanvasImg(self.main_canvas, icon_path,
                                      rel_obj=self.wind_img,
                                      rel_pos="BL", offset=(0, 4),
                                      **img_nw_cnf)
        # Noticed that sometimes Open Weather responds with no wind
        # direction in the current weather report.
        try:
            wind_dir_text = "{0}".format(
                self.begin_deg_conv(cw_link["wind"]["deg"]))
        except KeyError:
            wind_dir_text = ""

        wind_dir = CanvasText(self.main_canvas, rel_obj=self.wind_dir_img,
                              rel_pos="CR", offset=(5, 0),
                              text=wind_dir_text, font=h2, **cent_cnf)

        # Sunrise.
        icon_path = icon_prefix + "sunrise.png"
        self.sunrise_img = CanvasImg(self.main_canvas, icon_path,
                                     coordinates=(670, max_temp_bounds[1]),
                                     offset=(0, 0), **img_nw_cnf)
        sunrise_text = "{0}".format(
            self.begin_get_time(cw_link["sys"]["sunrise"]))
        sunrise = CanvasText(self.main_canvas, rel_obj=self.sunrise_img,
                             rel_pos="CR", offset=(5, 0),
                             text=sunrise_text, font=h2, **cent_cnf)

        # Sunset.
        icon_path = icon_prefix + "sunset.png"
        self.sunset_img = CanvasImg(self.main_canvas, icon_path,
                                    rel_obj=self.sunrise_img, rel_pos="BL",
                                    offset=(0, 4), **img_nw_cnf)
        sunset_text = "{0}".format(
            self.begin_get_time(cw_link["sys"]["sunset"]))
        sunset = CanvasText(self.main_canvas, rel_obj=self.sunset_img,
                            rel_pos="CR", offset=(5, 0),
                            text=sunset_text, font=h2, **cent_cnf)

        # DISPLAY HOURLY INFO.

        # Icon size and color.
        icon_color = "true-blue"
        icon_size = "20px"
        icon_prefix = "Resources/Icons/Parameters/Icons-" + icon_size \
                      + "-" + icon_color + "/"

        # Here we iterate through w_d_short dictionary to confirm on
        # which days we have rain and/or snow to display their
        # corresponding icons properly without overlapping.
        rain_dates = {}
        snow_dates = {}
        previous_date = ""
        for item in self.v_link[units]["w_d_short"]["list"]:

            for name in ["rain", "snow"]:
                try:
                    if item[name]["3h"]:
                        date = self.begin_get_date(item["dt"])
                        current_date = "{0:.3}, {1:.5}".format(
                            date[0], date[1])
                        if current_date != previous_date:
                            if name == "rain":
                                rain_dates[current_date] = "rain"
                            else:
                                snow_dates[current_date] = "snow"
                except KeyError:
                    pass

        day = None
        previous_day_text = ""
        date_index = 0
        hr_rain = None
        day_y_offset = 0
        hr_x_offset = 0
        max_y = 0
        day_rain_present = False
        day_snow_present = False
        hr_rain_present = False
        hr_snow_present = False
        hr_snow = None
        self.hr_weather_icons = []
        self.hr_temp_icons = []
        """:type : list[CanvasImg]"""
        self.hr_pressure_icons = []
        """:type : list[CanvasImg]"""
        self.hr_rain_icons = []
        """:type : list[CanvasImg]"""
        self.hr_snow_icons = []
        """:type : list[CanvasImg]"""
        self.hr_cloud_icons = []
        """:type : list[CanvasImg]"""
        self.hr_humidity_icons = []
        """:type : list[CanvasImg]"""
        self.hr_wind_icons = []
        """:type : list[CanvasImg]"""
        self.hr_wind_dir_icons = []
        """:type : list[CanvasImg]"""

        for item in self.v_link[units]["w_d_short"]["list"]:

            day_text = "{0:.3}, {1:.5}".format(
                self.begin_get_date(item["dt"])[0],
                self.begin_get_date(item["dt"])[1])

            if previous_day_text == day_text:
                pass
            else:
                # Calculate y offset for the next day.
                if date_index > 0 and hr_x_offset == 7:
                    y1_day = self.main_canvas.bbox(day.id_num)[1]
                    day_y_offset += 25 + max_y - y1_day

                # Display date and day of the week.
                day = CanvasText(self.main_canvas, rel_obj=self.cur_icon,
                                 rel_pos="BL",
                                 offset=(0, 86 + day_y_offset),
                                 text=day_text, justify=tk.LEFT, font=h3,
                                 **hr_nw_cnf)

                # Draw temperature icon.
                icon_path = icon_prefix + "temperature.png"
                self.hr_temp_icons.append(
                    CanvasImg(self.main_canvas, icon_path,
                              rel_obj=day, rel_pos="BL", offset=(0, 0),
                              **hr_img_nw_cnf))

                # Draw pressure icon.
                icon_path = icon_prefix + "atmospheric_pressure.png"
                self.hr_pressure_icons.append(
                    CanvasImg(self.main_canvas, icon_path,
                              rel_obj=self.hr_temp_icons[-1], rel_pos="BL",
                              offset=(0, 0), **hr_img_nw_cnf))

                # Draw cloud coverage icon.
                icon_path = icon_prefix + "cloud.png"
                self.hr_cloud_icons.append(
                    CanvasImg(self.main_canvas, icon_path,
                              rel_obj=self.hr_pressure_icons[-1], rel_pos="BL",
                              offset=(0, 0), **hr_img_nw_cnf))

                # Draw humidity icon.
                icon_path = icon_prefix + "humidity.png"
                self.hr_humidity_icons.append(
                    CanvasImg(self.main_canvas, icon_path,
                              rel_obj=self.hr_cloud_icons[-1], rel_pos="BL",
                              offset=(0, 0), **hr_img_nw_cnf))

                # Draw wind icon.
                icon_path = icon_prefix + "windsock_filled.png"
                self.hr_wind_icons.append(
                    CanvasImg(self.main_canvas, icon_path,
                              rel_obj=self.hr_humidity_icons[-1], rel_pos="BL",
                              offset=(0, 0), **hr_img_nw_cnf))

                # Draw wind direction icon.
                icon_path = icon_prefix + "wind_rose.png"
                self.hr_wind_dir_icons.append(
                    CanvasImg(self.main_canvas, icon_path,
                              rel_obj=self.hr_wind_icons[-1], rel_pos="BL",
                              offset=(0, 0), **hr_img_nw_cnf))

                # Draw rain icon if phenomena present during the day.
                if day_text in rain_dates:
                    icon_path = icon_prefix + "rain" + ".png"
                    self.hr_rain_icons.append(
                        CanvasImg(self.main_canvas, icon_path,
                                  rel_obj=self.hr_wind_dir_icons[-1],
                                  rel_pos="BL", offset=(0, 0),
                                  **hr_img_nw_cnf))

                # Draw snow icon if phenomena present during the day.
                if day_text in rain_dates:
                    rel_obj_icon = self.hr_rain_icons[-1]
                else:
                    rel_obj_icon = self.hr_wind_dir_icons[-1]

                if day_text in snow_dates:
                    icon_path = icon_prefix + "snow" + ".png"
                    self.hr_snow_icons.append(
                        CanvasImg(self.main_canvas, icon_path,
                                  rel_obj=rel_obj_icon,
                                  rel_pos="BL", offset=(0, 0),
                                  **hr_img_nw_cnf))

                previous_day_text = day_text
                date_index += 1
                max_y = 0
                day_rain_present = False
                day_snow_present = False

            # Hour.
            hour_text = self.begin_get_time(item["dt"])
            hr_x_offset = self.calculate_hr_x_offset(hour_text)
            hour = CanvasText(self.main_canvas, rel_obj=day, rel_pos="CL",
                              offset=(130 + hr_x_offset * 115, 0),
                              text=hour_text, justify=tk.CENTER, font=h3,
                              **hr_w_cnf)

            # Hourly Weather icon.
            icon_path = "Resources/Icons/Weather/" \
                        + item["weather"][0]["icon"] + ".png"
            self.hr_weather_icons.append(
                CanvasImg(self.main_canvas, icon_path, rel_obj=hour,
                          rel_pos="BC", offset=(0, -5), **hr_img_n_cnf))

            # Hourly temperature.
            hr_temp_text = "{0:.1f}\N{DEGREE SIGN}{sign}".format(
                item["main"]["temp"], sign=sign)

            hr_temp = CanvasText(self.main_canvas,
                                 rel_obj=hour,
                                 rel_pos="BR",
                                 offset=(-1, 40),
                                 text=hr_temp_text, font=h3, **hr_ne_cnf)
            # Update hr_temp_icon y coordinate to center of hr_temp.
            self.hr_temp_icons[-1].move_rel_to_obj_y(hr_temp)

            # Hourly pressure.
            hr_pressure_text = "{0:.1f} hPa".format(item["main"]["pressure"])
            hr_pressure = CanvasText(self.main_canvas, rel_obj=hr_temp,
                                     rel_pos="BR",
                                     offset=(-2, 5),
                                     text=hr_pressure_text, font=h4,
                                     **hr_ne_cnf)
            # Update hr_pressure_icon y coordinate to center of
            # hr_pressure.
            self.hr_pressure_icons[-1].move_rel_to_obj_y(hr_pressure)

            # Hourly cloud coverage.
            hr_cloud_text = "{0}%".format(item["clouds"]["all"])
            hr_cloud = CanvasText(self.main_canvas, rel_obj=hr_pressure,
                                  rel_pos="BR",
                                  offset=(0, 5),
                                  text=hr_cloud_text, font=h4, **hr_ne_cnf)
            # Update hr_cloud_icon y coordinate to center of hr_cloud.
            self.hr_cloud_icons[-1].move_rel_to_obj_y(hr_cloud)

            # Hourly humidity.
            hr_humidity_text = "{0}%".format(item["main"]["humidity"])
            hr_humidity = CanvasText(self.main_canvas, rel_obj=hr_cloud,
                                     rel_pos="BR",
                                     offset=(-1, 5),
                                     text=hr_humidity_text, font=h4,
                                     **hr_ne_cnf)
            # Update hr_humidity_icon y coordinate to center of
            # hr_humidity.
            self.hr_humidity_icons[-1].move_rel_to_obj_y(hr_humidity)

            # Hourly wind speed.
            hr_wind_text = "{0:.1f} {1}".format(item["wind"]["speed"],
                                                speed_unit)
            hr_wind = CanvasText(self.main_canvas, rel_obj=hr_humidity,
                                 rel_pos="BR",
                                 offset=(-1, 5),
                                 text=hr_wind_text, font=h4, **hr_ne_cnf)
            # Update hr_wind_icon y coordinate to center of hr_wind.
            self.hr_wind_icons[-1].move_rel_to_obj_y(hr_wind)

            # Hourly wind direction.
            hr_wind_dir_text = "{0}".format(
                self.begin_deg_conv(item["wind"]["deg"]))
            hr_wind_dir = CanvasText(self.main_canvas, rel_obj=hr_wind,
                                     rel_pos="BR",
                                     offset=(-1, 5),
                                     text=hr_wind_dir_text, font=h4,
                                     **hr_ne_cnf)
            # Update hr_wind_dir_icon y coordinate to center of
            # hr_wind_dir.
            self.hr_wind_dir_icons[-1].move_rel_to_obj_y(hr_wind_dir)

            # Hourly Rain.
            try:
                rain_amount = item["rain"]["3h"]
                prefix = ""
                if rain_amount < 0.1:
                    prefix = u"\u2248 "
                    rain_amount = 0
                rain_text = "{0}{1:.1f} mm/3h".format(prefix, rain_amount)
                hr_rain = CanvasText(self.main_canvas,
                                     rel_obj=hr_wind_dir,
                                     rel_pos="BR",
                                     offset=(-1, 10),
                                     text=rain_text, font=h4,
                                     **hr_ne_cnf)
                # Update hr_rain_icon y coordinate to center of
                # hr_rain.
                if not day_rain_present:
                    self.hr_rain_icons[-1].move_rel_to_obj_y(
                        hr_rain)

                day_rain_present = True
                hr_rain_present = True

            except KeyError:
                pass

            # Hourly Snow.
            try:
                snow_amount = item["snow"]["3h"]
                prefix = ""
                if snow_amount < 0.1:
                    prefix = u"\u2248 "
                    snow_amount = 0
                snow_text = "{0}{1:.1f} mm/3h".format(prefix, snow_amount)
                # If no rain present during entire day.
                if day_text not in rain_dates:
                    rel_obj_text = hr_wind_dir
                    offset = (-1, 10)
                # If rain present at the current hour or in the day.
                else:
                    rel_obj_text = hr_wind_dir
                    offset = (-1, 35)
                hr_snow = CanvasText(self.main_canvas,
                                     rel_obj=rel_obj_text,
                                     rel_pos="BR",
                                     offset=offset,
                                     text=snow_text, font=h4,
                                     **hr_ne_cnf)
                # Update hr_snow_icon y coordinate to center of
                # hr_snow.
                if not day_snow_present:
                    self.hr_snow_icons[-1].move_rel_to_obj_y(
                        hr_snow)

                day_snow_present = True
                hr_snow_present = True

            except KeyError:
                pass

            # Get the maximum y coordinate present on the canvas.
            if hr_snow_present:
                cur_y = self.main_canvas.bbox(hr_snow.id_num)[3]
            elif hr_rain_present:
                cur_y = self.main_canvas.bbox(hr_rain.id_num)[3]
            else:
                cur_y = self.main_canvas.bbox(hr_wind_dir.id_num)[3]
            if cur_y > max_y:
                max_y = cur_y

            hr_snow_present = False
            hr_rain_present = False

        self.update()
        self.main_canvas.config(
            scrollregion=self.main_canvas.bbox("main", "hourly"))
        self.yscrollbar.focus()

class HoverButton(tk.Button):
    """Improves upon the standard button by adding status bar display 
    option.
    
    We can use the same configuration dictionary as for the standard 
    tk.Button.

    Args:
        tk.Button (tk.Button): Standard tkinter Button object which we 
            inherit from.
           
    """

    def __init__(self, master, controller, tip, cnf, **args):
        """Initialise MyButton.
        
        Args:
            master (tk.widget): Master widget to which MyButton (slave) 
                instance will belong. The master widget is part of 
                the WeatherApp object.
            controller (Controller): controller object which will store 
                all the data required by each segment of the 
                application.
            tip (str): Tooltip text to display in the status_bar_label.
            cnf (dict): Dictionary with the configuration for MyButton.
            **args: Keyword arguments to further initialise the button.
            
        :Attributes:
        
        :cur_bg (str): Current background color of the button.
        :tip (str): Text to display in the status_bar_label of the app.
        :controller (Controller): controller object which will store all
            the data required by each segment of the application. 
            This has to be the same Controller as for the WeatherApp.
        :v_link (dict): Link to access variables in controller.

        
        """

        super().__init__(master, cnf, **args)
        self.cur_bg = self["bg"]
        self.controller = controller
        self.v_link = self.controller.app_data
        self.tip = tip
        # Action on entering the button with mouse.
        self.bind("<Enter>", lambda e: self.enter_button())
        # Action on leaving the button with mouse.
        self.bind("<Leave>", lambda e: self.leave_button())

    def enter_button(self):
        """Displays information on button function to the user in the 
        status_bar_label.

        Returns:
            None
        """
        self.configure(background="DimGrey")
        self.v_link["var_status"].set(self.tip)

    def leave_button(self):
        """Clears status_bar_label after mouse leaves the button area.

        Returns:
            None
        """
        self.configure(background=self.cur_bg)
        if self.v_link["error_status"] == -1:
            self.v_link["var_status"].set(
                self.v_link["error_message"])
        else:
            self.v_link["var_status"].set("")


class CanvasObject(object):
    """Base class to create objects on canvas.

    Allows easier placement of objects on canvas in relation to other 
    objects. Allowed positions in relation to the relative object:
    TL - top-left, TC - top-center, TR - top-right, 
    CL - center-left, CC - center-center,
    CR - center-right, BL - bottom-left, BC - bottom-center,
    BR - bottom-right

    Args:
        object (object): Base Python object we inherit from.

    """

    def __init__(self, canvas, coordinates=None, rel_obj=None,
                 rel_pos=None, offset=None):
        """Initialise class - calculate x-y coordinates for our object.

        Allows positioning in relation to the rel_obj (CanvasText or 
        CanvasImg object).
        We can give absolute position for the object or a relative one.
        In case of an absolute position given we will ignore the 
        relative parameter.
        The offset allows us to move the instance away from the border of 
        the relative object.

        Args:
            canvas (tk.Canvas): Canvas on which CanvasObject will be 
                placed.
            coordinates (tuple): Absolute x, y coordinates where to 
                place text in canvas. Overrides any parameters  given in
                relative parameters section.
            rel_obj (CanvasText / CanvasImg): CanvasText / CanvasImg 
                object which will be used as a relative one next to 
                which text is meant to be written.
            rel_pos (str): String determining position of newly created 
                text in relation to the relative object. Similar concept
                to anchor.
                TL - top-left, TC - top-center, TR - top-right, 
                CL - center-left, CC - center-center,
                CR - center-right, BL - bottom-left, BC - bottom-center,
                BR - bottom-right
            offset (tuple): Offset given as a pair of values to move the
                newly created object away from the relative object.

        :Attributes:
        :id_num (int): Unique id number of the CanvasObject given by 
            canvas.bbox method in the subclass.  
        :canvas (tk.Canvas): tkinter Canvas object.
        :pos_x (int): X coordinate for our object.
        :pos_y (int): Y coordinate for our object.

        """

        self.id_num = 0
        self.canvas = canvas
        pos_x = 0
        pos_y = 0

        if offset:
            offset_x = offset[0]
            offset_y = offset[1]
        else:
            offset_x = 0
            offset_y = 0
        if coordinates:
            pos_x = coordinates[0]
            pos_y = coordinates[1]
        elif rel_obj is not None and rel_pos is not None:
            # Get Top-Left and Bottom-Right bounding points of the
            # relative object.
            r_x1, r_y1, r_x2, r_y2 = canvas.bbox(rel_obj.id_num)

            # Determine position of CanvasObject on canvas in relation
            # to the rel_obj.
            if rel_pos == "TL":
                pos_x = r_x1
                pos_y = r_y1
            elif rel_pos == "TC":
                pos_x = r_x2 - (r_x2 - r_x1) / 2
                pos_y = r_y1
            elif rel_pos == "TR":
                pos_x = r_x2
                pos_y = r_y1
            elif rel_pos == "CL":
                pos_x = r_x1
                pos_y = r_y2 - (r_y2 - r_y1) / 2
            elif rel_pos == "CC":
                pos_x = r_x2 - (r_x2 - r_x1) / 2
                pos_y = r_y2 - (r_y2 - r_y1) / 2
            elif rel_pos == "CR":
                pos_x = r_x2
                pos_y = r_y2 - (r_y2 - r_y1) / 2
            elif rel_pos == "BL":
                pos_x = r_x1
                pos_y = r_y2
            elif rel_pos == "BC":
                pos_x = r_x2 - (r_x2 - r_x1) / 2
                pos_y = r_y2
            elif rel_pos == "BR":
                pos_x = r_x2
                pos_y = r_y2
            else:
                raise ValueError(
                    "Please use the following strings for rel_pos: "
                    "TL - top-left, "
                    "TC - top-center, TR - top-right, CL - center-left, "
                    "CC - center-center, CR - center-right, "
                    "BL - bottom-left, "
                    "BC - bottom-center, BR - bottom-right")
        self.pos_x = int(pos_x + offset_x)
        self.pos_y = int(pos_y + offset_y)

    def move_rel_to_obj_y(self, rel_obj):
        """Move obj relative to rel_obj in y direction. 
        Initially aligning centers of the vertical side of objects is 
        supported.

        Args:
            rel_obj (CanvasText | CanvasImg): Object in relation to 
                which we want to move obj. 

        Returns:
            None
        """

        # Find y coordinate of the center of rel_obj.
        r_x1, r_y1, r_x2, r_y2 = self.canvas.bbox(rel_obj.id_num)
        r_center_y = r_y2 - (r_y2 - r_y1) / 2

        # Find y coordinate of the center of our object.
        x1, y1, x2, y2 = self.canvas.bbox(self.id_num)
        center_y = y2 - (y2 - y1) / 2

        # Find the delta.
        dy = int(r_center_y - center_y)

        # Move obj.
        self.canvas.move(self.id_num, 0, dy)
        self.pos_y += dy


class CanvasText(CanvasObject):
    """Creates text object on canvas.

    Allows easier placement of text objects on canvas in relation to 
    other objects.

    Args:
        CanvasObject (object): Base class we inherit from.

    """

    def __init__(self, canvas, coordinates=None, rel_obj=None,
                 rel_pos=None, offset=None, **args):
        """Initialise class.

        Allows positioning in relation to the rel_obj (CanvasText or 
        CanvasImg object).
        We can give absolute position for the text or a relative one.
        In case of absolute position given we will ignore the relative 
        parameter.
        The offset allows us to move the text away from the border of 
        the relative object.
        In **args we place all the normal canvas.create_text method 
        parameters.

        Args:
            canvas (tk.Canvas): Canvas object to which the text will be 
                attached to.
            coordinates (tuple): Absolute x, y coordinates where to 
                place text in canvas. Overrides any parameters given in 
                relative parameters section.
            rel_obj (CanvasText / CanvasImg): CanvasText / CanvasImg 
                object which will be used as a relative one next to 
                which text is meant to be written.
            rel_pos (str): String determining position of newly created 
                text in relation to the relative object. Similar 
                concept to anchor.
                TL - top-left, TC - top-center, TR - top-right, 
                CL - center-left, CC - center-center,
                CR - center-right, BL - bottom-left, BC - bottom-center,
                BR - bottom-right
            offset (tuple): Offset given as a pair of values to move the
                newly created text away from the relative object.
            **args: All the other arguments we need to pass to 
                create_text method.

        :Attributes:
        :id_num (int): Unique Id number returned by create_text method 
            which will help us identify objects and obtain their 
            bounding boxes.

        """

        # Initialise base class. Get x-y coordinates for CanvasText
        # object.
        super().__init__(canvas, coordinates, rel_obj, rel_pos, offset)

        # Create text on canvas.
        id_num = canvas.create_text(self.pos_x, self.pos_y, **args)
        self.id_num = id_num


class CanvasImg(CanvasObject):
    """Creates image object on canvas.

    Allows easier placement of image objects on canvas in relation to 
    other objects.

    Args:
        CanvasObject (object): Base class we inherit from.

    """

    def __init__(self, canvas, image, coordinates=None, rel_obj=None,
                 rel_pos=None, offset=None, **args):
        """Initialise class.
         
        Allows positioning in relation to the rel_obj (CanvasText or 
        CanvasImg object).
        We can give absolute position for the image or a relative one.
        In case of absolute position given we will ignore the relative 
        parameter.
        The offset allows us to move the image away from the border of 
        the relative object.
        In **args we place all the normal canvas.create_image method 
        parameters.

        Args:
            canvas (tk.Canvas): Canvas object to which the text will be 
            attached to.
            image (str): String with a path to the image.
            coordinates (tuple): Absolute x, y coordinates where to 
                place image in canvas. Overrides any parameters given in
                relative parameters section.
            rel_obj (CanvasText / CanvasImg): CanvasText / CanvasImg 
                object which will be used as a relative one next to 
                which image is meant to be placed.
            rel_pos (str): String determining position of newly created 
                image in relation to the relative object. Similar 
                concept to anchor.
                TL - top-left, TC - top-center, TR - top-right, 
                CL - center-left, CC - center-center,
                CR - center-right, BL - bottom-left, BC - bottom-center,
                BR - bottom-right
            offset (tuple): Offset given as a pair of values to move the
                newly created text away from the relative object.
            **args: All the other arguments we need to pass to 
                create_text method.

        :Attributes:
            :id_num (int): Unique Id number returned by create_image 
                method which will help us identify objects and 
                obtain their bounding boxes.
            :img (PIL.ImageTk.PhotoImage): Image to display on canvas.

        """

        # Initialise base class. Get x-y coordinates for CanvasImg
        # object.
        super().__init__(canvas, coordinates, rel_obj, rel_pos, offset)

        # Prepare image for insertion. Should work with most image file
        # formats.
        img = Image.open(image)
        self.img = ImageTk.PhotoImage(img)
        id_num = canvas.create_image(self.pos_x, self.pos_y, image=self.img,
                                     **args)
        self.id_num = id_num


# Launch application.
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
