from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkScrollbar
import tkinter as tk
import appimfo
from calendar_widget import CTkCalendar
from tableeditor import CTkEditableTreeview

from add_student import InputField
from be import Students, test, newstudent
test()


def newid():
    # Generate a new ID by incrementing the highest existing student ID
    if not Students:
        return "1"
    try:
        ids = [int(stdd.getimfo()[0]) for stdd in Students]
        return str(max(ids) + 1)
    except Exception:
        return str(len(Students) + 1)

class StartApp(CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{appimfo.name} {appimfo.version}")
        self.geometry("900x600+222+222")
        self.configure(bg="#f5f5f5")
        self.menubar()
        self.content_area()
        self.setlist()
        self.binds()
    def binds(self):
        self.bind("<Escape>", lambda e: self.setlist())
        self.bind("<F1>", lambda e: self.add_student_ui())



        


    def content_area(self):
        self.content = CTkFrame(self, fg_color="#ffffff")
        self.content.pack(side="right", fill="both", expand=True)



    def clear(self, master):
        for w in master.winfo_children():
            w.destroy()

    def setlist(self):
        self.clear(self.content)
        self.table()

    def table(self):
        # ---- SEARCH BAR ----
        search_frame = CTkFrame(self.content, fg_color="#ffffff")
        search_frame.pack(pady=5)

        CTkLabel(search_frame, text="Search:", font=("serif", 14)).pack(side="left", padx=5)
        self.search_entry = CTkEntry(search_frame, width=200, font=("serif", 14))
        self.search_entry.pack(side="left", padx=5)

        CTkButton(
            search_frame, text="Go", width=60,
            fg_color="#80e87a", text_color="black",
            command=self.search_student
        ).pack(side="left", padx=5)

        CTkButton(
            search_frame, text="Reset", width=60,
            fg_color="#ffb347", text_color="black",
            command=self.setlist
        ).pack(side="left", padx=5)

        CTkLabel(self.content, text="Student List", font=("serif", 20, "bold"), fg_color="#ffffff").pack(pady=10)

        # ---- TREE FRAME ----
        tree_frame = CTkFrame(self.content, fg_color="#ffffff")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- EDITABLE TREE ----
        self.tree = CTkEditableTreeview(
            tree_frame,
            editable_columns=["name", "gender", "age", "address"],
            columns=("id", "name", "gender", "age", "address"),
            show="headings",
            on_cell_edit=self.on_cell_edit
        )




        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("age", text="Age")
        self.tree.heading("address", text="Address")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=120)
        self.tree.column("gender", width=80)
        self.tree.column("age", width=50, anchor="center")
        self.tree.column("address", width=180)

        # Scrollbar
        scroll = CTkScrollbar(tree_frame, orientation="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(expand=True, fill="both")

        # Fill data
        self.fill_table()

    
    def on_cell_edit(self, row_id, column, new_value):
        # extract real Student ID from row values
        item = self.tree.item(row_id)
        sid = item["values"][0]   # first column is ID

        # Find in database
        for stdd in Students:
            if str(stdd.id) == str(sid):

                # apply update
                if column == "name":
                    stdd.name = new_value

                elif column == "gender":
                    stdd.gender = new_value

                elif column == "age":
                    stdd.age = int(new_value)

                elif column == "address":
                    stdd.adress = new_value

                # Update into database
                stdd.update()       # <-- YOU MUST HAVE update() in model

                print(f"Updated Student {sid}: {column} -> {new_value}")
                break



    def fill_table(self):
        self.tree.delete(*self.tree.get_children())
        for stdd in Students:
            row = stdd.getimfo()[:5]
            self.tree.insert("", "end", values=row)

    
    def update_student(self, row_id, column, new_value, old_value):
        # Fetch row values
        values = self.tree.item(row_id, "values")
        sid = values[0]  # ID is always first column

        # Find the student object
        target = None
        for st in Students:
            if str(st.getimfo()[0]) == str(sid):
                target = st
                break

        if not target:
            return

        # Update the correct field
        if column == "name":
            target.name = new_value

        elif column == "gender":
            target.gender = new_value

        elif column == "address":
            target.adress = new_value  # your model uses "adress"

        elif column == "age":
            try:
                target.age = int(new_value)
            except:
                target.age = 0

        print("UPDATED:", target.getimfo())



    def search_student(self):
        query = self.search_entry.get().lower().strip()
        if not query:
            return self.setlist()

        self.tree.delete(*self.tree.get_children())

        for stdd in Students:
            data = stdd.getimfo()
            row_id, name, gender, age, address = data[:5]  # <--- use first 5 only

            # Convert all to string for simple matching
            if (
                query in str(row_id).lower()
                or query in name.lower()
                or query in gender.lower()
                or query in str(age).lower()
                or query in address.lower()
            ):
                self.tree.insert("", "end", values=data[:5])


    def add_student_ui(self):
        self.clear(self.content)

        CTkLabel(
            self.content, text="Add New Student",
            font=("serif", 20, "bold"),
            fg_color="#ffffff"
        ).pack(pady=10)

        form = CTkFrame(self.content, fg_color="#f0f0f0")
        form.pack(pady=20, padx=30)

        # Full Name
        self.name_field = InputField(form, "Full Name:")
        self.name_field.grid(row=0, column=0, pady=5, padx=5)

        # Gender
        self.gender_field = InputField(form, "Gender:", entry_width=120)
        self.gender_field.grid(row=1, column=0, pady=5, padx=5)

        # Birthday (disabled entry)
        self.bday_field = InputField(form, "Birthday:", entry_width=150)
        self.bday_field.entry.configure(state="disabled")
        self.bday_field.grid(row=2, column=0, pady=5, padx=5)

        # Age (auto-calculated)
        self.age_field = InputField(form, "Age:", entry_width=80)
        self.age_field.grid(row=2, column=1, pady=5, padx=5)

        # Permanent Calendar Frame (CREATE FIRST)
        self.calendar_frame = CTkFrame(form, fg_color="#e8e8e8")
        self.calendar_frame.grid(row=3, column=0, pady=5, padx=5, sticky="w")

        # Load calendar AFTER frame exists ✔
        self.calendar_widget = CTkCalendar(
            master=self.calendar_frame,
            on_select=self.set_bday
        )
        self.calendar_widget.pack()



        # Address
        self.addr_field = InputField(form, "Address:", entry_width=220)
        self.addr_field.grid(row=4, column=0, pady=5, padx=5)

        # Buttons
        btn_frame = CTkFrame(self.content, fg_color="#ffffff")
        btn_frame.pack(pady=20)

        CTkButton(
            btn_frame, text="Save Student", fg_color="#79e65b", text_color="black",
            font=("serif", 14, "bold"), width=120, command=self.save_student
        ).pack(side="left", padx=10)

        CTkButton(
            btn_frame, text="Clear", fg_color="#ffb347", text_color="black",
            font=("serif", 14, "bold"), width=80,
            command=lambda: self.clear(form)
        ).pack(side="left", padx=10)

        self.name_field.entry.focus()


    def set_bday(self, date):
        self.bday_field.entry.configure(state="normal")
        self.bday_field.entry.delete(0, "end")
        self.bday_field.entry.insert(0, date)
        self.bday_field.entry.configure(state="disabled")
        self.calculate_age_from_bday()




    def save_student(self):
        name = self.name_field.get()
        gender = self.gender_field.get()
        bday = self.bday_field.get()
        age = int(self.age_field.get())   # AGE MUST BE INT
        addr = self.addr_field.get()
        sid = newid()

        from datetime import date
        joindate = date.today().strftime("%d/%m/%Y")

        newstudent(
            id=sid,
            name=name,
            adress=addr,
            gender=gender,
            bday=bday,
            age=age,
            joindate=joindate
        )

        self.setlist()


    def calculate_age_from_bday(self, event=None):
        bday = self.bday_field.get().strip()

        # Expect format DD/MM/YYYY
        if len(bday) != 10 or bday[2] != "/" or bday[5] != "/":
            self.age_field.set("")   # Clear age if invalid
            return

        try:
            day, month, year = map(int, bday.split("/"))

            from datetime import date
            today = date.today()

            # Basic validity check
            dob = date(year, month, day)

            # Calculate age
            age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day)
            )

            # Set the age
            if age >= 0:
                self.age_field.set(str(age))
            else:
                self.age_field.set("")

        except Exception:
            # Invalid date → clear the age box
            self.age_field.set("")




    def menubar(self):
        # Create menu bar
        menubar = tk.Menu(self)

        # ---------------- FILE MENU ----------------
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Sync")
        file_menu.add_command(label="Backup")
        menubar.add_cascade(label="File", menu=file_menu)

        # ---------------- ACTIONS MENU ----------------
        actions_menu = tk.Menu(menubar, tearoff=0)
        actions_menu.add_command(label="Register Student", command=self.add_student_ui)
        actions_menu.add_command(label="List Students", command=self.setlist)
        menubar.add_cascade(label="Actions", menu=actions_menu)

        # ---------------- SETTINGS MENU ----------------
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="General Settings")
        settings_menu.add_command(label="Theme")
        settings_menu.add_separator()
        settings_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Attach to window
        self.config(menu=menubar)




if __name__ == "__main__":
    app = StartApp()
    app.mainloop()

