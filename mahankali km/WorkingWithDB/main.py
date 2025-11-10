from db import Bridge
from tables import create_all_tables
from core.planmanager import PlanManager
from core.seatmanager import SeatManager
from core.studentmanager import StudentManager
def init():
    Bridge.init_pool()
    create_all_tables()   # ✅ must run before inserts

    students = StudentManager()
    plans = PlanManager()
    seats = SeatManager()

    students.add("John Doe", "Earth", "M", "2001-01-01", "REG001")
    plans.add("Monthly", "Morning", 30, 999.0)
    seats.add_day("A1", "available")
    seats.add_night("B1", "available")

    print("\n[Students]", students.list())
    print("[Plans]", plans.list())
    print("[Seats Day]", seats.list_day())
    print("[Seats Night]", seats.list_night())

    Bridge.close_pool()

init()
