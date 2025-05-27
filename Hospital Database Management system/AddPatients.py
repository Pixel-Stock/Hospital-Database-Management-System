from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import page_after_login
from datetime import datetime
import ast

# Global dictionary to store patient data
PATIENTS_DATA = {}
DATA_FILE = "patients_data.txt"


def load_data():
    global PATIENTS_DATA
    try:
        with open(DATA_FILE, 'r') as file:
            content = file.read()
            if content:
                # Using ast.literal_eval for safe dictionary reading
                PATIENTS_DATA = ast.literal_eval(content)
            else:
                PATIENTS_DATA = {}
    except FileNotFoundError:
        PATIENTS_DATA = {}


def save_data():
    with open(DATA_FILE, 'w') as file:
        # Writing the dictionary in a readable format
        file.write(str(PATIENTS_DATA))


def add_patient():
    # Load existing data when opening the window
    load_data()

    def refresh_table():
        for item in my_tree.get_children():
            my_tree.delete(item)

        for mobile, data in PATIENTS_DATA.items():
            my_tree.insert('', 'end', values=(mobile, data['name'], data['dob'],
                                              data['history'], data['medicines']))

    def add():
        mobile = str(mobile_entry.get()).strip()
        name = str(name_entry.get()).strip()
        dob = str(dob_entry.get()).strip()
        history = str(history_entry.get()).strip()
        medicines = str(medicines_entry.get()).strip()

        if not all([mobile, name, dob, history, medicines]):
            messagebox.showinfo("Error", "Please fill all fields")
            return

        if mobile in PATIENTS_DATA:
            messagebox.showinfo("Error", "Patient already exists")
            return

        PATIENTS_DATA[mobile] = {
            'name': name,
            'dob': dob,
            'history': history,
            'medicines': medicines
        }
        save_data()  # Save after adding
        refresh_table()
        clear_entries()

    def update():
        try:
            selected = my_tree.selection()[0]
            mobile = str(mobile_entry.get()).strip()
            name = str(name_entry.get()).strip()
            dob = str(dob_entry.get()).strip()
            history = str(history_entry.get()).strip()
            medicines = str(medicines_entry.get()).strip()

            if not all([mobile, name, dob, history, medicines]):
                messagebox.showinfo("Error", "Please fill all fields")
                return

            PATIENTS_DATA[mobile] = {
                'name': name,
                'dob': dob,
                'history': history,
                'medicines': medicines
            }
            save_data()  # Save after updating
            refresh_table()
            clear_entries()
        except IndexError:
            messagebox.showinfo("Error", "Please select a patient to update")

    def delete():
        try:
            selected = my_tree.selection()[0]
            mobile = my_tree.item(selected)['values'][0]

            if messagebox.askyesno("Confirm", "Delete this patient?"):
                del PATIENTS_DATA[mobile]
                save_data()  # Save after deleting
                refresh_table()
                clear_entries()
        except IndexError:
            messagebox.showinfo("Error", "Please select a patient to delete")

    def select_record(event):
        try:
            selected = my_tree.selection()[0]
            values = my_tree.item(selected)['values']
            clear_entries()
            mobile_entry.insert(0, values[0])
            name_entry.insert(0, values[1])
            dob_entry.insert(0, values[2])
            history_entry.insert(0, values[3])
            medicines_entry.insert(0, values[4])
        except IndexError:
            pass

    def clear_entries():
        mobile_entry.delete(0, END)
        name_entry.delete(0, END)
        dob_entry.delete(0, END)
        history_entry.delete(0, END)
        medicines_entry.delete(0, END)

    def back():
        root.destroy()
        page_after_login.page_after_login()

    root = Tk()
    root.title("Oakwell Medical - Patient Management")
    root.geometry("1366x768")
    root.state('zoomed')
    root.configure(bg='#0a1a2c')

    # Main container
    main_container = Frame(root, bg='#0a1a2c')
    main_container.pack(fill='both', expand=True, padx=20, pady=20)

    # Left sidebar
    sidebar = Frame(main_container, bg='#0d1f34', padx=30, pady=30)
    sidebar.pack(side=LEFT, fill='y', padx=(0, 20))

    # Hospital Name
    hospital_name = Label(sidebar, text="OAKWELL\nMEDICAL",
                          font=('Segoe UI', 32, "bold"),
                          bg='#0d1f34', fg='white', justify=LEFT)
    hospital_name.pack(anchor='w', pady=(0, 10))

    # Current Time
    time_label = Label(sidebar, font=('Segoe UI', 36), bg='#0d1f34', fg='white')
    date_label = Label(sidebar, font=('Segoe UI', 14), bg='#0d1f34', fg='#8a8a8a')
    time_label.pack(pady=(20, 5))
    date_label.pack()

    def update_time():
        time_label.config(text=datetime.now().strftime("%I:%M %p"))
        date_label.config(text=datetime.now().strftime("%B %d, %Y"))
        root.after(1000, update_time)

    update_time()

    # Back Button
    back_btn = Button(sidebar, text="← Back", font=('Segoe UI', 12),
                      bg='#1e3951', fg='white', bd=0, cursor='hand2',
                      activebackground='#1e3951', activeforeground='white',
                      command=back)
    back_btn.pack(side=BOTTOM, pady=20, fill='x')

    # Main content area
    content = Frame(main_container, bg='#0d1f34')
    content.pack(side=LEFT, fill='both', expand=True)

    # Title
    title_frame = Frame(content, bg='#0d1f34', pady=20)
    title_frame.pack(fill='x')

    Label(title_frame, text="Patient Management",
          font=('Segoe UI', 24, "bold"),
          bg='#0d1f34', fg='white').pack(side=LEFT, padx=20)

    # Entry Fields Frame
    entry_frame = Frame(content, bg='#0d1f34', padx=20, pady=20)
    entry_frame.pack(fill='x')

    # Style for entry fields
    entry_style = {
        'font': ('Segoe UI', 12),
        'bg': '#162c43',
        'fg': 'white',
        'insertbackground': 'white',
        'relief': 'flat',
        'width': 30
    }

    # Labels and Entries
    Label(entry_frame, text="Mobile", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').grid(row=0, column=0, padx=5, pady=5, sticky='w')
    mobile_entry = Entry(entry_frame, **entry_style)
    mobile_entry.grid(row=1, column=0, padx=5, pady=5)

    Label(entry_frame, text="Name", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').grid(row=0, column=1, padx=5, pady=5, sticky='w')
    name_entry = Entry(entry_frame, **entry_style)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(entry_frame, text="Date of Birth", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').grid(row=2, column=0, padx=5, pady=5, sticky='w')
    dob_entry = Entry(entry_frame, **entry_style)
    dob_entry.grid(row=3, column=0, padx=5, pady=5)

    Label(entry_frame, text="Medical History", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').grid(row=2, column=1, padx=5, pady=5, sticky='w')
    history_entry = Entry(entry_frame, **entry_style)
    history_entry.grid(row=3, column=1, padx=5, pady=5)

    Label(entry_frame, text="Medicines", font=('Segoe UI', 12),
          bg='#0d1f34', fg='#8a8a8a').grid(row=4, column=0, padx=5, pady=5, sticky='w')
    medicines_entry = Entry(entry_frame, **entry_style)
    medicines_entry.grid(row=5, column=0, padx=5, pady=5)

    # Buttons Frame
    btn_frame = Frame(entry_frame, bg='#0d1f34')
    btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

    # Button style
    btn_style = {
        'font': ('Segoe UI', 12),
        'fg': 'white',
        'bd': 0,
        'cursor': 'hand2',
        'width': 15,
        'height': 2
    }

    add_btn = Button(btn_frame, text="Add Patient", bg='#2196F3',
                     activebackground='#1976D2', command=add, **btn_style)
    add_btn.pack(side=LEFT, padx=5)

    update_btn = Button(btn_frame, text="Update", bg='#4CAF50',
                        activebackground='#388E3C', command=update, **btn_style)
    update_btn.pack(side=LEFT, padx=5)

    delete_btn = Button(btn_frame, text="Delete", bg='#f44336',
                        activebackground='#d32f2f', command=delete, **btn_style)
    delete_btn.pack(side=LEFT, padx=5)

    # Treeview
    tree_frame = Frame(content, bg='#0d1f34', padx=20, pady=20)
    tree_frame.pack(fill='both', expand=True)

    # Style the Treeview
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
    my_tree = ttk.Treeview(tree_frame, height=10)
    my_tree['columns'] = ('Mobile', 'Name', 'DOB', 'History', 'Medicines')

    # Format columns
    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('Mobile', anchor=W, width=140)
    my_tree.column('Name', anchor=W, width=200)
    my_tree.column('DOB', anchor=W, width=140)
    my_tree.column('History', anchor=W, width=300)
    my_tree.column('Medicines', anchor=W, width=300)

    # Create headings
    my_tree.heading('#0', text='', anchor=W)
    my_tree.heading('Mobile', text='Mobile', anchor=W)
    my_tree.heading('Name', text='Name', anchor=W)
    my_tree.heading('DOB', text='Date of Birth', anchor=W)
    my_tree.heading('History', text='Medical History', anchor=W)
    my_tree.heading('Medicines', text='Medicines', anchor=W)

    my_tree.pack(fill='both', expand=True)
    my_tree.bind('<<TreeviewSelect>>', select_record)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=my_tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_tree.configure(yscrollcommand=scrollbar.set)

    # Initialize table with saved data
    refresh_table()

    root.mainloop()

