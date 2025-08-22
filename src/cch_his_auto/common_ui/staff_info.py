import tkinter as tk


class UsernamePasswordFrame(tk.LabelFrame):
    def __init__(self, parent, text: str, *args, **kwargs):
        super().__init__(parent, text=text, *args, **kwargs)
        self.columnconfigure(1, weight=1)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        tk.Label(self, text="username").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.username_var).grid(row=0, column=1)
        tk.Label(self, text="password").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.password_var).grid(row=1, column=1)

    def get_username(self):
        return self.username_var.get()

    def set_username(self, value: str):
        return self.username_var.set(value)

    def get_password(self):
        return self.password_var.get()

    def set_password(self, value: str):
        return self.password_var.set(value)


class UsernamePasswordDeptFrame(UsernamePasswordFrame):
    def __init__(self, parent, text: str, *args, **kwargs):
        super().__init__(parent, text=text, *args, **kwargs)
        self.dept_var = tk.StringVar()
        tk.Label(self, text="Khoa lâm sàng:", justify="right").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.dept_var).grid(row=2, column=1)

    def get_department(self) -> str:
        return self.dept_var.get()

    def set_department(self, value: str):
        self.dept_var.set(value)
