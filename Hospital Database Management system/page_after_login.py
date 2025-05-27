from tkinter import *
from PIL import ImageTk, Image
import Login_PAGE
import AddPatients
import Appoinment_FILE
import time
from datetime import datetime


def page_after_login():
    def addpatients():
        window.destroy()
        AddPatients.add_patient()

    def addappointment():
        window.destroy()
        Appoinment_FILE.book_appointment()

    def sign_out():
        window.destroy()
        Login_PAGE.page()

    window = Tk()
    window.geometry('1366x768')
    window.resizable(1, 1)
    window.state('zoomed')
    window.title('Oakwell Medical - Dashboard')
    window.configure(bg='#0a1a2c')

    # Create main container
    main_container = Frame(window, bg='#0a1a2c')
    main_container.pack(fill='both', expand=True, padx=20, pady=20)

    # Left sidebar
    sidebar = Frame(main_container, bg='#0d1f34', padx=30, pady=30)
    sidebar.pack(side=LEFT, fill='y', padx=(0, 20))

    # Hospital Name
    hospital_name = Label(sidebar,
                          text="OAKWELL\nMEDICAL",
                          font=('Segoe UI', 32, "bold"),
                          bg='#0d1f34',
                          fg='white',
                          justify=LEFT)
    hospital_name.pack(anchor='w', pady=(0, 10))

    # Tagline
    tagline = Label(sidebar,
                    text="Advanced Healthcare Solutions",
                    font=('Segoe UI', 12),
                    bg='#0d1f34',
                    fg='#4a9eff')
    tagline.pack(anchor='w', pady=(0, 30))

    # Separator
    separator = Frame(sidebar, height=2, bg='#1e3951')
    separator.pack(fill='x', pady=20)

    # Current Time
    time_label = Label(sidebar,
                       font=('Segoe UI', 36),
                       bg='#0d1f34',
                       fg='white')
    time_label.pack(pady=(20, 5))

    # Current Date
    date_label = Label(sidebar,
                       font=('Segoe UI', 14),
                       bg='#0d1f34',
                       fg='#8a8a8a')
    date_label.pack()

    def update_time():
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%B %d, %Y")
        time_label.config(text=current_time)
        date_label.config(text=current_date)
        window.after(1000, update_time)

    update_time()

    # Main content area
    main_content = Frame(main_container, bg='#0a1a2c')
    main_content.pack(side=LEFT, fill='both', expand=True)

    # Welcome Text
    Label(main_content,
          text="Welcome to Dashboard",
          font=('Segoe UI', 24, "bold"),
          bg='#0a1a2c',
          fg='white').pack(anchor='w', pady=(0, 5))

    Label(main_content,
          text="Select an option to proceed",
          font=('Segoe UI', 14),
          bg='#0a1a2c',
          fg='#8a8a8a').pack(anchor='w', pady=(0, 30))

    # Function to create action cards
    def create_action_card(parent, title, description, command, color):
        # Card container
        card = Frame(parent, bg='#0d1f34', padx=25, pady=20)
        card.pack(fill='x', pady=10)

        # Content container
        content = Frame(card, bg='#0d1f34')
        content.pack(fill='x')

        title_label = Label(content,
                            text=title,
                            font=('Segoe UI', 16, 'bold'),
                            bg='#0d1f34',
                            fg='white')
        title_label.pack(anchor='w')

        desc_label = Label(content,
                           text=description,
                           font=('Segoe UI', 11),
                           bg='#0d1f34',
                           fg='#8a8a8a')
        desc_label.pack(anchor='w', pady=(5, 15))

        button = Button(content,
                        text="→",
                        font=('Segoe UI', 16, 'bold'),
                        bg=color,
                        fg='white',
                        command=command,
                        width=10,
                        height=1,
                        bd=0,
                        cursor='hand2',
                        activebackground=color,  # Set initial active background
                        activeforeground='white')
        button.pack(anchor='w')

        # Calculate hover colors
        hover_bg = '#162c43'  # Lighter shade for card background

        # Calculate darker button color for hover (20% darker)
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        hover_btn = f'#{int(r * 0.8):02x}{int(g * 0.8):02x}{int(b * 0.8):02x}'

        def on_hover(e):
            # Smooth transition for card background
            card.configure(bg=hover_bg)
            content.configure(bg=hover_bg)
            title_label.configure(bg=hover_bg)
            desc_label.configure(bg=hover_bg)
            # Darker shade for button
            button.configure(bg=hover_btn, activebackground=hover_btn)

        def on_leave(e):
            # Return to original colors
            card.configure(bg='#0d1f34')
            content.configure(bg='#0d1f34')
            title_label.configure(bg='#0d1f34')
            desc_label.configure(bg='#0d1f34')
            button.configure(bg=color, activebackground=color)

        # Bind hover events to the entire card
        for widget in [card, content, title_label, desc_label, button]:
            widget.bind('<Enter>', on_hover)
            widget.bind('<Leave>', on_leave)

        return card

    # Create action cards
    create_action_card(main_content,
                       "Enter Patient Data",
                       "Add and manage patient records and information",
                       addpatients,
                       '#2196F3')

    create_action_card(main_content,
                       "Book Appointment",
                       "Schedule and manage patient appointments",
                       addappointment,
                       '#4CAF50')

    create_action_card(main_content,
                       "Sign Out",
                       "Securely log out from the dashboard",
                       sign_out,
                       '#f44336')

    window.mainloop()

