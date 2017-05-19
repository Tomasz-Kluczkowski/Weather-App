# Title: Weather App
# Author: Tomasz Kluczkowski
# email: tomaszk1@hotmail.co.uk


import tkinter as tk
from PIL import Image, ImageTk
from weather_backend import Report
from controller import Controller
import datetime


# TODO: Have to add then a combobox with selection of previous locations.
# TODO: See if autocompletion is possible in the entry field.
# TODO: Add a small button to open a selection list of previous locations.
# TODO: Add set to default location after successful call has been made.
# TODO: Add a frame around the location name label and entry and search
# TODO: button in dusty color to visualise that they belong together better.
# TODO: Add changing to other unit system when report already on screen without needing to press search button.


class WeatherApp(tk.Tk):
    """Class for generating graphic user interface for the weather application.
    
    Inherits from tk.TK object (main window).    
    We will apply Model-View-Controller(Adapter) architecture to the project to
    decouple each segment from the other. The View has no direct contact with the Model and vice versa.
    All communication is done via the Controller. 
    Due to the nature of tkinter library we have to initialise a root Tk object to which StringVar type variables
    and all the GUI elements are connected. Since there can be only one Tk object we have to create the WeatherApp class 
    object first (it inherits from Tk object) and then inside the class call Controller and Report classes. 
    Controller class will have access then to the same Tk object as the WeatherApp class. 
    
    Args:
        tk.TK  -- base class for the WeatherApp class. Tkinter main window (root) object.
    
    """

    def __init__(self):
        """Initializes WeatherApp class.
        
        Attributes:
            controller (Controller) -- Controller class object used for passing data between 
                the View (weather_gui) and the Model (weather_backend).
            dusty (Str) -- color definition in hex number.
            lavender (Str) -- color definition in hex number.
            overcast (Str) -- color definition in hex number.
            paper (Str) -- color definition in hex number.
            font (Str) -- font definition.
            title (str) -- Main window title displayed when using application.
            loc_frame (tk.Frame) -- Location frame, parent of all top bar objects.
            loc_label (tk.Label) -- Location label.
            loc_entry (tk.Entry) -- Location entry object. Here user can input 
                data which will be passed to var_loc.
            search_button (HoverButton) -- Search for weather report button.
            metric_button (HoverButton)   -- Metric units (degC, m/s) selection
                button.
            imperial_button (HoverButton)   -- Imperial units (degF / mile/hr) 
                selection button.
            main_canvas (tk.Canvas) -- Main canvas on which all of the weather 
                report will be visualised.
            canvas_bg_img (PIL.ImageTk.PhotoImage) -- Main canvas background 
                image. It is a conversion of a .jpg image using PIL module.
                
        """

        super().__init__()

        # Add Controller to the WeatherApp class instance.
        controller = Controller()
        self.controller = controller

        # Add main application instance as a View to the Controller.
        self.controller.add_view(self)

        # Create a Report object for backend operations.
        report = Report(self.controller)
        # Add it as a Model to the Controller class object.
        self.controller.add_model(report)

        # Color palette used:
        self.dusty = "#96858F"
        self.lavender = "#6D7993"
        self.overcast = "#9099A2"
        self.paper = "#D5D5D5"
        self.font = "Georgia 12"

        # Configure main window.
        self.title("The Weather App")
        self.config(bg=self.paper, bd=2, relief="groove")
        # Get screen size.
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        # Center application window.
        self.geometry("+{0}+0".format(int(s_width / 2) - 300))
        # Prevent resizing.
        self.resizable(width=tk.FALSE, height=tk.FALSE)

        # GUI style definitions.

        # Widget styles.
        frame_cnf = {"bg": self.overcast, "bd": 2, "relief": "groove"}
        label_cnf = {"fg": "black", "bg": self.dusty, "bd": 2, "padx": 4,
                     "pady": 9, "font": self.font, "relief": "groove"}
        entry_cnf = {"fg": "black", "bg": self.paper, "width": 40, "bd": 2,
                     "font": self.font, "relief": "sunken"}
        clear_cnf = {"bg": self.lavender, "fg": "black", "activebackground": self.dusty,
                     "activeforeground": self.paper, "padx": 2, "pady": 2,
                     "anchor": tk.CENTER, "font": self.font, "relief": "groove"}
        self.button_released_cnf = {"fg": "black", "bg": self.lavender,
                                    "activebackground": self.dusty,
                                    "activeforeground": self.paper, "bd": 2,
                                    "padx": 2, "pady": 2, "anchor": tk.CENTER,
                                    "width": 2, "font": self.font, "relief": "raised"}

        self.button_pushed_cnf = {"fg": self.paper, "bg": self.dusty,
                                  "activebackground": self.lavender,
                                  "activeforeground": "black", "bd": 2, "padx": 2,
                                  "pady": 2, "anchor": tk.CENTER, "width": 2,
                                  "font": self.font, "relief": "sunken"}
        canvas_cnf = {"bg": self.paper, "bd": 2, "height": 500,
                      "highlightbackground": self.paper,
                      "highlightcolor": self.paper, "relief": "groove"}

        # LAYOUT DESIGN.

        # Location frame.
        self.loc_frame = tk.Frame(self, **frame_cnf)
        self.loc_frame.grid(row=0, column=0, padx=(2, 2), pady=(2, 2),
                            sticky=tk.EW)

        # Location label.
        self.loc_label = tk.Label(self.loc_frame, text="Location name:", **label_cnf)
        self.loc_label.grid(row=0, column=0, padx=(4, 4), pady=(4, 4), sticky=tk.NSEW)

        # Location entry.
        self.loc_entry = tk.Entry(self.loc_frame,
                                  textvariable=self.controller.app_data["var_loc"],
                                  **entry_cnf)
        self.loc_entry.focus()
        self.loc_entry.grid(row=0, column=1, padx=(0, 0), pady=(4, 5),
                            sticky=tk.NSEW)
        self.loc_entry.bind("<Return>", self.begin_get_report)
        # If there is an error message and user starts to correct location name, remove error.
        self.loc_entry.bind("<Key>", self.clear_error_message)

        # Search button.
        self.search_img = tk.PhotoImage(file=r"Resources\Buttons\magnifier-tool.png")
        self.search_button = HoverButton(self.loc_frame, controller, "Press to get a weather report.",
                                         clear_cnf, image=self.search_img,
                                         command=self.begin_get_report)
        self.search_button.grid(row=0, column=2, sticky=tk.NSEW, padx=(0, 4), pady=(4, 5))
        # Press Enter to get report.
        self.search_button.bind("<Return>", self.begin_get_report)

        # Metric units button.
        self.metric_button = HoverButton(self.loc_frame, controller, "Press to change units to metric.",
                                         self.button_pushed_cnf,
                                         text=u"\N{DEGREE SIGN}C", command=self.metric_pushed)
        self.metric_button.grid(row=0, column=3, padx=(2, 4), pady=(4, 5),
                                sticky=tk.NSEW)

        # Imperial units button.
        self.imperial_button = HoverButton(self.loc_frame, controller,
                                           "Press to change units to imperial.",
                                           self.button_released_cnf,
                                           text=u"\N{DEGREE SIGN}F",
                                           command=self.imperial_pushed)
        self.imperial_button.grid(row=0, column=4, padx=(2, 4), pady=(4, 5),
                                  sticky=tk.NSEW)

        # Main display area canvas.
        self.main_canvas = tk.Canvas(self, **canvas_cnf)
        self.main_canvas.grid(row=1, column=0, columnspan=5, padx=(0, 0), pady=(0, 2), sticky=tk.NSEW)
        image = Image.open(r"Resources\Images\paradise-08.jpg")
        image_conv = ImageTk.PhotoImage(image)
        self.canvas_bg_img = image_conv
        self.main_canvas.create_image(0, 0, image=self.canvas_bg_img,
                                      anchor=tk.NW)

        # Error/Status Bar.
        self.status_bar_label = tk.Label(self, textvariable=self.controller.app_data["var_status"], **label_cnf)
        self.status_bar_label.grid(row=2, column=0, padx=(2, 2), pady=(0, 2), sticky=tk.NSEW)
        self.status_bar_label.configure(relief="sunken")

    def metric_pushed(self, *args):
        """Activates metric units and changes the look of the units buttons.
        *args contains event object passed automatically from metric_button."""

        self.imperial_button.configure(**self.button_released_cnf)
        self.metric_button.configure(**self.button_pushed_cnf)
        # If button is pushed when there is a report already on the screen get a new report with changed units.
        if self.controller.app_data["var_units"].get() == "imperial":
            self.controller.app_data["var_units"].set("metric")

            if self.controller.app_data["w_d_cur"] and self.controller.app_data["w_d_short"]\
                    and self.controller.app_data["w_d_long"]:
                self.begin_get_report()

    def imperial_pushed(self, *args):
        """Activates imperial units and changes the look of the units buttons.
        *args contains event object passed automatically from imperial_button."""

        self.metric_button.configure(**self.button_released_cnf)
        self.imperial_button.configure(**self.button_pushed_cnf)
        # If button is pushed when there is a report already on the screen get a new report with changed units.
        if self.controller.app_data["var_units"].get() == "metric":
            self.controller.app_data["var_units"].set("imperial")

            if self.controller.app_data["w_d_cur"] and self.controller.app_data["w_d_short"] \
                    and self.controller.app_data["w_d_long"]:
                self.begin_get_report()

    def clear_error_message(self, event):
        """Clears error messages from status_bar_label after user starts to correct an invalid location name.
        
        Args:
            event (event) -- tkinter.event object sent when a keyboard was pressed. 
        """
        if self.controller.app_data["error_status"] == -1:
            self.controller.app_data["var_status"].set("")
            self.controller.app_data["error_status"] = 0

    def begin_get_report(self, *args):
        """Begin getting data for the weather report to display it on the main_canvas.
        The call goes to the Controller first. Then to the Model.
        *args contains event object passed automatically from loc_entry."""

        # Do nothing if no location is entered.
        if self.controller.app_data["var_loc"].get() == "":
            return
        # Request a report using a Mediating Controller.
        self.controller.get_report()
        # Upon a successful contact with the API display the result in the GUI.
        if self.controller.app_data["error_status"] == 0:
            self.display_report()

    def display_report(self):
        """Display results of the API call in the main_canvas.
        
        Tags:
            main -- used for current weather parameters
        """

        # Delete a previous report if existing on canvas.
        self.main_canvas.delete("main")

        # Display location information.
        time = datetime.datetime.now()

        # Start coordinates in pixels of the report title.
        x1 = 10
        y1 = 10
        # Common config parameters for main section (current weather).
        main_cnf = {"tags": "main", "fill": self.paper, "anchor": tk.NW}
        img_cnf = {"tags": "main", "anchor": tk.NW}

        # Title placement.
        title_text = "Report for: {0}, {1}".format(self.controller.app_data["w_d_cur"]["name"],
                                                   self.controller.app_data["w_d_cur"]["sys"]["country"])
        title = CanvasText(self.main_canvas, (x1, y1), text=title_text, font="Georgia 18", **main_cnf)

        # Date placement.
        date_text = "Received at: {0}".format(time.strftime("%H:%M %Y/%m/%d"))
        date = CanvasText(self.main_canvas, rel_obj=title, rel_pos="BL", offset=(1, 5),
                          text=date_text, font="Georgia 12", **main_cnf)

        # Geo-coords placement.
        coords_text = "Lon: {0}, Lat: {1}".format(self.controller.app_data["w_d_cur"]["coord"]["lon"],
                                                  self.controller.app_data["w_d_cur"]["coord"]["lat"])
        coords = CanvasText(self.main_canvas, rel_obj=date, rel_pos="BL", offset=(1, 5),
                            text=coords_text, font="Georgia 12", **main_cnf)

        # Draw a current weather icon.
        icon_path = "Resources\Icons\Weather\\" + self.controller.app_data["w_d_cur"]["weather"][0]["icon"] + ".png"
        # Images have to be added as attributes or otherwise they get garbage collected and will not display at all.
        self.cur_icon = CanvasImg(self.main_canvas, icon_path, rel_obj=coords, rel_pos="BL", offset=(0, 50), **img_cnf)

        # Current temperature.
        if self.controller.app_data["var_units"].get() == "metric":
            sign = "C"
        else:
            sign = "F"
        cur_temp_text = "{0:.1f} \N{DEGREE SIGN}{1}".format(self.controller.app_data["w_d_cur"]["main"]["temp"], sign)

        cur_temp = CanvasText(self.main_canvas, rel_obj=self.cur_icon, rel_pos="TR", offset=(20, 5),
                              text=cur_temp_text, font="Georgia 20", **main_cnf)

        # Max temperature.
        max_temp_text = "max: {0} \N{DEGREE SIGN}{1}".format(self.controller.app_data["w_d_cur"]["main"]['temp_max'], sign)
        max_temp = CanvasText(self.main_canvas, rel_obj=cur_temp, rel_pos="TR", offset=(15, 0),
                              text=max_temp_text, font="Georgia 10", **main_cnf)
        # Min temperature.
        min_temp_text = "min: {0} \N{DEGREE SIGN}{1}".format(self.controller.app_data["w_d_cur"]["main"]['temp_min'], sign)
        min_temp = CanvasText(self.main_canvas, rel_obj=max_temp, rel_pos="BL", offset=(1, 0),
                              text=min_temp_text, font="Georgia 10", **main_cnf)

        # Weather description.
        w_desc_text = "{0}".format(self.controller.app_data["w_d_cur"]["weather"][0]["description"].title())
        w_desc = CanvasText(self.main_canvas, rel_obj=cur_temp, rel_pos="BL", offset=(1, 5),
                            text=w_desc_text, font="Georgia 12", **main_cnf)


