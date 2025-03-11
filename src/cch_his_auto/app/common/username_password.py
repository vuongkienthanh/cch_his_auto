import tkinter as tk

class UsernamePasswordFrame(tk.LabelFrame):
    def __init__(self, parent, label: str, *args, **kwargs):
        super().__init__(parent, text=label, *args, **kwargs)
        self.username_var = tk.StringVar()
        username_label = tk.Label(self, text="username")
        username_entry = tk.Entry(self, textvariable=self.username_var)
        self.password_var = tk.StringVar()
        password_label = tk.Label(self, text="password")
        passord_entry = tk.Entry(self, show="*", textvariable=self.password_var)

        self.columnconfigure(1, weight=1)

        username_label.grid(row=0, column=0)
        password_label.grid(row=1, column=0)
        username_entry.grid(row=0, column=1)
        passord_entry.grid(row=1, column=1)

    def get_username(self):
        return self.username_var.get()

    def set_username(self, value: str):
        return self.username_var.set(value)

    def get_password(self):
        return self.password_var.get()

    def set_password(self, value: str):
        return self.password_var.set(value)
