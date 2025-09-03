import tkinter as tk
from cch_his_auto.common_structs import User


class UsernamePasswordFrame(tk.LabelFrame):
    def __init__(self, parent, text: str, *args, **kwargs):
        super().__init__(parent, text=text, *args, **kwargs)
        self.columnconfigure(1, weight=1)

        self.name_var = tk.StringVar()
        self.password_var = tk.StringVar()
        tk.Label(self, text="name").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1)
        tk.Label(self, text="password").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.password_var).grid(row=1, column=1)

    def get_user(self) -> User:
        return User(self.name_var.get(), self.password_var.get())

    def set_user(self, value: User):
        self.name_var.set(value.name)
        self.password_var.set(value.password)


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
