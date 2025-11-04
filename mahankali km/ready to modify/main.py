from datetime import date, timedelta
import json
from core.plans import Plan
from core.members import Member
from core.students import Student

# 🧩 Student Class

# 🧩 Application Class
class Application:
    def __init__(self):
        self.students = {}
        self.plans = {}
        self.members = {}

        self.student_counter = 0
        self.plan_counter = 0
        self.member_counter = 0

        self.load_default_plans()


    def load_data(self, filename="library_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            # 🧍 Rebuild students
            self.students = {}
            for reg, s in data.get("students", {}).items():
                self.students[reg] = Student(
                    s["name"],
                    s["age"],
                    s["gender"],
                    s["reg_number"],
                    s["mob_number"]
                )

            # 🗓️ Rebuild plans
            self.plans = {}
            for pid, p in data.get("plans", {}).items():
                self.plans[pid] = Plan(
                    p["plan_id"],
                    p["name"],
                    p["duration_days"],
                    p["price"],
                    p["shift"]
                )

            # 🪑 Rebuild members
            self.members = {}
            for mid, m in data.get("members", {}).items():
                student = self.students.get(str(m["student"]))
                plan = self.plans.get(str(m["plan"]))
                if student and plan:
                    member = Member(
                        m["member_id"],
                        student,
                        plan,
                        m["seat_number"],
                        date.fromisoformat(m["start_date"]),
                        date.fromisoformat(m["end_date"]),
                        m["paid"]
                    )
                    member.status = m.get("status", "active")
                    self.members[mid] = member

            # Restore counters
            self.student_counter = len(self.students)
            self.plan_counter = len(self.plans)
            self.member_counter = len(self.members)

            # ✅ Check expired members only after successful load
            self.check_expired_members()

            return {"ok": True, "data": "Data loaded successfully."}

        except (FileNotFoundError, json.JSONDecodeError):
            return {"ok": False, "error": "No valid saved data found, starting fresh."}


    def list_seat_status(self):
        print("\n🪑 Seat Status:")
        occupied = {m.seat_number for m in self.members.values() if m.status == "active"}
        all_seats = [f"A{i}" for i in range(1, 11)] + [f"B{i}" for i in range(1, 11)]  # 20 total
        for seat in all_seats:
            status = "❌ Occupied" if seat in occupied else "✅ Available"
            print(f"  {seat}: {status}")



    def is_seat_available(self, seat_number):
        """Check if the given seat is available (not occupied by an active member)."""
        for member in self.members.values():
            if member.seat_number == seat_number and member.status == "active":
                return False
        return True


    def load_default_plans(self):
        ready_made_plans = [
            ("Monthly-Day", 30, 1200, "day"),
            ("Monthly-Night", 30, 1000, "night"),
            ("Weekly-Day", 7, 400, "day"),
            ("Weekly-Night", 7, 350, "night"),
        ]
        for name, days, price, shift in ready_made_plans:
            self.plan_counter += 1
            plan_id = str(self.plan_counter)
            plan = Plan(plan_id, name, days, price, shift)
            self.plans[plan_id] = plan
        print("✅ Default plans loaded successfully.\n")

    def make_student(self, name, age, gender, mob_number):
        self.student_counter += 1
        reg_number = str(self.student_counter)
        student = Student(name, age, gender, reg_number, mob_number)
        self.students[reg_number] = student
        self.save_data()
        return {"ok": True, "data": vars(student)}


    def edit_student(self, reg_number, **kwargs):
        student = self.students.get(reg_number)
        if not student:
            return {"ok": False, "error": "Student not found."}
        student.edit_info(**kwargs)
        self.save_data()
        return {"ok": True, "data": vars(student)}

    def make_plan(self, name, duration_days, price, shift="day"):
        self.plan_counter += 1
        plan_id = str(self.plan_counter)
        plan = Plan(plan_id, name, duration_days, price, shift)
        self.plans[plan_id] = plan
        self.save_data()
        return {"ok": True, "data": vars(plan)}

    def new_member(self, reg_number, plan_id, seat_number):
        student = self.students.get(reg_number)
        plan = self.plans.get(plan_id)
        if not student or not plan:
            return {"ok": False, "error": "Invalid student or plan."}

        if not self.is_seat_available(seat_number):
            return {"ok": False, "error": f"Seat {seat_number} is currently occupied."}

        self.member_counter += 1
        member_id = str(self.member_counter)
        start_date = date.today()
        end_date = start_date + timedelta(days=plan.duration_days)
        member = Member(member_id, student, plan, seat_number, start_date, end_date)
        self.members[member_id] = member
        self.save_data()
        return {"ok": True, "data": vars(member)}


    def renew_member(self, member_id):
        member = self.members.get(member_id)
        if not member:
            return {"ok": False, "error": "Member not found."}
        member.start_date = date.today()
        member.end_date = member.start_date + timedelta(days=member.plan.duration_days)
        member.paid = False
        member.status = "active"
        self.save_data()
        return {"ok": True, "data": vars(member)}

    def check_expired_members(self):
        today = date.today()
        expired = []
        for member in self.members.values():
            if member.is_expired(today):
                if member.status != "expired":
                    member.mark_expired()
                    expired.append({"member_id": member.member_id, "name": member.student.name, "expired_on": str(member.end_date)})
        if expired:
            self.save_data()
        return {"ok": True, "data": expired}

    def get_members_by_shift(self, shift_type):
        members = [vars(m) for m in self.members.values() if m.plan.shift.lower() == shift_type.lower()]
        return {"ok": True, "data": members}

    def get_members_by_date(self, from_date, to_date):
        members = [vars(m) for m in self.members.values() if m.start_date <= to_date and m.end_date >= from_date]
        return {"ok": True, "data": members}

    def get_info(self):
        return {
            "ok": True,
            "data": {
                "students": [vars(s) for s in self.students.values()],
                "plans": [vars(p) for p in self.plans.values()],
                "members": [vars(m) for m in self.members.values()]
            }
        }

    def get_all_students(self):
        return {"ok": True, "data": [vars(s) for s in self.students.values()]}

    def get_all_members(self):
        members_list = []
        for m in self.members.values():
            members_list.append({
                "member_id": m.member_id,
                "student": {
                    "reg_number": m.student.reg_number,
                    "name": m.student.name,
                    "age": m.student.age,
                    "gender": m.student.gender,
                    "mob_number": m.student.mob_number
                },
                "plan": {
                    "plan_id": m.plan.plan_id,
                    "name": m.plan.name,
                    "duration_days": m.plan.duration_days,
                    "price": m.plan.price,
                    "shift": m.plan.shift
                },
                "seat_number": m.seat_number,
                "start_date": str(m.start_date),
                "end_date": str(m.end_date),
                "status": m.status,
                "paid": m.paid
            })
        return {"ok": True, "data": members_list}

    def get_all_plans(self):
        return {"ok": True, "data": [vars(p) for p in self.plans.values()]}

    def save_data(self, filename="library_data.json"):
        data = {
            "students": {
                reg: {
                    "name": s.name,
                    "age": s.age,
                    "gender": s.gender,
                    "reg_number": s.reg_number,
                    "mob_number": s.mob_number
                }
                for reg, s in self.students.items()
            },
            "plans": {
                pid: {
                    "plan_id": p.plan_id,
                    "name": p.name,
                    "duration_days": p.duration_days,
                    "price": p.price,
                    "shift": p.shift
                }
                for pid, p in self.plans.items()
            },
            "members": {
                mid: {
                    "member_id": m.member_id,
                    "student": str(m.student.reg_number),  # store id only
                    "plan": str(m.plan.plan_id),          # store id only
                    "seat_number": m.seat_number,
                    "start_date": m.start_date.isoformat(),
                    "end_date": m.end_date.isoformat(),
                    "paid": m.paid,
                    "status": m.status
                }
                for mid, m in self.members.items()
            }
        }

        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            return {"ok": True, "data": "Data saved successfully."}
        except Exception as e:
            return {"ok": False, "error": f"Failed to save data: {e}"}


# 🧩 Manager (for future features)
class Manager:
    def __init__(self):
        pass

if __name__ == "__main__":
    app = Application()
    app.load_data()  # try loading old data first

    app.make_student("Amit", 21, "Male", "9998887777")
    app.make_student("Pooja", 19, "Female", "9991112222")

    app.new_member("1", "1", "A1")
    app.new_member("2", "2", "B1")

    app.get_info()
    app.get_members_by_shift("night")

    app.save_data()  # 💾 Save progress

