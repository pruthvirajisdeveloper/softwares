from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkEntry, CTkScrollbar
from tkinter import ttk
import appimfo
from be import Student, Students, test, newstudent
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
        self.make_slider()
        self.content_area()
        self.pack_buttons()
        self.setlist()

    def make_slider(self):
        self.slider = CTkFrame(self, width=120, fg_color="#edc37b")
        self.slider.pack(side="left", fill="y")

    def content_area(self):
        self.content = CTkFrame(self, fg_color="#ffffff")
        self.content.pack(side="right", fill="both", expand=True)

    def pack_buttons(self):
        CTkLabel(self.slider, text="Menu", font=("serif", 18, "bold"), fg_color="#edc37b").pack(pady=20)
        CTkButton(self.slider, text="List Students", command=self.setlist, width=100, height=40).pack(pady=10)
        CTkButton(self.slider, text="Add Student", command=self.add_student_ui, width=100, height=40).pack(pady=10)

    def clear(self, master):
        for w in master.winfo_children():
            w.destroy()

    def setlist(self):
        self.clear(self.content)
        self.table()

    def table(self):
        CTkLabel(self.content, text="Student List", font=("serif", 20, "bold"), fg_color="#ffffff").pack(pady=10)
        tree_frame = CTkFrame(self.content, fg_color="#ffffff")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "name", "gender", "age", "address"),
            show="headings"
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
        scroll = CTkScrollbar(tree_frame, orientation="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(expand=True, fill="both")
        self.fill_table()

    def fill_table(self):
        self.tree.delete(*self.tree.get_children())
        for stdd in Students:
            row = stdd.getimfo()[:5]
            self.tree.insert("", "end", values=row)

    def add_student_ui(self):
        self.clear(self.content)
        CTkLabel(self.content, text="Add New Student", font=("serif", 20, "bold"), fg_color="#ffffff").pack(pady=10)
        form = CTkFrame(self.content, fg_color="#f0f0f0")
        form.pack(pady=20, padx=30)
        # Name
        CTkLabel(form, text="Full Name:", font=("serif", 14)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = CTkEntry(form, width=200, font=("serif", 14))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        # Gender
        CTkLabel(form, text="Gender:", font=("serif", 14)).grid(row=1, column=0, sticky="w", pady=5)
        self.gender_entry = CTkEntry(form, width=120, font=("serif", 14))
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)
        # Birthday
        CTkLabel(form, text="Birthday (DD/MM/YYYY):", font=("serif", 14)).grid(row=2, column=0, sticky="w", pady=5)
        self.bday_entry = CTkEntry(form, width=140, font=("serif", 14))
        self.bday_entry.grid(row=2, column=1, padx=10, pady=5)
        # Age
        CTkLabel(form, text="Age:", font=("serif", 14)).grid(row=3, column=0, sticky="w", pady=5)
        self.age_entry = CTkEntry(form, width=80, font=("serif", 14))
        self.age_entry.grid(row=3, column=1, padx=10, pady=5)
        # Address
        CTkLabel(form, text="Address:", font=("serif", 14)).grid(row=4, column=0, sticky="nw", pady=5)
        self.address_entry = CTkEntry(form, width=200, font=("serif", 14))
        self.address_entry.grid(row=4, column=1, padx=10, pady=5)
        # Buttons
        btn_frame = CTkFrame(self.content, fg_color="#ffffff")
        btn_frame.pack(pady=20)
        CTkButton(
            btn_frame, text="Save Student", fg_color="#79e65b", text_color="black",
            font=("serif", 14, "bold"), width=120, command=self.save_student
        ).pack(side="left", padx=10)
        CTkButton(
            btn_frame, text="Clear", fg_color="#ffb347", text_color="black",
            font=("serif", 14, "bold"), width=80, command=lambda: self.clear(form)
        ).pack(side="left", padx=10)
        self.name_entry.focus()

    def save_student(self):
        name = self.name_entry.get()
        gender = self.gender_entry.get()
        bday = self.bday_entry.get()
        age = self.age_entry.get()
        addr = self.address_entry.get()
        sid = newid()
        newstudent(
            name=name,
            id=sid,
            adress=addr,
            gender=gender,
            bday=bday,
            age=age
        )
        self.setlist()

if __name__ == "__main__":
    app = StartApp()
    app.mainloop()

