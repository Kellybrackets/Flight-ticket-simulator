import tkinter as tk
from tkinter import messagebox, ttk
import random
import hashlib
import os
import json

class FlightBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.flight_names = ['Fly Emirates ZA45', 'SA Airs L908', 'Fly Emirates ZA40', 
                            'SA Airs L909', 'SA Airs L911']
        self.seat_numbers = [f"P{i:02d}" for i in range(1, 15)]
        self.users_file = "users.json"
        self.current_user = None
        
        self.setup_styles()
        self.create_main_frame()
        
        # Create data file if it doesn't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), padding=6)
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Success.TLabel', foreground='green')
        self.style.configure('Error.TLabel', foreground='red')

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_frame(self):
        self.clear_frame()
        ttk.Label(self.root, text="FLIGHT BOOKING SYSTEM", style='Header.TLabel').pack(pady=20)
        
        ttk.Button(self.root, text="Register", command=self.show_register,
                  width=20).pack(pady=10)
        ttk.Button(self.root, text="Login", command=self.show_login,
                  width=20).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.destroy,
                  width=20).pack(pady=10)

    def show_register(self):
        self.clear_frame()
        ttk.Label(self.root, text="Create New Account", style='Header.TLabel').pack(pady=10)
        
        ttk.Label(self.root, text="Username:").pack(pady=5)
        self.reg_username = ttk.Entry(self.root, width=30)
        self.reg_username.pack(pady=5)
        
        ttk.Label(self.root, text="Password:").pack(pady=5)
        self.reg_password = ttk.Entry(self.root, width=30, show="*")
        self.reg_password.pack(pady=5)
        
        ttk.Label(self.root, text="Confirm Password:").pack(pady=5)
        self.reg_confirm = ttk.Entry(self.root, width=30, show="*")
        self.reg_confirm.pack(pady=5)
        
        self.reg_status = ttk.Label(self.root, text="", style='Error.TLabel')
        self.reg_status.pack(pady=5)
        
        ttk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_frame).pack(pady=5)

    def show_login(self):
        self.clear_frame()
        ttk.Label(self.root, text="User Login", style='Header.TLabel').pack(pady=10)
        
        ttk.Label(self.root, text="Username:").pack(pady=5)
        self.login_username = ttk.Entry(self.root, width=30)
        self.login_username.pack(pady=5)
        
        ttk.Label(self.root, text="Password:").pack(pady=5)
        self.login_password = ttk.Entry(self.root, width=30, show="*")
        self.login_password.pack(pady=5)
        
        self.login_status = ttk.Label(self.root, text="", style='Error.TLabel')
        self.login_status.pack(pady=5)
        
        ttk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_main_frame).pack(pady=5)

    def show_booking(self):
        self.clear_frame()
        user_data = self.load_users().get(self.current_user)
        
        ttk.Label(self.root, text="BOOKING DETAILS", style='Header.TLabel').pack(pady=10)
        
        details = [
            ("Username:", self.current_user),
            ("Trip Date:", user_data['trip_date']),
            ("Flight Name:", user_data['flight_name']),
            ("Seat Number:", user_data['seat_number'])
        ]
        
        for label, value in details:
            frame = ttk.Frame(self.root)
            frame.pack(fill='x', padx=50, pady=5)
            ttk.Label(frame, text=label, width=15, anchor='e').pack(side='left')
            ttk.Label(frame, text=value, anchor='w').pack(side='left', fill='x', expand=True)
        
        ttk.Button(self.root, text="Logout", command=self.create_main_frame).pack(pady=20)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f)

    def register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if not username or not password:
            self.reg_status.config(text="Username and password are required!")
            return
        
        if password != confirm:
            self.reg_status.config(text="Passwords do not match!")
            return
            
        users = self.load_users()
        if username in users:
            self.reg_status.config(text="Username already exists!")
            return
            
        # Generate booking details
        trip_date = f"{random.randint(1, 31):02d}/{random.randint(1, 12):02d}/{random.randint(2023, 2024)}"
        flight_name = random.choice(self.flight_names)
        seat_number = random.choice(self.seat_numbers)
        
        # Store user data
        users[username] = {
            'password': self.hash_password(password),
            'trip_date': trip_date,
            'flight_name': flight_name,
            'seat_number': seat_number
        }
        
        self.save_users(users)
        messagebox.showinfo("Success", "Registration successful!")
        self.create_main_frame()

    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            self.login_status.config(text="Username and password are required!")
            return
            
        users = self.load_users()
        user_data = users.get(username)
        
        if not user_data or user_data['password'] != self.hash_password(password):
            self.login_status.config(text="Invalid credentials!")
            return
            
        self.current_user = username
        self.show_booking()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingSystem(root)
    root.mainloop()
