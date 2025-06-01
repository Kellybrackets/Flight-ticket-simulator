# ✈️ Flight Ticket Simulator - Python Console Application

![Flight Booking Demo](flight-demo.gif) *<!-- Replace with your actual demo GIF -->*

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/your-username/Flight-ticket-simulator)

> **Your virtual travel agent** - A comprehensive flight booking system with real-time availability checks and booking management!

## 🌍 Key Features

### 🛫 Booking Engine
| Feature | Description |
|---------|-------------|
| **🔍 Flight Search** | Find flights by destination, date, and airline |
| **🎫 Ticket Booking** | Reserve seats with passenger details |
| **📅 Schedule Management** | View and modify travel dates |
| **📋 Booking History** | Access past and upcoming trips |

### 🛡️ System Reliability
- **Robust error handling** for all user inputs
- **Data persistence** using JSON file storage
- **Real-time seat availability** checks
- **Confirmation emails** (simulated)

## 🖥️ Console Interface Preview

## 🚀 Installation & Usage

```bash
# Clone repository
git clone https://github.com/your-username/Flight-ticket-simulator.git

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

💻 Code Architecture
Flight Data Structure
```bash
class Flight:
    def __init__(self, flight_no, origin, destination, departure, seats):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.departure = departure  # datetime object
        self.available_seats = seats
```

Booking Management
```bash
def book_flight(passenger_name, flight):
    if flight.available_seats > 0:
        booking = {
            "confirmation_no": generate_confirmation_number(),
            "passenger": passenger_name,
            "flight": flight.flight_no,
            "status": "CONFIRMED"
        }
        save_booking(booking)  # Saves to bookings.json
        return booking
    raise NoSeatsAvailableError
```
📊 Sample Database Structure
```bash
{
  "flights": [
    {
      "flight_no": "BA249",
      "origin": "LHR",
      "destination": "JFK",
      "departure": "2023-12-15T14:30:00",
      "seats": 120,
      "price": 599.99
    }
  ],
  "bookings": [
    {
      "confirmation_no": "ABC123",
      "passenger": "John Doe",
      "flight": "BA249",
      "status": "CONFIRMED"
    }
  ]
}
```

✈️ Flight Search Options
By destination (city or airport code)

By date range (flexible travel dates)

By price range (budget filtering)

By airline (carrier preference)

🧑‍💻 Development Roadmap
Core booking system

File-based data storage

Seat selection feature

Frequent flyer points

Web API integration

🤝 Contributing
We welcome aviation enthusiasts and developers!

🍴 Fork the repository

🌱 Create a feature branch

💻 Commit your changes

📤 Push to the branch

🔄 Open a pull request

