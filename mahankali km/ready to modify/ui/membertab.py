from ui.basetab import BaseTab, DialogHelper
import tkinter as tk
from tkinter import ttk, messagebox
class MemberTab(BaseTab):
    def build_ui(self):
        ttk.Label(self.frame, text="🧍 Manage Members", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Button(self.frame, text="➕ Add Member", command=self.add_member).pack(pady=6)
        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "student", "plan", "start", "end"),
            show="headings"
        )
        for c in ("id", "student", "plan", "start", "end"):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=160, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def add_member(self):
        data = DialogHelper.open(self.frame, "Add Member", [
            ("student_reg", "Student RegNo"),
            ("plan_id", "Plan ID"),
            ("start_date", "Start Date (YYYY-MM-DD)")
        ])
        if not data:
            return
        try:
            res = self.app.new_member(data["student_reg"], data["plan_id"], data["start_date"])
            if res["ok"]:
                self.main_ui.save_in_background()
                self.refresh()
            else:
                messagebox.showerror("Error", res["error"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for m in self.app.members.values():
            self.tree.insert("", "end", values=(
                m.member_id, m.student.reg_number, m.plan.plan_id, m.start_date, m.end_date
            ))

