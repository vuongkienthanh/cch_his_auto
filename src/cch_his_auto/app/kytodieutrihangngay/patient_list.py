import tkinter as tk
from typing import cast

from .config import PHCN_ORDER, Patient
from ..common.scrollable_frame import ScrollFrame

class PatientFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        header = tk.Frame(self)
        header.grid(row=0, column=0, sticky="WE")
        header.columnconfigure(0, weight=1, minsize=200)
        header.columnconfigure(1, minsize=120)
        header.columnconfigure(2, minsize=120)
        header.columnconfigure(3, minsize=180)
        header.columnconfigure(4, minsize=180)
        header.columnconfigure(5, minsize=80)

        url = tk.Label(header, text="url", relief="raised", anchor="center")
        ky_xetnghiem = tk.Label(
            header, text="Ký xét nghiệm", relief="raised", anchor="center"
        )
        ky_todieutri = tk.Label(
            header, text="Ký tờ điều trị", relief="raised", anchor="center"
        )
        ky_3tra = tk.Label(
            header, text="Vị trí ký 3tra", relief="raised", anchor="center"
        )
        phcn = tk.Label(header, text="Đăng ký PHCN", relief="raised", anchor="center")
        delete_btn = tk.Label(header, text="Xóa", relief="raised", anchor="center")

        url.grid(row=0, column=0, sticky="NSEW")
        ky_xetnghiem.grid(row=0, column=1, sticky="NSEW")
        ky_todieutri.grid(row=0, column=2, sticky="NSEW")
        ky_3tra.grid(row=0, column=3, sticky="NSEW")
        phcn.grid(row=0, column=4, sticky="NSEW")
        delete_btn.grid(row=0, column=5, sticky="NSWE", padx=(0, 15))

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.listframe = PatientList(self)
        self.listframe.grid(row=1, column=0, sticky="NSEW")

    def add_new(self):
        self.listframe.add_new()

    def add_patient(self, patient: Patient):
        self.listframe.add_patient(patient)

    def get_patients(self) -> list[Patient]:
        return self.listframe.get_patients()

    def clear(self):
        self.listframe.clear()

