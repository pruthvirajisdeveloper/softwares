import tkinter as tk
from tkinter import ttk, messagebox
from main import Application, Student, Plan
import json

app = Application()
app.load_data()

root = tk.Tk()
root.title("Study Hall Management")
root.geometry("850x600")
root.configure(bg="#f4f4f4")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# --------------------------------------------------------------------
# STUDENTS TAB
# --------------------------------------------------------------------
students_frame = ttk.Frame(notebook)
notebook.add(students_frame, text="🎓 Students")

# --- Add Student Section ---
add_student_frame = ttk.LabelFrame(students_frame, text="Add Student")
add_student_frame.pack(fill="x", padx=10, pady=10)

tk.Label(add_student_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(add_student_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_student_frame, text="Age:").grid(row=0, column=2, padx=5, pady=5)
age_entry = ttk.Entry(add_student_frame)
age_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(add_student_frame, text="Gender:").grid(row=1, column=0, padx=5, pady=5)
gender_var = tk.StringVar()
gender_combo = ttk.Combobox(add_student_frame, textvariable=gender_var, values=["Male", "Female"], state="readonly")
gender_combo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(add_student_frame, text="Mobile:").grid(row=1, column=2, padx=5, pady=5)
mob_entry = ttk.Entry(add_student_frame)
mob_entry.grid(row=1, column=3, padx=5, pady=5)


def add_student():
    name, age, gender, mob = name_entry.get(), age_entry.get(), gender_var.get(), mob_entry.get()
    if not all([name, age, gender, mob]):
        messagebox.showerror("Error", "All fields are required.")
        return

    result = app.make_student(name, int(age), gender, mob)
    if result["ok"]:
        messagebox.showinfo("Success", f"Added {name} (Reg: {result['data'].reg_number})")
        refresh_students()
    else:
        messagebox.showerror("Error", result["error"])


ttk.Button(add_student_frame, text="➕ Add Student", command=add_student).grid(row=2, column=0, columnspan=4, pady=10)

# --- Student List ---
student_tree = ttk.Treeview(students_frame, columns=("Reg", "Name", "Gender", "Age", "Mobile"), show="headings")
student_tree.heading("Reg", text="Reg No.")
student_tree.heading("Name", text="Name")
student_tree.heading("Gender", text="Gender")
student_tree.heading("Age", text="Age")
student_tree.heading("Mobile", text="Mobile")
student_tree.pack(expand=True, fill="both", padx=10, pady=5)


def refresh_students():
    for row in student_tree.get_children():
        student_tree.delete(row)
    for s in app.students.values():
        student_tree.insert("", "end", values=(s.reg_number, s.name, s.gender, s.age, s.mob_number))


# --- Context Menus ---
student_menu = tk.Menu(root, tearoff=0)
student_menu.add_command(label="Edit Cell", command=lambda: None)  # Placeholder for edit functionality
student_menu.add_separator()
student_menu.add_command(label="Refresh Table", command=lambda: refresh_all())

other_menu = tk.Menu(root, tearoff=0)
other_menu.add_command(label="Edit Cell", command=lambda: None)  # Placeholder for edit functionality
other_menu.add_command(label="Delete Row", command=lambda: None)  # Placeholder for delete functionality
other_menu.add_separator()
other_menu.add_command(label="Refresh Table", command=lambda: refresh_all())

# Context menu handler

def right_click(event):
    tree = event.widget
    parent = tree.master
    if tree.identify_row(event.y):
        tree.selection_set(tree.identify_row(event.y))
        if parent == students_frame:
            student_menu.post(event.x_root, event.y_root)
        else:
            other_menu.post(event.x_root, event.y_root)

student_tree.bind("<Button-3>", right_click)

# --------------------------------------------------------------------
# PLANS TAB
# --------------------------------------------------------------------
plans_frame = ttk.Frame(notebook)

add_plan_frame = ttk.LabelFrame(plans_frame, text="Add Plan")
add_plan_frame.pack(fill="x", padx=10, pady=10)

tk.Label(add_plan_frame, text="Plan Name:").grid(row=0, column=0, padx=5, pady=5)
plan_name_entry = ttk.Entry(add_plan_frame)
plan_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_plan_frame, text="Days:").grid(row=0, column=2, padx=5, pady=5)
plan_days_entry = ttk.Entry(add_plan_frame)
plan_days_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(add_plan_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
plan_price_entry = ttk.Entry(add_plan_frame)
plan_price_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(add_plan_frame, text="Shift:").grid(row=1, column=2, padx=5, pady=5)
plan_shift_combo = ttk.Combobox(add_plan_frame, values=["Day", "Night", "Full Day"], state="readonly")
plan_shift_combo.grid(row=1, column=3, padx=5, pady=5)


def add_plan():
    name, days, price, shift = plan_name_entry.get(), plan_days_entry.get(), plan_price_entry.get(), plan_shift_combo.get()
    if not all([name, days, price, shift]):
        messagebox.showerror("Error", "All fields required.")
        return

    result = app.make_plan(name, int(days), float(price), shift)
    if result["ok"]:
        messagebox.showinfo("Success", f"Added plan: {result['data'].name}")
        refresh_plans()
    else:
        messagebox.showerror("Error", result["error"])


ttk.Button(add_plan_frame, text="➕ Add Plan", command=add_plan).grid(row=2, column=0, columnspan=4, pady=10)

plan_tree = ttk.Treeview(plans_frame, columns=("ID", "Name", "Days", "Price", "Shift"), show="headings")
for col in ("ID", "Name", "Days", "Price", "Shift"):
    plan_tree.heading(col, text=col)
plan_tree.pack(expand=True, fill="both", padx=10, pady=5)


def refresh_plans():
    for row in plan_tree.get_children():
        plan_tree.delete(row)
    for p in app.plans.values():
        plan_tree.insert("", "end", values=(p.plan_id, p.name, p.duration_days, p.price, p.shift))


plan_tree.bind("<Button-3>", right_click)

# --------------------------------------------------------------------
# MEMBERS TAB
# --------------------------------------------------------------------
members_frame = ttk.Frame(notebook)
notebook.add(members_frame, text="🪑 Members")

add_member_frame = ttk.LabelFrame(members_frame, text="Add Member")
add_member_frame.pack(fill="x", padx=10, pady=10)

student_map = {}  # name -> reg number


def refresh_student_combo():
    student_combo["values"] = [f"{s.name} ({s.reg_number})" for s in app.students.values()]
    student_map.clear()
    for s in app.students.values():
        student_map[s.name] = s.reg_number


def refresh_plan_combo():
    plan_combo["values"] = [f"{p.plan_id} - {p.name} ({p.shift})" for p in app.plans.values()]


def on_student_name_selected(event):
    name_text = student_combo.get().split(" (")[0]
    reg_number = student_map.get(name_text)
    if reg_number:
        student_reg_entry.delete(0, tk.END)
        student_reg_entry.insert(0, reg_number)


def on_student_reg_change(*args):
    reg_text = student_reg_var.get().strip()
    if not reg_text:
        return
    for name, reg in student_map.items():
        if reg == reg_text:
            student_combo.set(f"{name} ({reg})")
            break


ttk.Label(add_member_frame, text="Student Name:").grid(row=0, column=0, padx=5, pady=5)
student_combo = ttk.Combobox(add_member_frame, state="readonly", width=30)
student_combo.grid(row=0, column=1, padx=5, pady=5)
student_combo.bind("<<ComboboxSelected>>", on_student_name_selected)

ttk.Label(add_member_frame, text="Reg Number:").grid(row=1, column=0, padx=5, pady=5)
student_reg_var = tk.StringVar()
student_reg_entry = ttk.Entry(add_member_frame, textvariable=student_reg_var)
student_reg_entry.grid(row=1, column=1, padx=5, pady=5)
student_reg_var.trace("w", on_student_reg_change)

ttk.Label(add_member_frame, text="Select Plan:").grid(row=2, column=0, padx=5, pady=5)
plan_combo = ttk.Combobox(add_member_frame, state="readonly", width=30)
plan_combo.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(add_member_frame, text="Seat Number:").grid(row=3, column=0, padx=5, pady=5)
seat_entry = ttk.Entry(add_member_frame)
seat_entry.grid(row=3, column=1, padx=5, pady=5)


def add_member():
    reg = student_reg_entry.get().strip()
    seat = seat_entry.get().strip()
    selected_plan = plan_combo.get()

    if not (reg and seat and selected_plan):
        messagebox.showerror("Error", "All fields required.")
        return

    plan_id = selected_plan.split(" - ")[0]
    result = app.new_member(reg, plan_id, seat)
    if result["ok"]:
        messagebox.showinfo("Success", f"Member added successfully.")
        refresh_members()
    else:
        messagebox.showerror("Error", result["error"])


ttk.Button(add_member_frame, text="➕ Add Member", command=add_member).grid(row=4, column=0, columnspan=2, pady=10)

member_tree = ttk.Treeview(members_frame, columns=("ID", "Name", "Plan", "Seat", "Start", "End", "Status"), show="headings")
for col in ("ID", "Name", "Plan", "Seat", "Start", "End", "Status"):
    member_tree.heading(col, text=col)
member_tree.pack(expand=True, fill="both", padx=10, pady=5)


def refresh_members():
    for row in member_tree.get_children():
        member_tree.delete(row)
    for m in app.members.values():
        member_tree.insert(
            "",
            "end",
            values=(
                m.member_id,
                m.student.name,
                m.plan.name,
                m.seat_number,
                m.start_date,
                m.end_date,
                m.status,
            ),
        )


member_tree.bind("<Button-3>", right_click)


def refresh_all():
    refresh_students()
    refresh_plans()
    refresh_student_combo()
    refresh_plan_combo()
    refresh_members()


refresh_all()
root.mainloop()
