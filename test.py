import tkinter as tk
import tkinter.ttk as tkk


class App:

    def __init__(self):
        root = tk.Tk()
        # Widget styles.
        style = tkk.Style()
        style.theme_use("winnative")
        # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

        style.configure("my.TFrame", relief="groove", borderwidth=10,
                        background="yellow")
        style.configure("clear.TButton", foreground="blue", background="red",
                        borderwidth=10, relief="sunken",
                        padding=(0, 0, 4, 0), width=5, anchor=tk.CENTER)

        style.configure("my.TCombobox",
                        fieldbackground="white",
                        foreground="black",
                        borderwidth=0,
                        relief="flat",
                        )
        # LOCATION FRAME
        loc_frame = tkk.Frame(root, style="my.TFrame", relief="sunken")
        loc_frame.grid(row=0, column=0, padx=(5, 5), pady=(10, 4), sticky=tk.EW)



        b3 = tkk.Button(loc_frame, text="Xenon", style="clear.TButton")
        b3.grid(row=0, column=0, sticky=tk.W, padx=(5, 5), pady=(5, 5))

        combo_frame = tkk.Frame(loc_frame, style="my.TFrame")
        combo_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=(5, 5), pady=(10, 4))

        loc_combobox = tkk.Combobox(combo_frame,
                                    width=70,
                                    font=("Arial", -18),
                                    values=["test1", "test2",
                                            "test3"],
                                    style="my.TCombobox")
        loc_combobox.focus()
        loc_combobox.grid(row=0, column=0, padx=(5, 5), pady=(5, 5),
                          sticky=tk.NSEW)

        root.mainloop()

app = App()

