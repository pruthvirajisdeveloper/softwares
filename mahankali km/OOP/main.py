from tkinter import *
class app(Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.label=Label(text='hello!')
    def make_window(self):
        self.label.pack()
        
    def show(self):
        self.make_window()
        self.mainloop()

app().show()