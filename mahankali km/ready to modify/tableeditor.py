# tableeditor.py
import tkinter as tk
from tkinter import ttk

class CTkEditableTreeview(ttk.Treeview):
    def __init__(self, master, editable_columns=None, on_cell_edit=None, **kwargs):
        super().__init__(master, **kwargs)

        self.editable_columns = editable_columns or []
        self.on_cell_edit = on_cell_edit
        self._edit_widget = None

        self.bind("<Double-1>", self._start_edit)

    def _start_edit(self, event):
        region = self.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)

        if not row_id or not col_id:
            return

        col_index = int(col_id.strip("#")) - 1
        col_name = self["columns"][col_index]

        if col_name not in self.editable_columns:
            return

        bbox = self.bbox(row_id, col_id)
        if not bbox:
            return

        x, y, w, h = bbox
        value = self.item(row_id, "values")[col_index]

        # --- Cancel any previous editor ---
        if self._edit_widget:
            self._edit_widget.destroy()

        # --- Gender Dropdown ---
        if col_name == "gender":
            self._edit_widget = ttk.Combobox(
                self,
                values=["Male", "Female", "Other"],
                state="readonly"
            )
            self._edit_widget.place(x=x, y=y, width=w, height=h)
            self._edit_widget.set(value)
            self._edit_widget.bind("<<ComboboxSelected>>",
                                   lambda e: self._finish_edit(row_id, col_index, col_name))

        # --- Numeric-only Age Editor ---
        elif col_name == "age":
            self._edit_widget = tk.Entry(self)
            self._edit_widget.place(x=x, y=y, width=w, height=h)
            self._edit_widget.insert(0, value)
            self._edit_widget.focus()

            # allow only digits
            def only_numbers(char):
                return char.isdigit()

            vcmd = (self.register(only_numbers), "%S")
            self._edit_widget.config(validate="key", validatecommand=vcmd)

            self._edit_widget.bind("<Return>", lambda e: self._finish_edit(row_id, col_index, col_name))
            self._edit_widget.bind("<FocusOut>", lambda e: self._finish_edit(row_id, col_index, col_name))

        # --- Normal text editor for other columns ---
        else:
            self._edit_widget = tk.Entry(self)
            self._edit_widget.place(x=x, y=y, width=w, height=h)
            self._edit_widget.insert(0, value)
            self._edit_widget.focus()
            self._edit_widget.bind("<Return>",
                                   lambda e: self._finish_edit(row_id, col_index, col_name))
            self._edit_widget.bind("<FocusOut>",
                                   lambda e: self._finish_edit(row_id, col_index, col_name))

    def _finish_edit(self, row_id, col_index, col_name):
        if not self._edit_widget:
            return

        new_value = self._edit_widget.get()

        values = list(self.item(row_id, "values"))
        values[col_index] = new_value
        self.item(row_id, values=values)

        # notify main UI
        if self.on_cell_edit:
            self.on_cell_edit(row_id, col_name, new_value)

        self._edit_widget.destroy()
        self._edit_widget = None
