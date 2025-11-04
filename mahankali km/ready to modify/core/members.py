


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

