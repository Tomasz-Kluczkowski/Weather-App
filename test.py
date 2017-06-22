import tkinter as tk
import tkinter.ttk as tkk


class App:

    def __init__(self):
        root = tk.Tk()
        # Widget styles.
        style = tkk.Style()
        style.theme_use("default")
        # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

        style.configure("my.TFrame", relief="groove", bd=10,
                        background="red")
        style.configure("clear.TButton", foreground="blue", background="red",
                        borderwidth=10, relief="raised",
                        padding=(0, 0, 4, 0), width=1, anchor=tk.CENTER)

        style.configure("my.TCombobox",
                        fieldbackground="red",
                        foreground="black",
                        relief="raised",
                        )
        # LOCATION FRAME
        loc_frame = tkk.Frame(root, style="my.TFrame")
        loc_frame.grid(row=0, column=0, padx=(5, 5), pady=(10, 4), sticky=tk.EW)

        b3 = tkk.Button(loc_frame, text="Xenon", style="clear.TButton")
        b3.grid(row=0, column=0, sticky=tk.W, padx=0, pady=0)

        loc_combobox = tkk.Combobox(loc_frame,
                                    width=70,
                                    font=("Arial", -18),
                                    values=["test1", "test2",
                                            "test3"],
                                    style="my.TCombobox")
        loc_combobox.focus()
        loc_combobox.grid(row=1, column=0, padx=(0, 0), pady=(4, 5),
                          sticky=tk.NSEW)

        root.mainloop()

app = App()

