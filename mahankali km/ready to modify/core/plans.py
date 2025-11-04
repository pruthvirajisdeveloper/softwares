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