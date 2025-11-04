# studyhall_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import date
from main import Application
from ui.membertab import MemberTab
from ui.basetab import BaseTab, DialogHelper

# ---------------------------------------------------
# THEME + STYLE
# ---------------------------------------------------
def apply_style(root):
    style = ttk.Style(root)
    # Try to load external theme (optional)
    try:
        root.tk.call("source", "azure.tcl")
        style.theme_use("azure")
    except tk.TclError:
        style.theme_use("clam")  # fallback to default built-in theme

    style.configure("TFrame", background="#f9f9f9")
    style.configure("TLabel", background="#f9f9f9", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    style.configure("TEntry", padding=4)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))


# ---------------------------------------------------
# STUDENT TAB
# ---------------------------------------------------
class StudentTab(BaseTab):
    def build_ui(self):
        title = ttk.Label(self.frame, text="🎓 Manage Students", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", pady=6)

        ttk.Button(btn_frame, text="➕ Add Student", command=self.add_student).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="✏️ Edit", command=self.edit_selected).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="🗑 Delete", command=self.delete_selected).pack(side="left", padx=4)

        self.tree = ttk.Treeview(
            self.frame,
            columns=("reg", "name", "age", "gender", "mob"),
            show="headings",
            height=18,
        )
        for col in ("reg", "name", "age", "gender", "mob"):
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def add_student(self):
        data = DialogHelper.open(self.frame, "Add Student", [
            ("name", "Name"), ("age", "Age"), ("gender", "Gender"), ("mob", "Mobile")
        ])
        if not data:
            return
        try:
            res = self.app.make_student(
                data["name"], int(data["age"]), data["gender"], data["mob"]
            )
            if res["ok"]:
                self.main_ui.save_in_background()
                self.refresh()
                messagebox.showinfo("Success", "Student added successfully.")
            else:
                messagebox.showerror("Error", res["error"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        reg = self.tree.item(sel[0], "values")[0]
        student = self.app.students.get(reg)
        if not student:
            return
        updated = DialogHelper.open(
            self.frame, "Edit Student",
            [("name", "Name"), ("age", "Age"), ("gender", "Gender"), ("mob_number", "Mobile")],
            vars(student)
        )
        if updated:
            try:
                student.name = updated["name"]
                student.age = int(updated["age"])
                student.gender = updated["gender"]
                student.mob_number = updated["mob_number"]
                self.main_ui.save_in_background()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        reg = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete student {reg}?"):
            self.app.students.pop(reg, None)
            self.main_ui.save_in_background()
            self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for s in self.app.students.values():
            self.tree.insert("", "end", values=(s.reg_number, s.name, s.age, s.gender, s.mob_number))


# ---------------------------------------------------
# PLAN TAB
# ---------------------------------------------------
class PlanTab(BaseTab):
    def build_ui(self):
        ttk.Label(self.frame, text="📋 Manage Plans", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Button(self.frame, text="➕ Add Plan", command=self.add_plan).pack(pady=6)
        self.tree = ttk.Treeview(self.frame, columns=("id", "name", "price", "duration"), show="headings")
        for c in ("id", "name", "price", "duration"):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=140, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def add_plan(self):
        data = DialogHelper.open(self.frame, "Add Plan", [
            ("name", "Plan Name"), ("price", "Price"), ("duration", "Duration (days)")
        ])
        if not data:
            return
        try:
            res = self.app.make_plan(data["name"], float(data["price"]), int(data["duration"]))
            if res["ok"]:
                self.main_ui.save_in_background()
                self.refresh()
            else:
                messagebox.showerror("Error", res["error"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.app.plans.values():
            self.tree.insert("", "end", values=(p.plan_id, p.name, p.price, p.duration_days))


# ---------------------------------------------------
# MEMBER TAB
# ---------------------------------------------------

# ---------------------------------------------------
# MAIN UI CLASS
# ---------------------------------------------------
class StudyHallApp:
    def __init__(self):
        self.app = Application()
        self.app.load_data()

        self.root = tk.Tk()
        self.root.title("Study Hall Management")
        self.root.geometry("1150x720")
        self.root.configure(bg="#f9f9f9")
        apply_style(self.root)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabs
        self.student_tab = StudentTab(self.notebook, self.app, self)
        self.plan_tab = PlanTab(self.notebook, self.app, self)
        self.member_tab = MemberTab(self.notebook, self.app, self)

        self.notebook.add(self.student_tab.frame, text="🎓 Students")
        self.notebook.add(self.plan_tab.frame, text="📋 Plans")
        self.notebook.add(self.member_tab.frame, text="🧍 Members")

        self.refresh_all()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    # -------------------------------------------
    # Optimized threaded save
    # -------------------------------------------
    def save_in_background(self):
        def save_job():
            try:
                self.app.save_data()
            except Exception as e:
                print("Save error:", e)
        threading.Thread(target=save_job, daemon=True).start()

    def refresh_all(self):
        self.student_tab.refresh()
        self.plan_tab.refresh()
        self.member_tab.refresh()

    def on_close(self):
        self.app.save_data()
        self.root.destroy()


if __name__ == "__main__":
    StudyHallApp()
