# Widget styles.
        style = tkk.Style()
        style.theme_use("vista")
        # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        style.configure("my.TCombobox",
                        fieldbackground=self.paper,
                        foreground="black",
                        )  # Location combobox.

loc_combobox = tkk.Combobox(loc_frame,
                            textvariable=self.v_link["var_loc"],
                            font=("Arial", -18),
                            width=70,
                            values=["test1", "test2",
                                    "test3"],
                            style="my.TCombobox")
loc_combobox.focus()
loc_combobox.grid(row=0, column=1, padx=(0, 0), pady=(4, 5),
                  sticky=tk.NSEW)
loc_combobox.bind("<Return>", lambda e: self.begin_get_report())
loc_combobox.bind("<Key>", lambda e: self.clear_error_message())