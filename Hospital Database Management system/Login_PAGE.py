from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox as mb
import page_after_login

# Dictionary to store user credentials
USER_CREDENTIALS = {
    "admin": "admin123",
    "user1": "password123",
    "doctor": "hospital123",
    "bhupendra": "jogi",
    "rakhi": "sawant",
    "harry": "potter",
    "skibidi": "toilet",
}


class LoginPage:
    def __init__(self, window):
        def validate():
            username = self.username_entry.get()
            password = self.password_entry.get()

            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                window.destroy()
                page_after_login.page_after_login()
            else:
                mb.showerror('Error', 'Invalid username or password')

        # Window Configuration
        self.window = window
        self.window.geometry('1366x768')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Oakwell Medical - Login')
        self.window.configure(bg='#0a1a2c')  # Dark theme background

        # Main container with modern dark theme
        container = Frame(self.window, bg='#0a1a2c')
        container.pack(fill='both', expand=True, padx=20, pady=20)

        # Login Frame
        self.lgn_frame = Frame(container, bg='#0d1f34', padx=40, pady=40)
        self.lgn_frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=600)

        # Hospital Logo or Icon (if available)
        # self.logo = Label(self.lgn_frame, text="🏥", font=('Segoe UI', 48), bg='#0d1f34', fg='#2196F3')
        # self.logo.pack(pady=(20, 0))

        # Welcome Text with modern font
        self.txt = "Welcome to Oakwell Medical"
        self.heading = Label(self.lgn_frame, text=self.txt,
                             font=('Segoe UI', 22, "bold"),
                             bg="#0d1f34", fg='white')
        self.heading.pack(pady=(0, 10))

        # Subtitle
        self.subtitle = Label(self.lgn_frame, text="Sign in to continue",
                              font=('Segoe UI', 14),
                              bg="#0d1f34", fg='#8a8a8a')
        self.subtitle.pack(pady=(0, 40))

        # Input Container
        input_container = Frame(self.lgn_frame, bg='#0d1f34')
        input_container.pack(fill='x', padx=40)

        # Username Section
        Label(input_container, text="Username",
              font=('Segoe UI', 12),
              bg="#0d1f34", fg='#8a8a8a').pack(anchor='w')

        self.username_entry = Entry(input_container,
                                    font=("Segoe UI", 12),
                                    bg="#162c43",
                                    fg="white",
                                    insertbackground='white',
                                    relief='flat')
        self.username_entry.pack(fill='x', pady=(5, 30))

        # Password Section
        Label(input_container, text="Password",
              font=('Segoe UI', 12),
              bg="#0d1f34", fg='#8a8a8a').pack(anchor='w')

        # Password Entry Container
        pwd_container = Frame(input_container, bg='#0d1f34')
        pwd_container.pack(fill='x', pady=(5, 32))

        self.password_entry = Entry(pwd_container,
                                    font=("Segoe UI", 12),
                                    bg="#162c43",
                                    fg="white",
                                    insertbackground='white',
                                    relief='flat',
                                    show="•")
        self.password_entry.pack(side='left', fill='x', expand=True)

        # Show/Hide Password Button
        try:
            self.show_image = ImageTk.PhotoImage(file='images\\show.png')
            self.hide_image = ImageTk.PhotoImage(file='images\\hide.png')

            self.show_button = Button(pwd_container,
                                      image=self.show_image,
                                      command=self.show,
                                      bg='#162c43',
                                      activebackground='#1e3951',
                                      bd=0,
                                      cursor='hand2')
            self.show_button.pack(side='right', padx=(10, 0))
        except:
            # If images are not found, use text alternative
            self.show_button = Button(pwd_container,
                                      text="👁",
                                      command=self.show,
                                      font=('Segoe UI', 10),
                                      bg='#162c43',
                                      fg='white',
                                      activebackground='#1e3951',
                                      activeforeground='white',
                                      bd=0,
                                      cursor='hand2')
            self.show_button.pack(side='right', padx=(10, 0))

        # Button Container for better spacing
        button_container = Frame(self.lgn_frame, bg='#0d1f34')
        button_container.pack(fill='x', padx=40, pady=(20, 0))

        # Login Button
        self.login = Button(button_container,
                            text='SIGN IN',
                            font=("Segoe UI", 12, "bold"),
                            bg='#2196F3',
                            fg='white',
                            cursor='hand2',
                            activebackground='#1976D2',
                            activeforeground='white',
                            relief='flat',
                            command=validate)
        self.login.pack(fill='x', ipady=12)  # Slightly increased button height

        # Hover effects
        self.login.bind('<Enter>', lambda e: self.login.configure(bg='#1976D2'))
        self.login.bind('<Leave>', lambda e: self.login.configure(bg='#2196F3'))

        # Spacer Frame for flexible spacing
        spacer = Frame(self.lgn_frame, bg='#0d1f34', height=80)  # Adjusted height for better spacing
        spacer.pack(fill='x', expand=True)

        # Footer text
        footer = Label(self.lgn_frame,
                       text="© 2025 Oakwell Medical. All rights reserved.",
                       font=('Segoe UI', 9),
                       bg="#0d1f34",
                       fg='#8a8a8a')
        footer.pack(side='bottom', pady=20)

    def show(self):
        try:
            self.hide_button = Button(self.password_entry.master,
                                      image=self.hide_image,
                                      command=self.hide,
                                      bg='#162c43',
                                      activebackground='#1e3951',
                                      bd=0,
                                      cursor='hand2')
        except:
            self.hide_button = Button(self.password_entry.master,
                                      text="○",
                                      command=self.hide,
                                      font=('Segoe UI', 10),
                                      bg='#162c43',
                                      fg='white',
                                      activebackground='#1e3951',
                                      activeforeground='white',
                                      bd=0,
                                      cursor='hand2')
        self.hide_button.pack(side='right', padx=(10, 0))
        self.show_button.destroy()
        self.password_entry.config(show='')

    def hide(self):
        try:
            self.show_button = Button(self.password_entry.master,
                                      image=self.show_image,
                                      command=self.show,
                                      bg='#162c43',
                                      activebackground='#1e3951',
                                      bd=0,
                                      cursor='hand2')
        except:
            self.show_button = Button(self.password_entry.master,
                                      text="👁",
                                      command=self.show,
                                      font=('Segoe UI', 10),
                                      bg='#162c43',
                                      fg='white',
                                      activebackground='#1e3951',
                                      activeforeground='white',
                                      bd=0,
                                      cursor='hand2')
        self.show_button.pack(side='right', padx=(10, 0))
        self.hide_button.destroy()
        self.password_entry.config(show='•')


def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()
