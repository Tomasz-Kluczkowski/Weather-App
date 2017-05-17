import tkinter as tk

# Coordinates that the cur_icon occupies.
x1, y1, x2, y2 = self.main_canvas.bbox(cur_icon_id)

# Current temperature.
if self.controller.app_data["var_units"].get() == "metric":
    sign = "C"
else:
    sign = "F"
cur_temp = "{0:.1f} \N{DEGREE SIGN}{1}".format(self.controller.app_data["w_d_cur"]["main"]["temp"], sign)
cur_temp_id = self.main_canvas.create_text(x2 + 10, y1, text=cur_temp, font="Georgia 20", tags="main",
                                           fill=self.paper, anchor=tk.NW)

class CanvasText(object):
    """Creates text object on canvas.
    
    Adds text object's coordinates and its rectangle parameters to a dictionary in the controller which later 
    can be accessed to allow easier placement of other objects on the canvas in relation to other objects.
    
    Args:
    
    """

    def __init__(self):

