# Title: Weather App
# Author: Tomasz Kluczkowski
# email: tomaszk1@hotmail.co.uk


import tkinter as tk
from PIL import Image, ImageTk
from weather_backend import Report
from controller import Controller


# TODO: Have to add then a combobox with selection of previous locations.
# TODO: See if autocompletion is possible in the entry field.
# TODO: Add a small button to open a selection list of previous locations.
# TODO: Add set to default location after successful call has been made.
# TODO: Add a frame around the location name label and entry and search
# TODO: button in dusty color to visualise that they belong together better.
# TODO: implement a controller to pass variables between classes.


class WeatherApp(tk.Tk):
    """Class for generating graphic user interface for the weather application.
    
    Inherits from tk.TK object (main window).    
    We will apply Model-View-Controller(Adapter) architecture to the project to
    decouple each segment from the other. The View has no direct contact with the Model and vice versa.
    All communication is done via the Controller. 
    Due to the nature of tkinter library we have to initialise a root Tk object to which StringVar type variables
    and all the GUI elements are connected. Since there can be only one Tk object we have to create the WeaterApp class 
    object first (it inherits from Tk object) and then inside the class call Controller and Report classes. 
    Controller class will have access then to the same Tk object as the WeatherApp class. 
    Therefore a complete 100% separation of Model / View / Controller is not possible (but we are very close :)).
    
    Args:
        tk.TK  -- base class for the WeatherApp class. Tkinter main window (root) object.
    
    """

    def __init__(self):
        """Initializes WeatherApp class.
        
        Attributes:
            controller (Controller) -- Controller class object used for passing data between 
                the View (weather_gui) and the Model (weather_backend).
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

        # Configure main window.
        self.title("The Weather App")
        self.config(bg=paper, bd=2, relief="groove")
        # self.geometry("1000x800")
        self.resizable(width=tk.FALSE, height=tk.FALSE)

        # GUI style definitions.

        # Color palette used:
        dusty = "#96858F"
        lavender = "#6D7993"
        overcast = "#9099A2"
        paper = "#D5D5D5"
        font = "Georgia 12"

        # Widget styles.
        frame_cnf = {"bg": overcast, "bd": 2, "relief": "groove"}
        label_cnf = {"fg": "black", "bg": dusty, "bd": 2, "padx": 4,
                     "pady": 9, "font": font, "relief": "groove"}
        entry_cnf = {"fg": "black", "bg": paper, "width": 40, "bd": 2,
                     "font": font, "relief": "sunken"}
        clear_cnf = {"bg": lavender, "fg": "black", "activebackground": dusty,
                     "activeforeground": paper, "padx": 2, "pady": 2,
                     "anchor": tk.CENTER, "font": font, "relief": "groove"}
        self.button_released_cnf = {"fg": "black", "bg": lavender,
                                    "activebackground": dusty,
                                    "activeforeground": paper, "bd": 2,
                                    "padx": 2, "pady": 2, "anchor": tk.CENTER,
                                    "width": 2, "font": font, "relief": "raised"}

        self.button_pushed_cnf = {"fg": paper, "bg": dusty,
                                  "activebackground": lavender,
                                  "activeforeground": "black", "bd": 2, "padx": 2,
                                  "pady": 2, "anchor": tk.CENTER, "width": 2,
                                  "font": font, "relief": "sunken"}
        canvas_cnf = {"bg": paper, "bd": 2, "height": 500,
                      "highlightbackground": paper,
                      "highlightcolor": paper, "relief": "groove"}

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
        self.loc_entry.bind("<Return>", self.display_report)
        # If there is an error message and user starts to correct location name, remove error.
        self.loc_entry.bind("<Key>", self.clear_error_message)

        # Search button.
        self.search_img = tk.PhotoImage(file=r"Resources\Buttons\magnifier-tool.png")
        self.search_button = HoverButton(self.loc_frame, controller, "Press to get a weather report.",
                                         clear_cnf, image=self.search_img,
                                         command=self.display_report)
        self.search_button.grid(row=0, column=2, sticky=tk.NSEW, padx=(0, 4), pady=(4, 5))
        # Press Enter to get report.
        self.search_button.bind("<Return>", self.display_report)

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
        canvas_text = self.main_canvas.create_text(100, 100, text="test text", font=font, fill=paper, anchor=tk.NW)

        # Error/Status Bar.
        self.status_bar_label = tk.Label(self, textvariable=self.controller.app_data["var_status"], **label_cnf)
        self.status_bar_label.grid(row=2, column=0, padx=(2, 2), pady=(0, 2), sticky=tk.NSEW)
        self.status_bar_label.configure(relief="sunken")

    def metric_pushed(self, *args):
        """Activates metric units and changes the look of the units buttons.
        *args contains event object passed automatically from metric_button."""
        self.imperial_button.configure(**self.button_released_cnf)
        self.metric_button.configure(**self.button_pushed_cnf)
        self.controller.app_data["var_units"].set("metric")

    def imperial_pushed(self, *args):
        """Activates imperial units and changes the look of the units buttons.
        *args contains event object passed automatically from imperial_button."""
        self.metric_button.configure(**self.button_released_cnf)
        self.imperial_button.configure(**self.button_pushed_cnf)
        self.controller.app_data["var_units"].set("imperial")

    def clear_error_message(self, event):
        """Clears error messages from status_bar_label after user starts to correct an invalid location name.
        Args:
            event (event) -- tkinter.event object sent when a keyboard was pressed. 
        """
        if self.controller.app_data["error_status"] == -1:
            self.controller.app_data["var_status"].set("")
            self.controller.app_data["error_status"] = 0

    def display_report(self, *args):
        # TODO: REMOVE DIRECT CALL TO THE REPORT CLASS FOR DATA.
        # TODO: THE CALL SHOULD BE TO THE CONTROLLER WHICH WILL THEN GET THE DATA AND GIVE IT TO THE GUI.
        """Obtains data from the report object and displays it in the main_canvas.
        *args contains event object passed automatically from loc_entry."""

        # Do nothing if no location is entered.
        if self.controller.app_data["var_loc"].get() == "":
            return
        # Request a report using a mediating controller.
        self.controller.request_report(self.controller.app_data["var_loc"].get(),
                                       self.controller.app_data["var_units"].get())
        # # Error handling.
        # # We expect a tuple returning from get_report. Item 0 contains error status.
        # self.controller.app_data["error_status"] = data[0]
        # if self.controller.app_data["error_status"] == -1:
        #     self.controller.app_data["error_message"] = data[1]
        #     self.controller.app_data["var_status"].set(data[1])
        # else:
        #     # Clear any error status and message upon successful response from API.
        #     self.controller.app_data["var_status"].set("")
        #     self.controller.app_data["error_message"] = ""
        #     # Unpack dictionaries from data
        #     # self.w_d_cur, self.w_d_short, self.w_d_long = data[1]


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
                of the application.
        
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


# Launch application.
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
