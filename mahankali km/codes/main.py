import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar

# Load seat data
with open('seats_data.json', 'r') as f:
    seats = json.load(f)

# Helper to get starting date from end date
# Format: dd-mm-yyyy

def get_starting_date(end_date):
    if not end_date:
        return ''
    try:
        end = datetime.strptime(end_date, '%d-%m-%Y')
        start = end - timedelta(days=30)
        return start.strftime('%d-%m-%Y')
    except Exception:
        return ''

# Update starting date and end date in memory (not saving to file)
def update_dates(seat_index, new_start_date):
    try:
        start = datetime.strptime(new_start_date, '%d-%m-%Y')
        end = start + timedelta(days=30)
        seats[seat_index]['end_date'] = end.strftime('%d-%m-%Y')
    except Exception:
        pass

# GUI
def show_editor():
    root = tk.Tk()
    root.title('Seat Date Editor')
    root.geometry('700x500')

    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%d-%m-%Y')
            return True
        except Exception:
            return False

    warning_label = ttk.Label(root, text='', foreground='red')
    warning_label.grid(row=5, column=0, columnspan=2)

    def highlight_date_error():
        cal_widget.config(background='red', foreground='white')
        warning_label.config(text='Date format is invalid! Please select a valid date using the calendar.')

    def clear_date_error():
        cal_widget.config(background='white', foreground='black')
        warning_label.config(text='')

    # Use a permanent Calendar widget for date selection
    cal_frame = ttk.Frame(root)
    cal_frame.grid(row=2, column=1, padx=10, pady=10)
    cal_widget = Calendar(cal_frame, selectmode='day', date_pattern='dd-mm-yyyy')
    cal_widget.pack(side='left')

    selected_date_label = ttk.Label(cal_frame, text='Selected Date:')
    selected_date_label.pack(side='left', padx=10)

    def update_selected_date_label(date_str):
        selected_date_label.config(text=f'Selected Date: {date_str}')

    def on_seat_select(event):
        idx = seat_combo.current()
        student = seats[idx]
        name_var.set(student['name'])
        if not student['name']:
            cal_widget.config(state='disabled')
            start_var.set('')
            end_var.set('')
            update_selected_date_label('')
            clear_date_error()
        else:
            cal_widget.config(state='normal')
            # If end_date exists, calculate starting date
            if student['end_date']:
                start_date = get_starting_date(student['end_date'])
            else:
                start_date = datetime.today().strftime('%d-%m-%Y')
            start_var.set(start_date)
            try:
                cal_widget.selection_set(datetime.strptime(start_var.get(), '%d-%m-%Y'))
                update_selected_date_label(start_var.get())
                clear_date_error()
            except Exception:
                cal_widget.selection_set(datetime.today())
                update_selected_date_label(datetime.today().strftime('%d-%m-%Y'))
                highlight_date_error()
            try:
                start_dt = datetime.strptime(start_var.get(), '%d-%m-%Y')
                end_dt = start_dt + timedelta(days=30)
                end_var.set(end_dt.strftime('%d-%m-%Y'))
            except Exception:
                end_var.set('')

    def on_calendar_select(event):
        idx = seat_combo.current()
        new_start = cal_widget.selection_get().strftime('%d-%m-%Y')
        start_var.set(new_start)
        update_selected_date_label(new_start)
        try:
            start_dt = datetime.strptime(new_start, '%d-%m-%Y')
            end_dt = start_dt + timedelta(days=30)
            seats[idx]['end_date'] = end_dt.strftime('%d-%m-%Y')
            end_var.set(seats[idx]['end_date'])
            clear_date_error()
        except Exception:
            end_var.set('')
            highlight_date_error()
        # Feed positive on Enter
        root.event_generate('<Return>')

    cal_widget.bind('<<CalendarSelected>>', on_calendar_select)
    cal_widget.bind('<Return>', lambda e: save_changes())

    def save_changes():
        # Validate all dates before saving
        for i, seat in enumerate(seats):
            if seat['name']:
                if not is_valid_date(seat['end_date']):
                    highlight_date_error()
                    warning_label.config(text=f"Invalid end date for seat {i+1}: {seat['end_date']}. Please select a valid date using the calendar.")
                    return
        clear_date_error()
        with open('seats_data.json', 'w') as f:
            json.dump(seats, f, indent=2)
        tk.messagebox.showinfo('Saved', 'Changes saved to seats_data.json')

    seat_numbers = [f"Seat {i+1}" for i in range(len(seats))]
    seat_combo = ttk.Combobox(root, values=seat_numbers, state='readonly')
    seat_combo.grid(row=0, column=1, padx=10, pady=10)
    seat_combo.set(seat_numbers[0])
    seat_combo.bind('<<ComboboxSelected>>', on_seat_select)

    ttk.Label(root, text='Select Seat:').grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(root, text='Student Name:').grid(row=1, column=0, padx=10, pady=10)
    name_var = tk.StringVar()
    ttk.Entry(root, textvariable=name_var, state='readonly').grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(root, text='Starting Date:').grid(row=2, column=0, padx=10, pady=10)
    start_var = tk.StringVar()

    ttk.Label(root, text='End Date:').grid(row=3, column=0, padx=10, pady=10)
    end_var = tk.StringVar()
    ttk.Entry(root, textvariable=end_var, state='readonly').grid(row=3, column=1, padx=10, pady=10)

    save_btn = ttk.Button(root, text='Save', command=save_changes)
    save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # Initialize with first seat
    on_seat_select(None)
    root.mainloop()

if __name__ == '__main__':
    show_editor()