class PatientList(ScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.viewPort.columnconfigure(0, weight=1)

    def add_new(self):
        line = Line(self.viewPort)
        line.grid(row=len(self.viewPort.grid_slaves()), column=0, sticky="EW")

    def add_patient(self, patient: Patient):
        line = Line(self.viewPort)
        line.set_patient(patient)
        line.grid(row=len(self.viewPort.grid_slaves()), column=0, sticky="EW")

    def get_patients(self) -> list[Patient]:
        return [cast(Line, p).to_patient() for p in self.viewPort.grid_slaves()[::-1]]

    def clear(self):
        for w in self.viewPort.grid_slaves():
            w.destroy()

class Line(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.url_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.xn_var = tk.BooleanVar()
        self.tdt_var = tk.BooleanVar()
        self.bs_0_var = tk.BooleanVar()
        self.bs_1_var = tk.BooleanVar()
        self.bs_2_var = tk.BooleanVar()
        self.bs_3_var = tk.BooleanVar()
        self.bs_4_var = tk.BooleanVar()
        self.dd_0_var = tk.BooleanVar()
        self.dd_1_var = tk.BooleanVar()
        self.dd_2_var = tk.BooleanVar()
        self.dd_3_var = tk.BooleanVar()
        self.dd_4_var = tk.BooleanVar()
        self.bunuot_var = tk.BooleanVar()
        self.giaotiep_var = tk.BooleanVar()
        self.hohap_var = tk.BooleanVar()
        self.vandong_var = tk.BooleanVar()

        info_frame = tk.Frame(self)
        url_entry = tk.Entry(info_frame, textvariable=self.url_var)
        note_label = tk.Label(info_frame, text="note")
        note_entry = tk.Entry(info_frame, textvariable=self.note_var)

        xn_checkbox = tk.Checkbutton(self, variable=self.xn_var)
        tdt_checkbox = tk.Checkbutton(self, variable=self.tdt_var)
        tdt_checkbox.select()

        k3t = tk.Frame(self, borderwidth=10)
        k3t_bs = tk.LabelFrame(k3t, text="Bác sĩ")
        k3t_dd = tk.LabelFrame(k3t, text="Điều dưỡng")
        k3t_bs_0 = tk.Checkbutton(k3t_bs, variable=self.bs_0_var)
        k3t_bs_1 = tk.Checkbutton(k3t_bs, variable=self.bs_1_var)
        k3t_bs_2 = tk.Checkbutton(k3t_bs, variable=self.bs_2_var)
        k3t_bs_3 = tk.Checkbutton(k3t_bs, variable=self.bs_3_var)
        k3t_bs_4 = tk.Checkbutton(k3t_bs, variable=self.bs_4_var)
        k3t_dd_0 = tk.Checkbutton(k3t_dd, variable=self.dd_0_var)
        k3t_dd_1 = tk.Checkbutton(k3t_dd, variable=self.dd_1_var)
        k3t_dd_2 = tk.Checkbutton(k3t_dd, variable=self.dd_2_var)
        k3t_dd_3 = tk.Checkbutton(k3t_dd, variable=self.dd_3_var)
        k3t_dd_4 = tk.Checkbutton(k3t_dd, variable=self.dd_4_var)

        phcn = tk.Frame(self)
        bunuot = tk.Checkbutton(phcn, variable=self.bunuot_var, text=PHCN_ORDER[0])
        giaotiep = tk.Checkbutton(phcn, variable=self.giaotiep_var, text=PHCN_ORDER[1])
        hohap = tk.Checkbutton(phcn, variable=self.hohap_var, text=PHCN_ORDER[2])
        vandong = tk.Checkbutton(phcn, variable=self.vandong_var, text=PHCN_ORDER[3])

        delete_button = tk.Button(self, text="Xóa", command=self.destroy)

        self.columnconfigure(0, weight=1, minsize=200)
        self.columnconfigure(1, minsize=120)
        self.columnconfigure(2, minsize=120)
        self.columnconfigure(3, minsize=180)
        self.columnconfigure(4, minsize=180)
        self.columnconfigure(5, minsize=80)

        info_frame.columnconfigure(1, weight=1)
        info_frame.grid(row=0, column=0, sticky="WE")
        url_entry.grid(row=0, column=0, sticky="WE", columnspan=2)
        note_label.grid(row=1, column=0)
        note_entry.grid(row=1, column=1, sticky="WE")

        xn_checkbox.grid(row=0, column=1)
        tdt_checkbox.grid(row=0, column=2)

        k3t.grid(row=0, column=3)
        k3t_bs.grid(row=0, column=0)
        k3t_bs_0.grid(row=0, column=0)
        k3t_bs_1.grid(row=0, column=1)
        k3t_bs_2.grid(row=0, column=2)
        k3t_bs_3.grid(row=0, column=3)
        k3t_bs_4.grid(row=0, column=4)
        k3t_dd.grid(row=1, column=0)
        k3t_dd_0.grid(row=0, column=0)
        k3t_dd_1.grid(row=0, column=1)
        k3t_dd_2.grid(row=0, column=2)
        k3t_dd_3.grid(row=0, column=3)
        k3t_dd_4.grid(row=0, column=4)

        phcn.grid(
            row=0,
            column=4,
        )
        bunuot.grid(row=0, column=0, sticky="w")
        giaotiep.grid(row=1, column=0, sticky="w")
        hohap.grid(row=2, column=0, sticky="w")
        vandong.grid(row=3, column=0, sticky="w")

        delete_button.grid(row=0, column=5)

    def set_patient(self, patient: Patient):
        self.url_var.set(patient["url"])
        self.note_var.set(patient["note"])
        self.xn_var.set(patient["ky_xetnghiem"])
        self.tdt_var.set(patient["ky_todieutri"])
        self.bs_0_var.set(patient["ky_3tra"]["bacsi"][0])
        self.bs_1_var.set(patient["ky_3tra"]["bacsi"][1])
        self.bs_2_var.set(patient["ky_3tra"]["bacsi"][2])
        self.bs_3_var.set(patient["ky_3tra"]["bacsi"][3])
        self.bs_4_var.set(patient["ky_3tra"]["bacsi"][4])
        self.dd_0_var.set(patient["ky_3tra"]["dieuduong"][0])
        self.dd_1_var.set(patient["ky_3tra"]["dieuduong"][1])
        self.dd_2_var.set(patient["ky_3tra"]["dieuduong"][2])
        self.dd_3_var.set(patient["ky_3tra"]["dieuduong"][3])
        self.dd_4_var.set(patient["ky_3tra"]["dieuduong"][4])
        self.bunuot_var.set(patient["phcn"][0])
        self.giaotiep_var.set(patient["phcn"][1])
        self.hohap_var.set(patient["phcn"][2])
        self.vandong_var.set(patient["phcn"][3])

    def to_patient(self) -> Patient:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "ky_xetnghiem": self.xn_var.get(),
            "ky_todieutri": self.tdt_var.get(),
            "ky_3tra": {
                "bacsi": (
                    self.bs_0_var.get(),
                    self.bs_1_var.get(),
                    self.bs_2_var.get(),
                    self.bs_3_var.get(),
                    self.bs_4_var.get(),
                ),
                "dieuduong": (
                    self.dd_0_var.get(),
                    self.dd_1_var.get(),
                    self.dd_2_var.get(),
                    self.dd_3_var.get(),
                    self.dd_4_var.get(),
                ),
            },
            "phcn": (
                self.bunuot_var.get(),
                self.giaotiep_var.get(),
                self.hohap_var.get(),
                self.vandong_var.get(),
            ),
        }
