from datetime import date, timedelta
import json

# 🧩 Student Class
class Student:
    def __init__(self, name, age, gender, reg_number, mob_number):
        self.name = name
        self.age = age
        self.gender = gender
        self.reg_number = reg_number
        self.mob_number = mob_number

    def get_details(self):
        print(
            f"\n{self.name} : {self.gender}, {self.age} years old"
            f"\nReg. number: {self.reg_number}"
            f"\nMobile number: {self.mob_number}"
        )

    def edit_info(self, name=None, age=None, gender=None, mob_number=None):
        if name:
            self.name = name
        if age:
            self.age = age
        if gender:
            self.gender = gender
        if mob_number:
            self.mob_number = mob_number
        print(f"Student {self.reg_number} updated successfully.")

    def __str__(self):
        return f"[{self.reg_number}]: {self.name} ({self.gender}, {self.age})"


# 🧩 Plan Class (with shift support)
class Plan:
    def __init__(self, plan_id, name, duration_days, price, shift="day"):
        self.plan_id = plan_id
        self.name = name
        self.duration_days = duration_days
        self.price = price
        self.shift = shift.lower()

    def show_info(self):
        print(f"\n  Plan Info:"
              f"\n  ID: {self.plan_id}"
              f"\n  Name: {self.name}"
              f"\n  Duration: {self.duration_days} days"
              f"\n  Price: ₹{self.price}"
              f"\n  Shift: {self.shift.capitalize()}")

    def edit_plan(self, name=None, duration_days=None, price=None, shift=None):
        if name:
            self.name = name
        if duration_days:
            self.duration_days = duration_days
        if price:
            self.price = price
        if shift:
            self.shift = shift.lower()
        print(f"Plan {self.plan_id} updated successfully.")

    def __str__(self):
        return f"[{self.plan_id}] {self.name} - ₹{self.price} ({self.duration_days} days, {self.shift})"


# 🧩 Member Class (with status tracking)
class Member:
    def __init__(self, member_id, student, plan, seat_number, start_date, end_date, paid=False):
        self.member_id = member_id
        self.student = student
        self.plan = plan
        self.seat_number = seat_number
        self.start_date = start_date
        self.end_date = end_date
        self.paid = paid
        self.status = "active"

    def show_info(self):
        print(f"\n🪑 Member Info:"
              f"\n  Member ID: {self.member_id}"
              f"\n  Student: {self.student.name} ({self.student.reg_number})"
              f"\n  Plan: {self.plan.name}"
              f"\n  Seat Number: {self.seat_number}"
              f"\n  Start Date: {self.start_date}"
              f"\n  End Date: {self.end_date}"
              f"\n  Shift: {self.plan.shift.capitalize()}"
              f"\n  Paid: {'✅ Yes' if self.paid else '❌ No'}"
              f"\n  Status: {self.status.upper()}")

    def mark_paid(self):
        self.paid = True
        print(f"💰 Member {self.member_id} marked as paid.")

    def is_expired(self, current_date):
        return current_date > self.end_date

    def mark_expired(self):
        self.status = "expired"

    def __str__(self):
        return f"[{self.member_id}] {self.student.name} - {self.plan.name} ({self.start_date} → {self.end_date}) [{self.plan.shift}]"


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
                student = self.students.get(m["student"]["reg_number"])
                plan = self.plans.get(m["plan"]["plan_id"])
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
            self.check_expired_members()

            print("📂 Data loaded successfully.")

        except FileNotFoundError:
            print("⚠️ No saved data found, starting fresh.")



    def list_seat_status(self):
        """Show which seats are occupied or free."""
        print("\n🪑 Seat Status:")
        occupied = [m.seat_number for m in self.members.values() if m.status == "active"]
        for i in range(1, 21):  # example: seats A1–A20
            seat = f"A{i}"
            if seat in occupied:
                print(f"  {seat}: ❌ Occupied")
            else:
                print(f"  {seat}: ✅ Available")


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
        return {"status": "success", "message": f"Student {name} added.", "reg_number": reg_number}


    def edit_student(self, reg_number, **kwargs):
        student = self.students.get(reg_number)
        if not student:
            print("❌ Student not found.")
            return
        student.edit_info(**kwargs)

    def make_plan(self, name, duration_days, price, shift="day"):
        self.plan_counter += 1
        plan_id = str(self.plan_counter)
        plan = Plan(plan_id, name, duration_days, price, shift)
        self.plans[plan_id] = plan
        print(f"🗓️ Plan '{name}' added with ID {plan_id}")

    def new_member(self, reg_number, plan_id, seat_number):
        student = self.students.get(reg_number)
        plan = self.plans.get(plan_id)
        if not student or not plan:
            print("❌ Invalid student or plan.")
            return

        if not self.is_seat_available(seat_number):
            print(f"❌ Seat {seat_number} is currently occupied.")
            return

        self.member_counter += 1
        member_id = str(self.member_counter)
        start_date = date.today()
        end_date = start_date + timedelta(days=plan.duration_days)
        member = Member(member_id, student, plan, seat_number, start_date, end_date)
        self.members[member_id] = member
        print(f"✅ Member {member_id} created for {student.name} ({plan.name}) - Seat {seat_number}")


    def renew_member(self, member_id):
        member = self.members.get(member_id)
        if not member:
            print("❌ Member not found.")
            return
        member.start_date = date.today()
        member.end_date = member.start_date + timedelta(days=member.plan.duration_days)
        member.paid = False
        member.status = "active"
        print(f"🔁 Member {member_id} renewed successfully.")

    def check_expired_members(self):
        today = date.today()
        for member in self.members.values():
            if member.is_expired(today):
                if member.status != "expired":
                    member.mark_expired()
                    print(f"⚠️ Member {member.member_id} ({member.student.name}) expired on {member.end_date}.")

    def get_members_by_shift(self, shift_type):
        print(f"\n📋 Members in {shift_type.upper()} shift:")
        for m in self.members.values():
            if m.plan.shift.lower() == shift_type.lower():
                print(f"  {m.student.name} - Seat {m.seat_number} - {m.plan.name} ({m.status})")

    def get_members_by_date(self, from_date, to_date):
        print(f"\n📆 Members active between {from_date} and {to_date}:")
        for m in self.members.values():
            if m.start_date <= to_date and m.end_date >= from_date:
                print(f"  {m.student.name} - {m.start_date} → {m.end_date} ({m.plan.shift}, {m.status})")

    def get_info(self):
        print("\n👥 Students:")
        for s in self.students.values():
            print(" ", s)

        print("\n📦 Plans:")
        for p in self.plans.values():
            print(" ", p)

        print("\n🪑 Members:")
        for m in self.members.values():
            print(" ", m)
    def save_data(self, filename="library_data.json"):
        data = {
            "students": {k: vars(v) for k, v in self.students.items()},
            "plans": {k: vars(v) for k, v in self.plans.items()},
            "members": {k: vars(v) for k, v in self.members.items()},
            }
        with open(filename, "w") as f:
            json.dump(data, f, default=str, indent=4)
        print("💾 Data saved successfully.")


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

