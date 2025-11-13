from be import Student, Students, test
from tkinter import *
import appimfo
from tkinter import ttk
test()

class startapp(Tk):
    def __init__(self):
        super().__init__()
        self.title(f'{appimfo.name} {appimfo.version}')
        self.geometry('500x300')
    def MakeSlider(self):
        self.slider=Frame(self, width=100, height=300, bg='#edc37b')
        self.slider.pack(side=LEFT, expand=False, fill=Y)
    def ContentArea(self):
        self.Content=Frame(self, bg="#c5ed7b")
        self.Content.pack(side=RIGHT, fill=BOTH, expand=1)
    def PackButtons(self):
        self.btn1=Button(self.slider, text='List', command= lambda:self.setlist(), width=13)
        self.btn1.pack(fill=X)
    def setlist(self):
        for w in self.Content.winfo_children():
            w.destroy()
        self.table()
    def table(self):
        self.tree=ttk.Treeview(self.Content, columns=("id", "name", "gender", "age", "address"), show="headings")
        self.config(bg="#dced7b")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("age", text="Age")
        self.tree.heading("address", text="Address")
        self.tree.column("id", width=50, anchor='center')
        self.tree.column("name", width=100)
        self.tree.column("gender", width=80)
        self.tree.column("age", width=50, anchor='center')
        self.tree.column("address", width=120)
        scroll = ttk.Scrollbar(self.Content, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(expand=True, fill="both")
        self.FT()
    def FT(self):
        for stdd in Students:
            self.tree.insert("", END, values=stdd.getimfo())

