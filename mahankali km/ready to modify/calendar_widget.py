from customtkinter import *
from datetime import datetime
import calendar


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

        # Buttons
        CTkButton(header, text="<<", width=40, corner_radius=12,
                  command=self.prev_10_years).pack(side="left", padx=3)

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

        # Year dropdown
        # Show only 40 years (current -30 to +10)
        years = [str(y) for y in range(self.year - 30, self.year + 11)]

        self.year_var = StringVar(value=str(self.year))
        year_cb = CTkComboBox(
            header,
            values=years,
            variable=self.year_var,
            width=80,
            corner_radius=10,
            command=self.year_changed
        )
        year_cb.pack(side="left", padx=7)

        CTkButton(header, text=">", width=40, corner_radius=12,
                  command=self.next_month).pack(side="left", padx=3)

        CTkButton(header, text=">>", width=40, corner_radius=12,
                  command=self.next_10_years).pack(side="left", padx=3)

        # ---------------- DAY GRID ----------------
        grid_frame = CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10)

        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        # Day name row
        for col, d in enumerate(days):
            CTkLabel(grid_frame, text=d, width=40).grid(row=0, column=col, pady=4)

        month_days = calendar.monthcalendar(int(self.year), int(self.month))

        # Date buttons
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

    def prev_10_years(self):
        self.year -= 10
        self.year_var.set(str(self.year))
        self.build()

    def next_10_years(self):
        self.year += 10
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