class HoverButton(tk.Button):
    """Improves upon the standard button by adding status bar display option.
    
    We can use the same configuration dictionary as for the  standard tk.Button.

    Args:
        tk.Button (tk.Button) -- Standard tkinter Button object which we inherit from.
           
    """

    def __init__(self, master, controller, tip, cnf, **args):
        """Initialise MyButton.
        
        Args:
            master (tk.widget) -- Master widget to which MyButton (slave) instance will belong.
                The master widget is part of the WeatherApp object.
            controller (Controller) -- controller object which will store all the data required by each segment
                of the application.
            tip (Str) -- Tooltip text to display in the status_bar_label.
            cnf (Dict) -- Dictionary with the configuration for MyButton.
            **args -- Keyword arguments to further initialise the button.
            
        Attributes:
            tip (Str) -- Text to display in the status_bar_label of the app.
            controller (Controller) -- controller object which will store all the data required by each segment
                of the application. This has to be the same Controller as for the WeatherApp.
        
        """
        super().__init__(master, cnf, **args)
        self.controller = controller
        self.tip = tip
        # Action on entering the button with mouse.
        self.bind("<Enter>", self.enter_button)
        # Action on leaving the button with mouse.
        self.bind("<Leave>", self.leave_button)

    def enter_button(self, *args):
        """Displays information on button function to the user in the status_bar_label.
         *args contains event object passed automatically from the button."""
        self.controller.app_data["var_status"].set(self.tip)

    def leave_button(self, *args):
        """Clears status_bar_label after mouse leaves the button area.
        *args contains event object passed automatically from the button."""
        if self.controller.app_data["error_status"] == -1:
            self.controller.app_data["var_status"].set(self.controller.app_data["error_message"])
        else:
            self.controller.app_data["var_status"].set("")


