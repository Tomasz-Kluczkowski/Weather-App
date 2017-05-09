import tkinter as tk
from weather_backend import Report
from PIL import Image, ImageTk

#TODO: Have to add then a combobox with selection of previous locations.
#TODO: See if autocompletion is possible in the entry field.
#TODO: Add a small button to open a selection list of previous locations.

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
            var_status (tk.StringVar) -- S error message to be displayed in the 
                status bar.
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

        # GUI style definitions.
        font = "Georgia 16"
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
        canvas_cnf = {"bg": paper, "bd": 2, "height": 600,
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
        self.bind("<Return>", self.display_report)
        # Clear text from location entry button.
        # self.button_clear_normal_img = PhotoImage(file=r"Resources\Buttons\clear_entry_normal.png")
        # self.button_clear_hover_img = PhotoImage(file=r"Resources\Buttons\clear_entry_hover.png")
        self.clear_loc_button = tk.Button(self.loc_frame, text="X",
                                          command=self.clear_loc_entry, **clear_cnf)
        self.clear_loc_button.grid(row=0, column=2, sticky=tk.W, padx=(0, 4),
                                   pady=(4, 5))
        self.clear_loc_button.bind("<Return>", self.clear_loc_entry)
        # self.clear_loc_button.bind("<Enter>", self.hover_clear_button)
        # self.clear_loc_button.bind("<Leave>", self.normal_clear_button)

        # Metric units button.
        self.metric_button = tk.Button(self.loc_frame, text=u"\N{DEGREE SIGN}C",
                                       command=self.metric_pushed,
                                       **self.button_pushed_cnf)
        # self.metric_button.config(relief="sunken")
        self.metric_button.grid(row=0, column=3, padx=(4, 4), pady=(4, 4),
                                sticky=tk.W)

        # Imperial units button.
        self.imperial_button = tk.Button(self.loc_frame, text=u"\N{DEGREE SIGN}F",
                                         command=self.imperial_pushed,
                                         **self.button_released_cnf)
        # self.imperial_button.config(relief="raised")
        self.imperial_button.grid(row=0, column=4, padx=(4, 4), pady=(4, 4),
                                  sticky=tk.W)

        # Main display area canvas.
        self.main_canvas = tk.Canvas(self, **canvas_cnf)
        self.main_canvas.grid(row=1, column=0, columnspan=5, padx=(0, 0), pady=(0, 2), sticky=tk.NSEW)
        image = Image.open(r"Resources\Images\paradise-08.jpg")
        image_conv = ImageTk.PhotoImage(image)
        self.canvas_bg_img = image_conv
        print(type(self.canvas_bg_img))
        self.main_canvas.create_image(0, 0, image=self.canvas_bg_img,
                                      anchor=tk.NW)
        #
        # self.image = Image.open(r"Resources\Labels\location.png")
        # self.image_conv = ImageTk.PhotoImage(self.image)
        # self.canvas_img_1 = self.image_conv
        # self.main_canvas.create_image(20, 20, image=self.canvas_img_1, anchor=NW)

        canvas_text = self.main_canvas.create_text(100, 100, text="test text", font=font, fill=paper, anchor=tk.NW)

        # Error/Status Bar.
        self.status_bar_label = tk.Label(self, textvariable=self.var_status, **label_cnf)
        self.status_bar_label.grid(row=2, column=0, padx=(2, 2), pady=(0, 2), sticky=tk.NSEW)
        self.status_bar_label.configure(relief="sunken")

        # status / error bar
        # self.l_status = Label(self.text_frame, textvariable=self.var_status, width=30, style="my.TLabel")
        # self.l_status.grid(row=21, column=0, pady=4, sticky=W)


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

    def imperial_pushed(self, *args):
        """Activates imperial units and changes the look of the units buttons.
        *args contains event object passed automatically from imperial_button."""
        self.imperial_button.configure(**self.button_pushed_cnf)
        self.metric_button.configure(**self.button_released_cnf)

    def display_report(self, *args):
        """Obtains data from the report object and displays it in the main_canvas.
        *args contains event object passed automatically from loc_entry."""
        report.get_report(self.var_loc.get(), self.var_units.get())

app = WeatherApp()
report = Report()
app.mainloop()
