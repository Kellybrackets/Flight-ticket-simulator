import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import hashlib
import json
import os
import datetime
from PIL import Image, ImageTk
import webbrowser

class FlightBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyWings Premium Booking System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        
        # Modern color scheme
        self.bg_color = "#f5f5f5"  # Light gray background
        self.header_color = "#2c3e50"  # Dark blue header
        self.button_color = "#ecf0f1"  # Light gray buttons
        self.button_text_color = "#000000"  # Black button text
        self.accent_color = "#e74c3c"  # Red for important actions
        self.success_color = "#27ae60"  # Green for success
        
        # Current user and booking data
        self.current_user = None
        self.flight_data = self.load_flight_data()
        
        # Create UI
        self.setup_styles()
        self.create_main_menu()

    def setup_styles(self):
        """Configure modern widget styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button styles
        style.configure('TButton', 
                      font=('Helvetica', 12),
                      background=self.button_color,
                      foreground=self.button_text_color,
                      borderwidth=1,
                      relief="raised",
                      padding=10)
        
        style.map('TButton',
                background=[('active', '#bdc3c7')],
                relief=[('pressed', 'sunken')])
        
        # Label styles
        style.configure('Header.TLabel',
                      font=('Helvetica', 24, 'bold'),
                      foreground='white',
                      background=self.header_color)
        
        style.configure('Subheader.TLabel',
                      font=('Helvetica', 16),
                      foreground=self.header_color)

    def load_flight_data(self):
        """Load sample flight data"""
        return {
            "cities": ["New York", "London", "Paris", "Tokyo", "Dubai", "Sydney"],
            "airlines": ["Emirates", "Qatar Airways", "Singapore Airlines", "Lufthansa"],
            "classes": ["Economy", "Premium Economy", "Business", "First Class"],
            "airports": {
                "New York": "JFK",
                "London": "LHR",
                "Paris": "CDG",
                "Tokyo": "HND",
                "Dubai": "DXB",
                "Sydney": "SYD"
            }
        }

    def create_main_menu(self):
        """Create the main menu interface"""
        self.clear_frame()
        
        # Header with logo
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header, 
                 text="✈ SkyWings Premium", 
                 style='Header.TLabel').pack(pady=20)
        
        # Main content
        content = ttk.Frame(self.root)
        content.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Feature buttons grid
        button_frame = ttk.Frame(content)
        button_frame.pack(pady=50)
        
        buttons = [
            ("Search Flights", self.show_flight_search),
            ("My Bookings", self.show_my_bookings),
            ("Flight Deals", self.show_deals),
            ("Account Settings", self.show_account_settings)
        ]
        
        if not self.current_user:
            buttons.append(("Login/Register", self.show_auth_options))
        else:
            buttons.append(("Logout", self.logout))
        
        # Create buttons in a grid
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, 
                           text=text, 
                           command=command,
                           style='TButton')
            btn.grid(row=i//2, column=i%2, padx=15, pady=15, ipadx=20, ipady=15)
        
        # Flight status widget
        status_frame = ttk.LabelFrame(content, text="Flight Status")
        status_frame.pack(fill='x', pady=20)
        
        ttk.Label(status_frame, 
                 text="Check real-time flight status:").pack(pady=5)
        
        flight_entry = ttk.Entry(status_frame, width=20)
        flight_entry.pack(side='left', padx=5)
        
        ttk.Button(status_frame, 
                 text="Check Status", 
                 command=lambda: self.check_flight_status(flight_entry.get())).pack(side='left')
        
        # Footer
        footer = ttk.Frame(self.root)
        footer.pack(fill='x', pady=20)
        
        ttk.Button(footer, 
                 text="Customer Support", 
                 command=self.show_support).pack(side='left', padx=20)
        
        ttk.Button(footer, 
                 text="About Us", 
                 command=self.show_about).pack(side='right', padx=20)

    def show_flight_search(self):
        """Flight search interface"""
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header, 
                 text="✈ Find Your Flight", 
                 style='Header.TLabel').pack(pady=20)
        
        # Search form
        form = ttk.LabelFrame(self.root, text="Flight Search Criteria")
        form.pack(fill='both', padx=50, pady=20)
        
        # Form fields
        fields = [
            ("From:", "origin", self.flight_data['cities']),
            ("To:", "destination", self.flight_data['cities']),
            ("Departure:", "date", []),
            ("Return:", "date", []),
            ("Passengers:", "spin", (1, 8)),
            ("Class:", "class", self.flight_data['classes'])
        ]
        
        self.search_vars = {}
        
        for i, (label, field_type, options) in enumerate(fields):
            row = ttk.Frame(form)
            row.pack(fill='x', pady=10)
            
            ttk.Label(row, text=label, width=12).pack(side='left')
            
            if field_type in ["origin", "destination"]:
                var = tk.StringVar()
                combo = ttk.Combobox(row, textvariable=var, values=options)
                combo.pack(fill='x', expand=True)
                self.search_vars[field_type] = var
            elif field_type == "date":
                var = tk.StringVar()
                entry = ttk.Entry(row, textvariable=var)
                entry.pack(fill='x', expand=True)
                self.search_vars[field_type + str(i)] = var
            elif field_type == "spin":
                var = tk.IntVar(value=1)
                spin = ttk.Spinbox(row, from_=options[0], to=options[1], textvariable=var)
                spin.pack(side='left')
                self.search_vars["passengers"] = var
            elif field_type == "class":
                var = tk.StringVar()
                combo = ttk.Combobox(row, textvariable=var, values=options)
                combo.pack(fill='x', expand=True)
                self.search_vars["class"] = var
        
        # Action buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, 
                 text="Search Flights", 
                 command=self.search_flights).pack(side='left', padx=10)
        
        ttk.Button(button_frame, 
                 text="Back", 
                 command=self.create_main_menu).pack(side='left', padx=10)

    def search_flights(self):
        """Search for available flights"""
        results = ttk.LabelFrame(self.root, text="Available Flights")
        results.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Sample results table
        columns = ("Airline", "Flight", "Departure", "Arrival", "Duration", "Price")
        tree = ttk.Treeview(results, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        # Sample data
        flights = [
            ("Emirates", "EK202", "08:00", "14:30", "6h 30m", "$799"),
            ("Qatar Airways", "QR123", "10:15", "17:45", "7h 30m", "$899"),
            ("Singapore Airlines", "SQ321", "14:20", "06:30+1", "16h 10m", "$1299")
        ]
        
        for flight in flights:
            tree.insert("", "end", values=flight)
        
        tree.pack(fill='both', expand=True)
        
        # Booking button
        ttk.Button(results, 
                 text="Book Selected Flight", 
                 command=self.book_flight).pack(pady=10)

    def book_flight(self):
        """Book a flight"""
        messagebox.showinfo("Success", "Your flight has been booked successfully!")
        self.create_main_menu()

    def show_my_bookings(self):
        """Show user's bookings"""
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header, 
                 text="✈ My Bookings", 
                 style='Header.TLabel').pack(pady=20)
        
        # Booking list
        bookings = ttk.LabelFrame(self.root, text="Your Upcoming Trips")
        bookings.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Sample booking cards
        sample_bookings = [
            {
                "airline": "Emirates",
                "flight": "EK202",
                "route": "New York (JFK) → Dubai (DXB)",
                "date": "15 Jun 2023",
                "time": "08:00 - 14:30",
                "seat": "12A (Business)"
            },
            {
                "airline": "Qatar Airways",
                "flight": "QR123",
                "route": "Dubai (DXB) → London (LHR)",
                "date": "20 Jun 2023",
                "time": "10:15 - 17:45",
                "seat": "24B (Economy)"
            }
        ]
        
        for booking in sample_bookings:
            card = ttk.Frame(bookings, relief='groove', borderwidth=2)
            card.pack(fill='x', pady=10, padx=10)
            
            # Booking info
            ttk.Label(card, 
                     text=f"{booking['airline']} Flight {booking['flight']}",
                     font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=10, pady=5)
            
            ttk.Label(card, 
                     text=booking['route']).pack(anchor='w', padx=10)
            
            ttk.Label(card, 
                     text=f"{booking['date']} | {booking['time']} | {booking['seat']}").pack(anchor='w', padx=10, pady=5)
            
            # Action buttons
            btn_frame = ttk.Frame(card)
            btn_frame.pack(fill='x', pady=5)
            
            ttk.Button(btn_frame, 
                     text="View Ticket", 
                     command=lambda b=booking: self.view_ticket(b)).pack(side='left', padx=5)
            
            ttk.Button(btn_frame, 
                     text="Cancel", 
                     style='Accent.TButton').pack(side='left', padx=5)
            
            ttk.Button(btn_frame, 
                     text="Change Flight").pack(side='left', padx=5)
        
        ttk.Button(bookings, 
                 text="Back to Main Menu", 
                 command=self.create_main_menu).pack(pady=20)

    def view_ticket(self, booking):
        """View booking ticket"""
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title(f"Ticket - {booking['flight']}")
        
        # Ticket content
        ttk.Label(ticket_window, 
                 text=f"{booking['airline']}\nFlight {booking['flight']}",
                 font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        ttk.Label(ticket_window, 
                 text=booking['route']).pack()
        
        ttk.Label(ticket_window, 
                 text=f"Date: {booking['date']}\nTime: {booking['time']}\nSeat: {booking['seat']}").pack(pady=10)
        
        ttk.Button(ticket_window, 
                 text="Print Ticket").pack(pady=10)

    def show_deals(self):
        """Show special flight deals"""
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header, 
                 text="✈ Hot Deals", 
                 style='Header.TLabel').pack(pady=20)
        
        # Deals content
        deals = ttk.LabelFrame(self.root, text="Today's Best Deals")
        deals.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Sample deals
        sample_deals = [
            {
                "route": "New York → London",
                "price": "$499",
                "dates": "Jun 10 - Jun 30",
                "airline": "British Airways"
            },
            {
                "route": "Dubai → Singapore",
                "price": "$399",
                "dates": "Jun 15 - Jul 15",
                "airline": "Emirates"
            },
            {
                "route": "Paris → Tokyo",
                "price": "$899",
                "dates": "Jul 1 - Aug 15",
                "airline": "Japan Airlines"
            }
        ]
        
        for deal in sample_deals:
            card = ttk.Frame(deals, relief='groove', borderwidth=2)
            card.pack(fill='x', pady=10, padx=10)
            
            ttk.Label(card, 
                     text=deal['route'],
                     font=('Helvetica', 14, 'bold')).pack(anchor='w', padx=10, pady=5)
            
            ttk.Label(card, 
                     text=f"Only {deal['price']} | {deal['dates']}").pack(anchor='w', padx=10)
            
            ttk.Label(card, 
                     text=f"Operated by {deal['airline']}").pack(anchor='w', padx=10, pady=5)
            
            ttk.Button(card, 
                     text="Book Now",
                     command=lambda d=deal: self.book_deal(d)).pack(pady=5)
        
        ttk.Button(deals, 
                 text="Back to Main Menu", 
                 command=self.create_main_menu).pack(pady=20)

    def book_deal(self, deal):
        """Book a special deal"""
        messagebox.showinfo("Deal Booked", f"You've booked: {deal['route']} for {deal['price']}!")
        self.create_main_menu()

    def show_auth_options(self):
        """Show authentication options"""
        choice = messagebox.askquestion("Login/Register", "Do you have an account?")
        
        if choice == 'yes':
            self.show_login()
        else:
            self.show_register()

    def show_login(self):
        """Login dialog"""
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show='*')
        
        if username and password:
            self.current_user = username
            messagebox.showinfo("Welcome", f"Welcome back, {username}!")
            self.create_main_menu()

    def show_register(self):
        """Registration dialog"""
        username = simpledialog.askstring("Register", "Choose a username:")
        email = simpledialog.askstring("Register", "Enter your email:")
        password = simpledialog.askstring("Register", "Choose a password:", show='*')
        
        if username and email and password:
            self.current_user = username
            messagebox.showinfo("Success", "Account created successfully!")
            self.create_main_menu()

    def show_account_settings(self):
        """Account settings"""
        messagebox.showinfo("Account Settings", "Account settings will appear here")

    def check_flight_status(self, flight_number):
        """Check flight status"""
        messagebox.showinfo("Flight Status", f"Status for flight {flight_number}:\n\nOn Time")

    def show_support(self):
        """Open support page"""
        webbrowser.open("https://www.skywings.com/support")

    def show_about(self):
        """Show about information"""
        messagebox.showinfo("About SkyWings", "SkyWings Premium Booking System\nVersion 2.0")

    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.create_main_menu()

    def clear_frame(self):
        """Clear the current frame"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingSystem(root)
    root.mainloop()
