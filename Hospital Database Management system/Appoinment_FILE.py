import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import ast
import page_after_login

# Available time slots
TIME_SLOTS = [
    "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
    "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM",
    "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
    "04:00 PM", "04:30 PM", "05:00 PM"
]

# Global dictionary to store all appointments
APPOINTMENTS_DATA = {}
APPOINTMENTS_FILE = "appointments.txt"


def load_appointments():
    """Load appointments from the text file"""
    global APPOINTMENTS_DATA
    try:
        with open(APPOINTMENTS_FILE, 'r') as file:
            content = file.read().strip()
            if content:
                APPOINTMENTS_DATA = ast.literal_eval(content)
            else:
                APPOINTMENTS_DATA = {}
    except FileNotFoundError:
        APPOINTMENTS_DATA = {}
    except Exception as e:
        print(f"Error loading appointments: {e}")
        APPOINTMENTS_DATA = {}


def save_appointments():
    """Save appointments to the text file"""
    try:
        with open(APPOINTMENTS_FILE, 'w') as file:
            file.write(str(APPOINTMENTS_DATA))
    except Exception as e:
        print(f"Error saving appointments: {e}")
        mb.showerror("Error", "Failed to save appointments!")


def book_appointment():
    # Load existing appointments when opening the window
    load_appointments()

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)

        for appt_id, data in APPOINTMENTS_DATA.items():
            tree.insert('', END, values=(
                appt_id,
                data['name'],
                data['doctor'],
                data['phone'],
                data['gender'],
                data['date'],
                data['time'],
                data['reason']
            ))

    def reset_fields():
        name_strvar.set('')
        contact_strvar.set('')
        doctor_strvar.set('')
        gender_strvar.set('')
        time_strvar.set('Select Time')
        reason_strvar.set('')
        dob.set_date(datetime.datetime.now().date())

    def add_record():
        name = name_strvar.get().strip()
        doctor = doctor_strvar.get().strip()
        phone = contact_strvar.get().strip()
        gender = gender_strvar.get()
        date = dob.get_date().strftime('%Y-%m-%d')
        time = time_strvar.get()
        reason = reason_strvar.get().strip()

        if not all([name, doctor, phone, gender, date, time]) or time == 'Select Time':
            mb.showerror('Error!', "Please fill all the fields!")
            return

        # Check if the time slot is available for the selected date
        for appt_id, data in APPOINTMENTS_DATA.items():
            if data['date'] == date and data['time'] == time:
                mb.showerror('Error!', "This time slot is already booked!")
                return

        # Generate a unique appointment ID
        appt_id = str(len(APPOINTMENTS_DATA) + 1)
        while appt_id in APPOINTMENTS_DATA:
            appt_id = str(int(appt_id) + 1)

        APPOINTMENTS_DATA[appt_id] = {
            'name': name,
            'doctor': doctor,
            'phone': phone,
            'gender': gender,
            'date': date,
            'time': time,
            'reason': reason
        }

        save_appointments()
        refresh_table()
        reset_fields()
        mb.showinfo('Success', f"Appointment booked for {name}")

    def view_record():
        if not tree.selection():
            mb.showerror('Error!', 'Please select an appointment')
            return

        current_item = tree.focus()
        values = tree.item(current_item)['values']

        name_strvar.set(values[1])
        doctor_strvar.set(values[2])
        contact_strvar.set(values[3])
        gender_strvar.set(values[4])
        date = datetime.datetime.strptime(values[5], '%Y-%m-%d').date()
        dob.set_date(date)
        time_strvar.set(values[6])
        reason_strvar.set(values[7])

    def back():
        main.destroy()
        page_after_login.page_after_login()

    # Main Window
    main = Tk()
    main.title("Oakwell Medical - Appointment Management")
    main.geometry("1366x768")
    main.resizable(0, 0)
    main.state('zoomed')
    main.configure(bg='#0a1a2c')

    # Creating the StringVar variables
    name_strvar = StringVar()
    doctor_strvar = StringVar()
    contact_strvar = StringVar()
    gender_strvar = StringVar()
    time_strvar = StringVar(value='Select Time')
    reason_strvar = StringVar()

    # Main container with modern dark theme
    container = Frame(main, bg='#0a1a2c')
    container.pack(fill='both', expand=True, padx=20, pady=20)

    # Left frame for input fields
    left_frame = Frame(container, bg='#0d1f34', padx=20, pady=20)
    left_frame.pack(side=LEFT, fill='both', expand=True, padx=(0, 10))

    # Title
    Label(left_frame, text="Book Appointment",
          font=('Segoe UI', 24, 'bold'),
          bg='#0d1f34', fg='white').pack(pady=(0, 20))

    # Input fields with modern styling
    input_frame = Frame(left_frame, bg='#0d1f34')
    input_frame.pack(fill='x', pady=10)

    # Style for entry fields
    entry_style = {
        'font': ('Segoe UI', 12),
        'bg': '#162c43',
        'fg': 'white',
        'insertbackground': 'white',
        'relief': 'flat'
    }

    # Patient Name
    Label(input_frame, text="Patient Name", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    Entry(input_frame, textvariable=name_strvar,
          width=30, **entry_style).pack(fill='x', pady=(5, 15))

    # Contact Number
    Label(input_frame, text="Contact Number", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    Entry(input_frame, textvariable=contact_strvar,
          width=30, **entry_style).pack(fill='x', pady=(5, 15))

    # Doctor Name
    Label(input_frame, text="Doctor Name", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    Entry(input_frame, textvariable=doctor_strvar,
          width=30, **entry_style).pack(fill='x', pady=(5, 15))

    # Gender
    Label(input_frame, text="Gender", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    gender_menu = OptionMenu(input_frame, gender_strvar, 'Male', 'Female')
    gender_menu.config(font=('Segoe UI', 12), bg='#162c43', fg='white',
                       activebackground='#1e3951', activeforeground='white', bd=0)
    gender_menu["menu"].config(font=('Segoe UI', 12), bg='#162c43', fg='white')
    gender_menu.pack(fill='x', pady=(5, 15))

    # Appointment Date
    Label(input_frame, text="Appointment Date", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    dob = DateEntry(input_frame, font=('Segoe UI', 12), width=28,
                    background='#162c43', foreground='white',
                    borderwidth=0)
    dob.pack(fill='x', pady=(5, 15))

    # Appointment Time
    Label(input_frame, text="Appointment Time", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    time_menu = OptionMenu(input_frame, time_strvar, *TIME_SLOTS)
    time_menu.config(font=('Segoe UI', 12), bg='#162c43', fg='white',
                     activebackground='#1e3951', activeforeground='white', bd=0)
    time_menu["menu"].config(font=('Segoe UI', 12), bg='#162c43', fg='white')
    time_menu.pack(fill='x', pady=(5, 15))

    # Reason for Visit
    Label(input_frame, text="Reason for Visit", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').pack(anchor='w')
    Entry(input_frame, textvariable=reason_strvar,
          width=30, **entry_style).pack(fill='x', pady=(5, 15))

    # Buttons frame
    buttons_frame = Frame(left_frame, bg='#0d1f34')
    buttons_frame.pack(fill='x', pady=20)

    # Button style
    btn_style = {
        'font': ('Segoe UI', 12),
        'fg': 'white',
        'bd': 0,
        'cursor': 'hand2',
        'width': 15,
        'height': 2
    }

    # Action buttons
    Button(buttons_frame, text="Book Appointment", bg='#2196F3',
           activebackground='#1976D2', command=add_record,
           **btn_style).pack(side=LEFT, padx=5)

    Button(buttons_frame, text="Reset", bg='#FF9800',
           activebackground='#F57C00',
           command=reset_fields,
           **btn_style).pack(side=LEFT, padx=5)

    # Back button at bottom
    Button(left_frame, text="← Back", font=('Segoe UI', 12),
           bg='#1e3951', fg='white', bd=0,
           activebackground='#1e3951', activeforeground='white',
           command=back).pack(side=BOTTOM, fill='x', pady=(20, 0))

    # Right frame for appointment list
    right_frame = Frame(container, bg='#0d1f34')
    right_frame.pack(side=LEFT, fill='both', expand=True, padx=(10, 0))

    # Title for appointments list
    Label(right_frame, text="Appointments",
          font=('Segoe UI', 24, 'bold'),
          bg='#0d1f34', fg='white').pack(pady=(20, 20))

    # Treeview style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#162c43",
                    foreground="white",
                    fieldbackground="#162c43",
                    rowheight=30)
    style.configure("Treeview.Heading",
                    background="#1e3951",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading",
              background=[('active', '#1e3951')])

    # Create Treeview
    tree = ttk.Treeview(right_frame, height=20)
    tree['columns'] = ('ID', 'Name', 'Doctor', 'Phone', 'Gender', 'Date', 'Time', 'Reason')

    # Format columns
    tree.column('#0', width=0, stretch=NO)
    tree.column('ID', anchor=W, width=50)
    tree.column('Name', anchor=W, width=150)
    tree.column('Doctor', anchor=W, width=150)
    tree.column('Phone', anchor=W, width=120)
    tree.column('Gender', anchor=W, width=80)
    tree.column('Date', anchor=W, width=100)
    tree.column('Time', anchor=W, width=100)
    tree.column('Reason', anchor=W, width=150)

    # Create headings
    tree.heading('#0', text='', anchor=W)
    tree.heading('ID', text='ID', anchor=W)
    tree.heading('Name', text='Patient Name', anchor=W)
    tree.heading('Doctor', text='Doctor', anchor=W)
    tree.heading('Phone', text='Phone', anchor=W)
    tree.heading('Gender', text='Gender', anchor=W)
    tree.heading('Date', text='Date', anchor=W)
    tree.heading('Time', text='Time', anchor=W)
    tree.heading('Reason', text='Reason', anchor=W)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(right_frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    # Bind selection event
    tree.bind('<<TreeviewSelect>>', lambda e: view_record())

    # Initialize table with saved data
    refresh_table()

    main.mainloop()