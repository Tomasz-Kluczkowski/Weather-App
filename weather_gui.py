import tkinter as tk
from weather_backend import Report
from PIL import Image, ImageTk

#TODO: Have to add then a combobox with selection of previous locations.
#TODO: See if autocompletion is possible in the entry field.
#TODO: Add a small button to open a selection list of previous locations.
#TODO: Add displaying info in status_bar_label when entering text into loc_entry (press enter to get report) and
#TODO: when hovering over buttons what they do.

class WeatherApp(tk.Tk):
    """Class for generating graphic user interface for the weather application.
    
    Inherits from tk.TK object (main window).
    
    Args:
        tk.TK  -- base class for the WeatherApp class
    
    """

    def __init__(self):
        """Initializes WeatherApp class.
        
        This class is used to generate the graphic user interface for the Weather 
        App. Its methods are directly related to the function of the buttons and 
        entry.
        
        Attributes:
            title (str) -- Main window title displayed when using application.
            var_units (tk.StringVar) -- Value of selection of units (metric / imperial).
            var_status (tk.StringVar) -- Stores error message to be displayed in the 
                status bar.
            error_message (Str) -- Last error message.
            error_status (Int) -- Value -1 means an error occurred and was not cleared. 0 means all ok.
            loc_frame (tk.Frame) -- Location frame, parent of all top bar objects.
            loc_label (tk.Label) -- Location label.
            var_loc (tk.StringVar) -- Tkinter text variable assigned to the 
                location entry object.
            loc_entry (tk.Entry) -- Location entry object. Here user can input 
                data which will be passed to var_loc.
            clear_loc_button (tk.Button) -- Clear location entry button. When 
                pressed deletes text entered into the loc_entry box.
            metric_button (tk.Button)   -- Metric units (degC, m/s) selection
                button.
            imperial_button (tk.Button)   -- Imperial units (degF / mile/hr) 
                selection button.
            main_canvas (tk.Canvas) -- Main canvas on which all of the weather 
                report will be visualised.
            canvas_bg_img (PIL.ImageTk.PhotoImage) -- Main canvas background 
                image. It is a conversion of a .jpg image using PIL module.
                
        """

        super().__init__()
        # Color palettes used:
        # morning_sky = "#CAE4D8"
        # honey = "#DCAE1D"
        # cerulean = "#00303F"
        # mist = "#7A9D96"
        #
        # pale_gold = "#C0B283"
        dusty = "#96858F"
        lavender = "#6D7993"
        overcast = "#9099A2"
        paper = "#D5D5D5"

        # Configure main window.
        self.title("The Weather App")
        self.config(bg=paper, bd=2, relief="groove")
        # self.geometry("1000x800")
        self.resizable(width=tk.FALSE, height=tk.FALSE)
        # Set main variables.
        self.var_units = tk.StringVar(value="metric")
        self.var_status = tk.StringVar(value="")
        self.error_message = ""
        self.error_status = 0
        self.w_d_cur = {}
        self.w_d_short = {}
        self.w_d_long = {}

        # GUI style definitions.
        font = "Georgia 12"
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
        # self.location_img = tk.PhotoImage(file=r"Resources\Labels\location.png")
        self.loc_label = tk.Label(self.loc_frame, text="Location name:", **label_cnf)
        # image=self.location_img, compound=tk.CENTER)
        self.loc_label.grid(row=0, column=0, padx=(4, 4), pady=(4, 4), sticky=tk.NSEW)

        # Location entry.
        self.var_loc = tk.StringVar()
        self.loc_entry = tk.Entry(self.loc_frame, textvariable=self.var_loc,
                                  **entry_cnf)
        self.loc_entry.focus()
        self.loc_entry.grid(row=0, column=1, padx=(0, 0), pady=(4, 5),
                            sticky=tk.NSEW)
        # Pressing enter while in location entry calls get_report function.
        self.loc_entry.bind("<Return>", self.display_report)
        # Clear text from loc_entry button.
        self.clear_loc_button = tk.Button(self.loc_frame, text="X",
                                          command=self.clear_loc_entry, **clear_cnf)
        self.clear_loc_button.grid(row=0, column=2, sticky=tk.W, padx=(0, 4),
                                   pady=(4, 5))
        self.clear_loc_button.bind("<Return>", self.clear_loc_entry)

        # Metric units button.
        self.metric_button = tk.Button(self.loc_frame, text=u"\N{DEGREE SIGN}C",
                                       command=self.metric_pushed,
                                       **self.button_pushed_cnf)
        self.metric_button.grid(row=0, column=3, padx=(4, 4), pady=(4, 4),
                                sticky=tk.W)
        # Action on entering the button with mouse.
        self.metric_button.bind("<Enter>", self.enter_metric_button)
        # Action on leaving the button with mouse.
        self.metric_button.bind("<Leave>", self.leave_metric_button)



        # Imperial units button.
        self.imperial_button = tk.Button(self.loc_frame, text=u"\N{DEGREE SIGN}F",
                                         command=self.imperial_pushed,
                                         **self.button_released_cnf)
        self.imperial_button.grid(row=0, column=4, padx=(4, 4), pady=(4, 4),
                                  sticky=tk.W)
        # Action on entering the button with mouse.
        self.imperial_button.bind("<Enter>", self.enter_imperial_button)
        # Action on leaving the button with mouse.
        self.imperial_button.bind("<Leave>", self.leave_imperial_button)

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
        self.status_bar_label = tk.Label(self, textvariable=self.var_status, **label_cnf)
        self.status_bar_label.grid(row=2, column=0, padx=(2, 2), pady=(0, 2), sticky=tk.NSEW)
        self.status_bar_label.configure(relief="sunken")

    def clear_loc_entry(self, *args):
        """Empties text from loc_entry. *args contains event object passed 
        automatically from clear_loc_button."""
        self.loc_entry.delete(0, tk.END)
        self.loc_entry.focus()

    def metric_pushed(self, *args):
        """Activates metric units and changes the look of the units buttons.
        *args contains event object passed automatically from metric_button."""
        self.metric_button.configure(**self.button_pushed_cnf)
        self.imperial_button.configure(**self.button_released_cnf)
        self.var_units.set("metric")

    def enter_metric_button(self, *args):
        """Displays information on button function to the user in the status_bar_label.
         *args contains event object passed automatically from metric_button."""
        self.var_status.set("Press to change units to metric")

    def leave_metric_button(self, *args):
        """Clears status_bar_label after mouse leaves the metric_button area.
        *args contains event object passed automatically from metric_button.
        """
        if self.error_status == -1:
            self.var_status.set(self.error_message)
        else:
            self.var_status.set("")

    def imperial_pushed(self, *args):
        """Activates imperial units and changes the look of the units buttons.
        *args contains event object passed automatically from imperial_button."""
        self.imperial_button.configure(**self.button_pushed_cnf)
        self.metric_button.configure(**self.button_released_cnf)
        self.var_units.set("imperial")

    def enter_imperial_button(self, *args):
        """Displays information on button function to the user in the status_bar_label.
         *args contains event object passed automatically from metric_button."""
        self.var_status.set("Press to change units to imperial")

    def leave_imperial_button(self, *args):
        """Clears status_bar_label after mouse leaves the imperial_button area.
        *args contains event object passed automatically from metric_button."""
        if self.error_status == -1:
            self.var_status.set(self.error_message)
        else:
            self.var_status.set("")

    def display_report(self, *args):
        """Obtains data from the report object and displays it in the main_canvas.
        *args contains event object passed automatically from loc_entry."""
        # We expect a tuple returning from get_report. Item 0 contains error status.
        data = report.get_report(self.var_loc.get(), self.var_units.get())
        # Error handling.
        self.error_status = data[0]
        if self.error_status == -1:
            self.error_message = data[1]
            self.var_status.set(data[1])
        else:
            # Clear error status upon successful response from API.
            self.var_status.set("")
            # Unpack dictionaries from data
            self.w_d_cur, self.w_d_short, self.w_d_long = data[1]


app = WeatherApp()
report = Report()
app.mainloop()
