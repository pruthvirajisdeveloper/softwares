import tkinter as tk
from tkinter import ttk

class DialogHelper:
    @staticmethod
    def open(root, title, fields, initial=None):
        dlg = tk.Toplevel(root)
        dlg.title(title)
        dlg.geometry("350x300")
        dlg.transient(root)
        dlg.grab_set()

        widgets = {}
        initial = initial or {}

        for i, (key, label) in enumerate(fields):
            ttk.Label(dlg, text=label).grid(row=i, column=0, padx=10, pady=6, sticky="e")
            ent = ttk.Entry(dlg)
            ent.insert(0, str(initial.get(key, "")))
            ent.grid(row=i, column=1, padx=10, pady=6, sticky="we")
            widgets[key] = ent

        result = {}

        def on_ok():
            for k, w in widgets.items():
                result[k] = w.get().strip()
            dlg.destroy()

        def on_cancel():
            dlg.destroy()

        ttk.Button(dlg, text="OK", command=on_ok).grid(row=len(fields), column=0, pady=12)
        ttk.Button(dlg, text="Cancel", command=on_cancel).grid(row=len(fields), column=1, pady=12)
        dlg.columnconfigure(1, weight=1)
        root.wait_window(dlg)
        return result if result else None

class BaseTab:
    def __init__(self, parent, app, main_ui):
        self.app = app
        self.main_ui = main_ui
        self.frame = ttk.Frame(parent)
        self.tree = None
        self.build_ui()

    def build_ui(self):
        raise NotImplementedError

    def refresh(self):
        pass
