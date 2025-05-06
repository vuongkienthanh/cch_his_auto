import tkinter as tk
from typing import cast

from .config import Patient

from cch_his_auto.common_ui.scrollable_frame import ScrollFrame


class PatientFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        header = tk.Frame(self)
        columnconfigure(header)
        header.grid(row=0, column=0, sticky="WE", padx=(0, 15))

        for i, h in enumerate(
            ["url", "XN", "CT", "MRI", "BBHC", "tờ ĐT", "Vị trí ký 3tra", "Xóa"]
        ):
            w = tk.Label(header, text=h, relief="raised", anchor="center")
            w.grid(row=0, column=i, sticky="NSEW")

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
        return [cast(Line, p).get_patient() for p in self.viewPort.grid_slaves()[::-1]]

    def clear(self):
        for w in self.viewPort.grid_slaves():
            w.destroy()


class Line(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        columnconfigure(self)
        self.url_var = tk.StringVar()
        self.note_var = tk.StringVar()

        info_frame = tk.Frame(self)
        info_frame.grid(row=0, column=0, sticky="WE")
        info_frame.columnconfigure(1, weight=1)
        tk.Entry(info_frame, textvariable=self.url_var).grid(
            row=0, column=0, sticky="WE", columnspan=2
        )
        tk.Label(info_frame, text="note").grid(row=1, column=0)
        tk.Entry(info_frame, textvariable=self.note_var).grid(
            row=1, column=1, sticky="WE"
        )

        self.xn_var = tk.BooleanVar()
        self.ct_var = tk.BooleanVar()
        self.mri_var = tk.BooleanVar()
        self.bbhc_var = tk.BooleanVar()
        self.tdt_var = tk.BooleanVar()

        for i, v in enumerate(
            [self.xn_var, self.ct_var, self.mri_var, self.bbhc_var, self.tdt_var], 1
        ):
            tk.Checkbutton(self, variable=v).grid(row=0, column=i)

        self.tdt_var.set(True)

        k3t = tk.Frame(self, borderwidth=10)
        k3t.grid(row=0, column=6)
        self.k3t_bs = Ky3Tra(k3t, text="Bác sĩ")
        self.k3t_dd = Ky3Tra(k3t, text="Điều dưỡng")
        self.k3t_bn = Ky3Tra(k3t, text="Bệnh nhân")
        self.k3t_bs.grid(row=0, column=0)
        self.k3t_dd.grid(row=1, column=0)
        self.k3t_bn.grid(row=2, column=0)

        del_btn = tk.Button(self, text="Xóa", command=self.destroy)
        del_btn.grid(row=0, column=7)

    def set_patient(self, patient: Patient):
        self.url_var.set(patient["url"])
        self.note_var.set(patient["note"])
        self.xn_var.set(patient["ky_xn"])
        self.ct_var.set(patient["ky_ct"])
        self.mri_var.set(patient["ky_mri"])
        self.bbhc_var.set(patient["ky_bbhc"])
        self.tdt_var.set(patient["ky_todieutri"])
        self.k3t_bs.set_vitri(patient["ky_3tra"]["bacsi"])
        self.k3t_dd.set_vitri(patient["ky_3tra"]["dieuduong"])
        self.k3t_bn.set_vitri(patient["ky_3tra"]["benhnhan"])

    def get_patient(self) -> Patient:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "ky_xn": self.xn_var.get(),
            "ky_ct": self.ct_var.get(),
            "ky_mri": self.mri_var.get(),
            "ky_bbhc": self.bbhc_var.get(),
            "ky_todieutri": self.tdt_var.get(),
            "ky_3tra": {
                "bacsi": self.k3t_bs.get_vitri(),
                "dieuduong": self.k3t_dd.get_vitri(),
                "benhnhan": self.k3t_bn.get_vitri(),
            },
        }


class Ky3Tra(tk.LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)
        self.v0 = tk.BooleanVar()
        self.v1 = tk.BooleanVar()
        self.v2 = tk.BooleanVar()
        self.v3 = tk.BooleanVar()
        self.v4 = tk.BooleanVar()
        for i, v in enumerate([self.v0, self.v1, self.v2, self.v3, self.v4]):
            tk.Checkbutton(self, variable=v).grid(row=0, column=i)

    def get_vitri(self) -> tuple[bool, bool, bool, bool, bool]:
        return (
            self.v0.get(),
            self.v1.get(),
            self.v2.get(),
            self.v3.get(),
            self.v4.get(),
        )

    def set_vitri(self, v: tuple[bool, bool, bool, bool, bool]):
        self.v0.set(v[0])
        self.v1.set(v[1])
        self.v2.set(v[2])
        self.v3.set(v[3])
        self.v4.set(v[4])


def columnconfigure(w: tk.Widget):
    w.columnconfigure(0, weight=1, minsize=200)
    w.columnconfigure(1, minsize=80)
    w.columnconfigure(2, minsize=80)
    w.columnconfigure(3, minsize=80)
    w.columnconfigure(4, minsize=80)
    w.columnconfigure(5, minsize=80)
    w.columnconfigure(6, minsize=180)
    w.columnconfigure(7, minsize=80)
