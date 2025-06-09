import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import hashlib
import json
import os
import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO

class FlightBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyWings Flight Booking System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ffffff")  # Pure white background
        self.root.resizable(True, True)
        
        # Color palette
        self.primary_color = "#005f87"    # Deep sky blue
        self.secondary_color = "#e1f5fe"  # Very light blue
        self.accent_color = "#ff5722"     # Vibrant orange
        self.text_color = "#333333"       # Dark gray
        self.light_text = "#ffffff"       # White
        self.success_color = "#4caf50"    # Green
        self.error_color = "#f44336"      # Red
        
        # Current user information
        self.current_user = None
        
        # Flight data
        self.flight_names = [
            'Emirates EK45', 'SA Airs SA908', 'Qatar Airways QR40',
            'British Airways BA909', 'Delta Airlines DL911',
            'Singapore Airlines SQ22', 'Lufthansa LH510'
        ]
        self.seat_classes = ["Economy", "Premium Economy", "Business", "First Class"]
        self.seat_numbers = [f"{row}{col}" for row in range(1, 21) for col in "ABCDEF"]
        self.destinations = {
            "New York (JFK)": 850,
            "London (LHR)": 650,
            "Paris (CDG)": 600,
            "Tokyo (HND)": 1200,
            "Dubai (DXB)": 750,
            "Sydney (SYD)": 1500,
            "Singapore (SIN)": 1300
        }
        
        # Aircraft images
        self.aircraft_images = []
        
        # Create database if not exists
        self.db_file = "flight_data.json"
        if not os.path.exists(self.db_file):
            self.create_database()
        
        # Load aircraft images
        self.load_aircraft_images()
        
        # Configure styles
        self.configure_styles()
        
        # Create GUI
        self.create_main_frame()

    def configure_styles(self):
        """Configure widget styles for consistent appearance"""
        style = ttk.Style()
        
        # Treeview style (flight table)
        style.configure("Treeview",
                      background="#ffffff",
                      foreground=self.text_color,
                      fieldbackground="#ffffff",
                      font=("Arial", 10))
        style.configure("Treeview.Heading",
                      font=("Arial", 10, "bold"),
                      background=self.primary_color,
                      foreground=self.light_text)
        style.map("Treeview",
                background=[('selected', self.primary_color)])
        
        # Button styles
        style.configure("TButton",
                      font=("Arial", 11),
                      padding=6,
                      background=self.primary_color,
                      foreground=self.light_text)
        style.map("TButton",
                background=[('active', self.accent_color)])
        
        # Label styles
        style.configure("Header.TLabel",
                      font=("Arial", 16, "bold"),
                      foreground=self.primary_color)
        style.configure("Subheader.TLabel",
                      font=("Arial", 12),
                      foreground=self.text_color)

    def load_aircraft_images(self):
        """Load aircraft images from online sources"""
        urls = [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Airbus_A380-841_Emirates_%28A6-EDR%29_%40_ARN_%282021-07-11%29_01.jpg/320px-Airbus_A380-841_Emirates_%28A6-EDR%29_%40_ARN_%282021-07-11%29_01.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Boeing_787-8_Dreamliner_%28ZA003%29.jpg/320px-Boeing_787-8_Dreamliner_%28ZA003%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Airbus_A350-941%2C_Air_France_%28F-HTYH%29_%40_ZRH_%282021-07-11%29_01.jpg/320px-Airbus_A350-941%2C_Air_France_%28F-HTYH%29_%40_ZRH_%282021-07-11%29_01.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Boeing_737_MAX_8%2C_Southwest_Airlines_%28N8712M%29_%40_PHX_%282021-09-19%29_01.jpg/320px-Boeing_737_MAX_8%2C_Southwest_Airlines_%28N8712M%29_%40_PHX_%282021-09-19%29_01.jpg"
        ]
        
        for url in urls:
            try:
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
                image = image.resize((300, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.aircraft_images.append(photo)
            except:
                # Fallback to a simple rectangle if image loading fails
                img = Image.new('RGB', (300, 150), color=self.secondary_color)
                photo = ImageTk.PhotoImage(img)
                self.aircraft_images.append(photo)

    def create_database(self):
        """Create initial database structure"""
        data = {
            "users": {},
            "bookings": {},
            "next_booking_id": 1
        }
        with open(self.db_file, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except:
            return {"users": {}, "bookings": {}, "next_booking_id": 1}

    def save_data(self, data):
        """Save data to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def clear_frame(self):
        """Clear all widgets from the root frame"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_frame(self):
        """Create the main application frame"""
        self.clear_frame()
        
        # Create header frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=100)
        header_frame.pack(fill="x")
        
        title = tk.Label(header_frame, text="SKYWINGS FLIGHT BOOKING SYSTEM", 
                        font=("Arial", 24, "bold"), fg=self.light_text, bg=self.primary_color)
        title.pack(pady=30)
        
        # Create content frame
        content_frame = tk.Frame(self.root, bg=self.secondary_color)
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Left side - Welcome and buttons
        left_frame = tk.Frame(content_frame, bg=self.secondary_color)
        left_frame.pack(side="left", fill="y", padx=(0, 30))
        
        welcome_label = tk.Label(left_frame, text="Welcome to SkyWings Airlines", 
                               font=("Arial", 18, "bold"), bg=self.secondary_color, fg=self.primary_color)
        welcome_label.pack(pady=20)
        
        desc_text = "Book flights to destinations worldwide with our premium service. " \
                   "Enjoy comfortable seating, gourmet meals, and exceptional service."
        desc_label = tk.Label(left_frame, text=desc_text, wraplength=300, 
                            font=("Arial", 11), bg=self.secondary_color, fg=self.text_color, justify="left")
        desc_label.pack(pady=10)
        
        # Aircraft image display
        aircraft_frame = tk.Frame(left_frame, bg=self.secondary_color)
        aircraft_frame.pack(pady=20)
        if self.aircraft_images:
            aircraft_label = tk.Label(aircraft_frame, image=self.aircraft_images[0], bg=self.secondary_color)
            aircraft_label.image = self.aircraft_images[0]  # Keep reference
            aircraft_label.pack()
        
        # Create buttons
        btn_frame = tk.Frame(left_frame, bg=self.secondary_color)
        btn_frame.pack(pady=20)
        
        button_style = {"font": ("Arial", 12), "width": 20, "height": 2, 
                        "bg": self.primary_color, "fg": self.light_text, "bd": 0}
        
        if not self.current_user:
            register_btn = tk.Button(btn_frame, text="Create Account", 
                                   command=self.show_register, **button_style)
            register_btn.pack(pady=10)
            
            login_btn = tk.Button(btn_frame, text="Login", 
                                 command=self.show_login, **button_style)
            login_btn.pack(pady=10)
        else:
            book_btn = tk.Button(btn_frame, text="Book a Flight", 
                                command=self.show_booking_form, **button_style)
            book_btn.pack(pady=10)
            
            my_bookings_btn = tk.Button(btn_frame, text="My Bookings", 
                                      command=self.show_my_bookings, **button_style)
            my_bookings_btn.pack(pady=10)
            
            logout_btn = tk.Button(btn_frame, text="Logout", 
                                 command=self.logout, **button_style)
            logout_btn.pack(pady=10)
        
        # Right side - Flight information
        right_frame = tk.Frame(content_frame, bg="white", relief="groove", bd=2)
        right_frame.pack(side="right", fill="both", expand=True)
        
        info_label = tk.Label(right_frame, text="Available Flights", 
                            font=("Arial", 16, "bold"), bg="white", fg=self.primary_color)
        info_label.pack(pady=15)
        
        # Create flight info table
        columns = ("Flight", "Destination", "Departure", "Arrival", "Duration", "Price")
        tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        tree.column("Flight", width=120, anchor="center")
        tree.column("Destination", width=150, anchor="center")
        tree.column("Departure", width=120, anchor="center")
        tree.column("Arrival", width=120, anchor="center")
        tree.column("Duration", width=100, anchor="center")
        tree.column("Price", width=100, anchor="center")
        
        # Add headings
        for col in columns:
            tree.heading(col, text=col)
        
        # Add sample flight data
        flights = [
            ("EK45", "New York (JFK)", "08:00", "13:30", "5h 30m", "$850"),
            ("SA908", "London (LHR)", "10:15", "16:45", "6h 30m", "$650"),
            ("QR40", "Paris (CDG)", "09:30", "15:45", "6h 15m", "$600"),
            ("DL911", "Tokyo (HND)", "11:00", "05:00+1", "14h 00m", "$1200"),
            ("SQ22", "Dubai (DXB)", "14:20", "22:10", "7h 50m", "$750"),
            ("LH510", "Sydney (SYD)", "22:00", "06:30+2", "16h 30m", "$1500"),
            ("AF123", "Singapore (SIN)", "13:45", "05:30+1", "15h 45m", "$1300")
        ]
        
        for flight in flights:
            tree.insert("", "end", values=flight)
        
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add some statistics
        stats_frame = tk.Frame(right_frame, bg="white")
        stats_frame.pack(fill="x", padx=20, pady=15)
        
        stats = [
            ("Daily Flights", "250+"),
            ("Destinations", "120+"),
            ("Aircraft Fleet", "85"),
            ("Satisfaction Rate", "98.2%")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg="white")
            stat_frame.grid(row=0, column=i, padx=10)
            
            tk.Label(stat_frame, text=label, font=("Arial", 10), 
                   bg="white", fg="#666666").pack()
            tk.Label(stat_frame, text=value, font=("Arial", 14, "bold"), 
                   bg="white", fg=self.primary_color).pack()
        
        # Footer
        footer = tk.Label(self.root, text="© 2023 SkyWings Airlines. All rights reserved.", 
                         font=("Arial", 9), bg=self.primary_color, fg=self.light_text)
        footer.pack(side="bottom", fill="x", pady=10)

    def show_register(self):
        """Show registration form"""
        self.clear_frame()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        tk.Label(header, text="Create New Account", font=("Arial", 20, "bold"), 
               fg=self.light_text, bg=self.primary_color).pack(pady=20)
        
        # Content
        content = tk.Frame(self.root, bg=self.secondary_color)
        content.pack(fill="both", expand=True, padx=100, pady=30)
        
        # Form frame
        form_frame = tk.Frame(content, bg="white", padx=30, pady=30, 
                            relief="groove", bd=2)
        form_frame.pack(fill="both", expand=True)
        
        # Form title
        tk.Label(form_frame, text="Create Your SkyWings Account", 
               font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, 
                                                          columnspan=2, pady=10)
        
        # Form fields
        labels = ["Full Name:", "Email Address:", "Username:", 
                 "Password:", "Confirm Password:", "Phone Number:"]
        entries = []
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, font=("Arial", 11), 
                   bg="white", anchor="e").grid(row=i+1, column=0, sticky="e", pady=8, padx=10)
            
            show = "*" if "Password" in label else ""
            entry = tk.Entry(form_frame, font=("Arial", 11), width=30, show=show)
            entry.grid(row=i+1, column=1, pady=8, padx=10)
            entries.append(entry)
        
        self.full_name, self.email, self.reg_username, self.reg_password, self.reg_confirm, self.phone = entries
        
        # Status label
        self.reg_status = tk.Label(form_frame, text="", font=("Arial", 10), 
                                 bg="white", fg=self.error_color)
        self.reg_status.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=len(labels)+2, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Register", font=("Arial", 11), 
                bg=self.primary_color, fg=self.light_text, width=12, command=self.register).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Back", font=("Arial", 11), 
                bg="#666", fg=self.light_text, width=12, command=self.create_main_frame).pack(side="left", padx=10)

    def show_login(self):
        """Show login form"""
        self.clear_frame()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        tk.Label(header, text="User Login", font=("Arial", 20, "bold"), 
               fg=self.light_text, bg=self.primary_color).pack(pady=20)
        
        # Content
        content = tk.Frame(self.root, bg=self.secondary_color)
        content.pack(fill="both", expand=True, padx=150, pady=30)
        
        # Login frame
        login_frame = tk.Frame(content, bg="white", padx=40, pady=40, 
                              relief="groove", bd=2)
        login_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(login_frame, text="Login to Your Account", 
               font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        # Form fields
        tk.Label(login_frame, text="Username:", font=("Arial", 11), 
               bg="white", anchor="w").pack(fill="x", pady=(20, 5))
        self.login_username = tk.Entry(login_frame, font=("Arial", 11), width=30)
        self.login_username.pack(fill="x", pady=5)
        
        tk.Label(login_frame, text="Password:", font=("Arial", 11), 
               bg="white", anchor="w").pack(fill="x", pady=(10, 5))
        self.login_password = tk.Entry(login_frame, font=("Arial", 11), 
                                     width=30, show="*")
        self.login_password.pack(fill="x", pady=5)
        
        # Remember me
        remember_frame = tk.Frame(login_frame, bg="white")
        remember_frame.pack(fill="x", pady=10)
        self.remember_var = tk.IntVar()
        tk.Checkbutton(remember_frame, text="Remember me", variable=self.remember_var,
                     bg="white").pack(side="left")
        
        # Forgot password
        tk.Button(remember_frame, text="Forgot Password?", font=("Arial", 9), 
                 bg="white", fg=self.primary_color, bd=0, command=self.show_password_reset).pack(side="right")
        
        # Status label
        self.login_status = tk.Label(login_frame, text="", font=("Arial", 10), 
                                   bg="white", fg=self.error_color)
        self.login_status.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(login_frame, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Login", font=("Arial", 11), 
                bg=self.primary_color, fg=self.light_text, width=12, command=self.login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Back", font=("Arial", 11), 
                bg="#666", fg=self.light_text, width=12, command=self.create_main_frame).pack(side="left", padx=10)

    def show_booking_form(self):
        """Show flight booking form"""
        self.clear_frame()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        tk.Label(header, text="Book a Flight", font=("Arial", 20, "bold"), 
               fg=self.light_text, bg=self.primary_color).pack(pady=20)
        
        # Content
        content = tk.Frame(self.root, bg=self.secondary_color)
        content.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Form frame
        form_frame = tk.Frame(content, bg="white", padx=20, pady=20, 
                            relief="groove", bd=2)
        form_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(form_frame, text="Flight Booking Details", 
               font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, 
                                                          columnspan=2, pady=10)
        
        # Form fields
        labels = ["Departure City:", "Destination:", "Travel Date:", 
                 "Passengers:", "Seat Class:", "Flight Preference:"]
        entries = []
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, font=("Arial", 11), 
                   bg="white", anchor="e").grid(row=i+1, column=0, sticky="e", pady=8, padx=10)
            
            if label == "Destination:":
                dest_var = tk.StringVar()
                dest_dropdown = ttk.Combobox(form_frame, textvariable=dest_var, 
                                           values=list(self.destinations.keys()), 
                                           font=("Arial", 11), width=27)
                dest_dropdown.grid(row=i+1, column=1, pady=8, padx=10)
                entries.append(dest_dropdown)
            elif label == "Seat Class:":
                class_var = tk.StringVar()
                class_dropdown = ttk.Combobox(form_frame, textvariable=class_var, 
                                            values=self.seat_classes, 
                                            font=("Arial", 11), width=27)
                class_dropdown.grid(row=i+1, column=1, pady=8, padx=10)
                entries.append(class_dropdown)
            elif label == "Passengers:":
                spinbox = tk.Spinbox(form_frame, from_=1, to=10, font=("Arial", 11), width=5)
                spinbox.grid(row=i+1, column=1, sticky="w", pady=8, padx=10)
                entries.append(spinbox)
            elif label == "Travel Date:":
                # Default to 7 days from now
                default_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
                date_entry = tk.Entry(form_frame, font=("Arial", 11), width=20)
                date_entry.insert(0, default_date)
                date_entry.grid(row=i+1, column=1, sticky="w", pady=8, padx=10)
                entries.append(date_entry)
            else:
                entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
                entry.grid(row=i+1, column=1, sticky="w", pady=8, padx=10)
                entries.append(entry)
        
        self.departure, self.destination, self.travel_date, self.passengers, self.seat_class, self.flight_pref = entries
        
        # Status label
        self.booking_status = tk.Label(form_frame, text="", font=("Arial", 10), 
                                    bg="white", fg=self.error_color)
        self.booking_status.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=len(labels)+2, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Search Flights", font=("Arial", 11), 
                bg=self.primary_color, fg=self.light_text, width=15, command=self.search_flights).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", font=("Arial", 11), 
                bg="#666", fg=self.light_text, width=15, command=self.create_main_frame).pack(side="left", padx=10)

    def show_my_bookings(self):
        """Show user's bookings"""
        self.clear_frame()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        tk.Label(header, text=f"{self.current_user}'s Bookings", font=("Arial", 20, "bold"), 
               fg=self.light_text, bg=self.primary_color).pack(pady=20)
        
        # Content
        content = tk.Frame(self.root, bg=self.secondary_color)
        content.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Bookings frame
        bookings_frame = tk.Frame(content, bg="white", padx=20, pady=20, 
                                relief="groove", bd=2)
        bookings_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(bookings_frame, text="Your Flight Bookings", 
               font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        # Load user bookings
        data = self.load_data()
        user_bookings = []
        
        for booking_id, booking in data["bookings"].items():
            if booking["username"] == self.current_user:
                user_bookings.append(booking)
        
        if not user_bookings:
            tk.Label(bookings_frame, text="You have no bookings yet.", 
                   font=("Arial", 12), bg="white").pack(pady=50)
        else:
            # Create a notebook for bookings
            notebook = ttk.Notebook(bookings_frame)
            notebook.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create a frame for each booking
            for booking in user_bookings:
                frame = tk.Frame(notebook, bg="white")
                notebook.add(frame, text=f"Booking {booking['id']}")
                
                # Booking details
                details = [
                    ("Booking ID:", booking["id"]),
                    ("Flight:", booking["flight"]),
                    ("From:", booking["departure"]),
                    ("To:", booking["destination"]),
                    ("Date:", booking["date"]),
                    ("Passengers:", booking["passengers"]),
                    ("Class:", booking["seat_class"]),
                    ("Seat:", booking["seat"]),
                    ("Price:", f"${booking['price']}"),
                    ("Status:", booking["status"])
                ]
                
                for i, (label, value) in enumerate(details):
                    tk.Label(frame, text=label, font=("Arial", 11, "bold"), 
                           bg="white", anchor="w").grid(row=i, column=0, sticky="w", padx=20, pady=5)
                    tk.Label(frame, text=value, font=("Arial", 11), 
                           bg="white", anchor="w").grid(row=i, column=1, sticky="w", padx=20, pady=5)
                
                # Action buttons
                btn_frame = tk.Frame(frame, bg="white")
                btn_frame.grid(row=len(details), column=0, columnspan=2, pady=20)
                
                tk.Button(btn_frame, text="Cancel Booking", font=("Arial", 10), 
                         bg=self.error_color, fg=self.light_text, width=15).pack(side="left", padx=10)
                tk.Button(btn_frame, text="Change Flight", font=("Arial", 10), 
                         bg=self.accent_color, fg=self.light_text, width=15).pack(side="left", padx=10)
                tk.Button(btn_frame, text="Print Ticket", font=("Arial", 10), 
                         bg=self.success_color, fg=self.light_text, width=15).pack(side="left", padx=10)
        
        # Back button
        tk.Button(content, text="Back to Main Menu", font=("Arial", 11), 
                 bg=self.primary_color, fg=self.light_text, command=self.create_main_frame).pack(pady=20)

    def register(self):
        """Register a new user"""
        full_name = self.full_name.get().strip()
        email = self.email.get().strip()
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        phone = self.phone.get().strip()
        
        # Validate inputs
        if not all([full_name, email, username, password, confirm, phone]):
            self.reg_status.config(text="All fields are required!")
            return
            
        if password != confirm:
            self.reg_status.config(text="Passwords do not match!")
            return
            
        # Load data
        data = self.load_data()
        
        # Check if username already exists
        if username in data["users"]:
            self.reg_status.config(text="Username already exists!")
            return
            
        # Create user
        data["users"][username] = {
            "password": self.hash_password(password),
            "full_name": full_name,
            "email": email,
            "phone": phone
        }
        
        # Save data
        self.save_data(data)
        
        # Show success message
        messagebox.showinfo("Registration Successful", 
                          "Your account has been created successfully!\nYou can now log in.")
        self.create_main_frame()

    def login(self):
        """Login user"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        # Validate inputs
        if not username or not password:
            self.login_status.config(text="Username and password are required!")
            return
            
        # Load data
        data = self.load_data()
        
        # Check credentials
        if username in data["users"]:
            stored_hash = data["users"][username]["password"]
            if stored_hash == self.hash_password(password):
                self.current_user = username
                self.create_main_frame()
                return
        
        # If we get here, credentials are invalid
        self.login_status.config(text="Invalid username or password!")

    def search_flights(self):
        """Search for available flights"""
        departure = self.departure.get().strip()
        destination = self.destination.get().strip()
        travel_date = self.travel_date.get().strip()
        passengers = self.passengers.get().strip()
        seat_class = self.seat_class.get().strip()
        
        # Validate inputs
        if not all([departure, destination, travel_date, passengers]):
            self.booking_status.config(text="All fields are required!")
            return
        
        # Generate a random flight
        flight = random.choice(self.flight_names)
        seat = random.choice(self.seat_numbers)
        
        # Calculate price
        base_price = self.destinations.get(destination, 500)
        class_multiplier = {"Economy": 1.0, "Premium Economy": 1.5, 
                          "Business": 2.5, "First Class": 4.0}.get(seat_class, 1.0)
        price = round(base_price * class_multiplier * int(passengers))
        
        # Create booking
        data = self.load_data()
        booking_id = data["next_booking_id"]
        
        data["bookings"][str(booking_id)] = {
            "id": booking_id,
            "username": self.current_user,
            "flight": flight,
            "departure": departure,
            "destination": destination,
            "date": travel_date,
            "passengers": passengers,
            "seat_class": seat_class,
            "seat": seat,
            "price": price,
            "status": "Confirmed"
        }
        
        data["next_booking_id"] += 1
        
        # Save data
        self.save_data(data)
        
        # Show success message
        messagebox.showinfo("Booking Confirmed", 
                          f"Your flight has been booked successfully!\n\n"
                          f"Flight: {flight}\n"
                          f"From: {departure} to {destination}\n"
                          f"Date: {travel_date}\n"
                          f"Passengers: {passengers}\n"
                          f"Class: {seat_class}\n"
                          f"Seat: {seat}\n"
                          f"Total Price: ${price}")
        
        self.create_main_frame()

    def show_password_reset(self):
        """Show password reset form"""
        messagebox.showinfo("Password Reset", 
                          "A password reset link has been sent to your registered email address.")

    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.create_main_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingSystem(root)
    root.mainloop()
