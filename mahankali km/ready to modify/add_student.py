from customtkinter import CTkFrame, CTkLabel, CTkEntry

class InputField(CTkFrame):
    def __init__(self, master, label_text, entry_width=180):
        super().__init__(master, fg_color="transparent")

        self.label = CTkLabel(self, text=label_text, font=("serif", 14))
        self.label.grid(row=0, column=0, padx=5, pady=3, sticky="w")

        self.entry = CTkEntry(self, width=entry_width, font=("serif", 14))
        self.entry.grid(row=0, column=1, padx=5, pady=3)

    def get(self):
        """Return the value inside the entry."""
        return self.entry.get()

    def set(self, value):
        """Set text inside the entry."""
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
