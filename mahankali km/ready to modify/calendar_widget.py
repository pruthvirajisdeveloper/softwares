from customtkinter import *
from datetime import datetime
import calendar


# ================= SCROLLABLE YEAR DROPDOWN =====================

class ScrollableYearBox(CTkFrame):
    def __init__(self, master, values, variable, width=80, height=28, command=None):
        super().__init__(master, fg_color="transparent")

        self.values = values
        self.variable = variable
        self.command = command
        self.width = width

        self.btn = CTkButton(
            self,
            textvariable=self.variable,
            width=width,
            height=height,
            corner_radius=10,
            command=self.open_dropdown
        )
        self.btn.pack()

        self.dropdown = None

    def open_dropdown(self):
        if self.dropdown:
            self.dropdown.destroy()

        self.dropdown = CTkToplevel(self)
        self.dropdown.overrideredirect(True)
        self.dropdown.geometry(
            f"{self.width}x150+{self.winfo_rootx()}+{self.winfo_rooty() + 32}"
        )

        frame = CTkScrollableFrame(self.dropdown, width=self.width, height=150)
        frame.pack()

        for y in self.values:
            b = CTkButton(
                frame,
                text=y,
                width=self.width - 10,
                height=26,
                command=lambda val=y: self.select(val)
            )
            b.pack(pady=2)

    def select(self, value):
        self.variable.set(value)
        if self.command:
            self.command()
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None


# ======================= CALENDAR CLASS ==========================

class CTkCalendar(CTkFrame):
    def __init__(self, master, on_select, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_select = on_select

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()

        # ---------------- HEADER ----------------
        header = CTkFrame(self, fg_color="transparent")
        header.pack(pady=5)

        CTkButton(header, text="<<", width=40, corner_radius=12,
                  command=self.prev_1_years).pack(side="left", padx=3)

        CTkButton(header, text="<", width=40, corner_radius=12,
                  command=self.prev_month).pack(side="left", padx=3)

        # Month dropdown
        months = list(calendar.month_name)[1:]
        self.month_var = StringVar(value=months[self.month - 1])
        month_cb = CTkComboBox(
            header,
            values=months,
            variable=self.month_var,
            width=130,
            corner_radius=10,
            command=self.month_changed
        )
        month_cb.pack(side="left", padx=7)

        # ---------------- YEAR DROPDOWN (SCROLLABLE) ----------------

        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 40, current_year + 20)]

        self.year_var = StringVar(value=str(self.year))

        year_cb = ScrollableYearBox(
            header,
            values=years,
            variable=self.year_var,
            width=70,
            command=self.year_changed
        )
        year_cb.pack(side="left", padx=7)

        CTkButton(header, text=">", width=40, corner_radius=12,
                  command=self.next_month).pack(side="left", padx=3)

        CTkButton(header, text=">>", width=40, corner_radius=12,
                  command=self.next_1_years).pack(side="left", padx=3)

        # ---------------- DAY GRID ----------------
        grid_frame = CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10)

        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        for col, d in enumerate(days):
            CTkLabel(grid_frame, text=d, width=40).grid(row=0, column=col, pady=4)

        month_days = calendar.monthcalendar(int(self.year), int(self.month))

        for r, week in enumerate(month_days, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    CTkLabel(grid_frame, text="", width=40).grid(row=r, column=c)
                else:
                    btn = CTkButton(
                        grid_frame,
                        text=str(day),
                        width=40,
                        height=30,
                        corner_radius=12,
                        command=lambda d=day: self.select_date(d)
                    )
                    btn.grid(row=r, column=c, padx=2, pady=2)

    # ---------------- LOGIC ----------------

    def month_changed(self, *args):
        months = list(calendar.month_name)[1:]
        self.month = months.index(self.month_var.get()) + 1
        self.build()

    def year_changed(self, *args):
        self.year = int(self.year_var.get())
        self.build()

    def prev_1_years(self):
        self.year -= 1
        self.year_var.set(str(self.year))
        self.build()

    def next_1_years(self):
        self.year += 1
        self.year_var.set(str(self.year))
        self.build()

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.build()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.build()

    def select_date(self, day):
        date = f"{day:02d}/{self.month:02d}/{self.year}"
        self.on_select(date)