class CanvasText(object):
    """Creates text object on canvas.

    Allows easier placement of text objects on canvas in relation to other objects.

    Args:
        object (object) -- Base Python object we inherit from.
    """

    def __init__(self, canvas, coordinates=None, rel_obj=None,
                 rel_pos=None, offset=None, **args):
        """Initialise class. 
        Allows positioning in relation to the rel_obj (CanvasText or CanvasImg object).
        We can give absolute position for the text or a relative one.
        In case of absolute position given we will ignore the relative parameter.
        The offset allows us to move the text away from the border of the relative object.
        In **args we place all the normal canvas.create_text method parameters.

        Args:
            canvas (tk.Canvas) -- Canvas object to which the text will be attached to.
            coordinates (Tuple) -- Absolute x, y coordinates where to place text in canvas. Overrides any parameters
                given in relative parameters section.
            rel_obj (CanvasText / CanvasImg) -- CanvasText / CanvasImg object which will be used
                as a relative one next to which text is meant to be written.
            rel_pos (Str) -- String determining position of newly created text in relation to the relative object.
                Similar concept to anchor.
                TL - top-left, TM - top-middle, TR - top-right, CL - center-left, CC - center-center, 
                CR - center-right, BL - bottom-left, BC - bottom-center, BR - bottom-right
            offset (Tuple) -- Offset given as a pair of values to move the newly created text
                away from the relative object.
            **args -- All the other arguments we need to pass to create_text method.
        
        Attributes:
            id_num (int) -- Unique Id number returned by create_text method which will help us identify objects
                and obtain their bounding boxes.
        """
        # Create text on canvas.
        # If absolute position is given relative parameters are ignored.
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
            # Get Top-Left and Bottom-Right bounding points of the relative object.
            r_x1, r_y1, r_x2, r_y2 = canvas.bbox(rel_obj.id_num)
            # TL - top - left, TM - top - middle, TR - top - right, CL - center - left, CC - center - center,
            # CR - center - right, BL - bottom - left, BC - bottom - center, BR - bottom - right

            # Determine position of CanvasText on canvas in relation to the rel_obj.
            if rel_pos == "TL":
                pos_x = r_x1
                pos_y = r_y1
            elif rel_pos == "TM":
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

        id_num = canvas.create_text(pos_x + offset_x, pos_y + offset_y, **args)
        # Store unique Id number returned from using canvas.create_text method as an instance attribute.
        self.id_num = id_num


