import random

# Define the list of flight names and seat numbers
flight_names = ['Fly Amirates ZA45', 'SA Airs L908', 'Fly Amirates ZA40', 'SA Airs L909', 'SA Airs L911']
seat_numbers = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12', 'P13', 'P14']


# Function to register a user
def register():
    # Get the username and password from the user
    username = input("Create your username: ")
    password = input("Create your password: ")

    # Generate a random trip date, flight name, and seat number
    trip_date = f"{random.randint(1, 31)}/{random.randint(1, 12)}/{random.randint(2023, 2024)}"
    flight_name = random.choice(flight_names)
    seat_number = random.choice(seat_numbers)

    # Save the user's details in a text file
    with open("trips.txt", "a") as f:
        f.write(f"{username},{password},{trip_date},{flight_name},{seat_number}\n")

    print("User registered successfully!\n")


# Function to log in a user
def login():
    # Get the username and password from the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the user's details match the stored information
    with open("trips.txt", "r") as f:
        for line in f:
            fields = line.strip().split(",")
            if fields[0] == username and fields[1] == password:
                print(f"\nWelcome {username}!\n")
                print(f"Trip Date: {fields[2]}\nFlight Name: {fields[3]}\nSeat Number: {fields[4]}\n")
                return
    print("Invalid credentials!\n")


# Main program loop
while True:
    print("FLIGHT BOOKING SYSTEM")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        break
    else:
        print("Invalid choice!\n")
