from students.ui import StartApp
from database import init_pool
init_pool()
if __name__ == "__main__":
    app = StartApp()
    
    app.mainloop()