class CanvasImg(object):
    """Creates image object on canvas.

    Allows easier placement of image objects on canvas in relation to other objects.

    Args:
        object (object) -- Base Python object we inherit from.
    """

    def __init__(self, canvas, image, coordinates=None, rel_obj=None,
                 rel_pos=None, offset=None, **args):
        """Initialise class. 
        Allows positioning in relation to the rel_obj (CanvasText or CanvasImg object).
        We can give absolute position for the image or a relative one.
        In case of absolute position given we will ignore the relative parameter.
        The offset allows us to move the image away from the border of the relative object.
        In **args we place all the normal canvas.create_image method parameters.

        Args:
            canvas (tk.Canvas) -- Canvas object to which the text will be attached to.
            image (Str) -- String with a path to the image.
            coordinates (Tuple) -- Absolute x, y coordinates where to place text in canvas. Overrides any parameters
                given in relative parameters section.
            rel_obj (CanvasText / CanvasImg) -- CanvasText / CanvasImg object which will be used
                as a relative one next to which text is meant to be written.
            rel_pos (Str) -- String determining position of newly created text in relation to the relative object.
                Similar concept to anchor.
                TL - top-left, TM - top-middle, TR - top-right, CL - center-left, CC - center-center, 
                CR - center-right, BL - bottom-left, BC - bottom-center, BR - bottom-right
            offset (Tuple) -- Offset given as a pair of values to move the newly created text
                away from the relative object.
            **args -- All the other arguments we need to pass to create_text method.

        Attributes:
            id_num (int) -- Unique Id number returned by create_image method which will help us identify objects
                and obtain their bounding boxes.
        """
        # Create text on canvas.
        # If absolute position is given relative parameters are ignored.
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
            # Get Top-Left and Bottom-Right bounding points of the relative object.
            r_x1, r_y1, r_x2, r_y2 = canvas.bbox(rel_obj.id_num)
            # TL - top - left, TM - top - middle, TR - top - right, CL - center - left, CC - center - center,
            # CR - center - right, BL - bottom - left, BC - bottom - center, BR - bottom - right

            # Determine position of CanvasImg on canvas in relation to the rel_obj.
            if rel_pos == "TL":
                pos_x = r_x1
                pos_y = r_y1
            elif rel_pos == "TM":
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

        # Prepare image for insertion. Should work with most image file formats.
        img = Image.open(image)
        self.img = ImageTk.PhotoImage(img)
        id_num = canvas.create_image(pos_x + offset_x, pos_y + offset_y, image=self.img, **args)
        # Store unique Id number returned from using canvas.create_image method as an instance attribute.
        self.id_num = id_num


# Launch application.
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
