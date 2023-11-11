import random

flightNames = ['Fly Amirates ZA45','SA Airs L908','Fly Amirates ZA40','SA Airs L909','SA Airs L911']
seatNumbers = ['P01','P02','P03','P04','P05','P06','P07','P08','P09','P10','P11','P12','P13','P14']

def theRegister():
    user = input("Create your username: ")
    password = input("Create your password: ")

    tripDate = f"{random.randint(1, 31)}/{random.randint(1, 12)}/{random.randint(2023, 2024)}"
    flightName = random.choice(flightNames)
    seatNumber = random.choice(seatNumbers)

    file = open("trips.txt","a")
    file.write(f"{user},{password},{tripDate},{flightName},{seatNumber}\n")
    print("User registered successfully!\n")

def theLogin():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    file = open("trips.txt", "r")
    for line in file:
        value = line.strip().split(",")
        if value[0] == username and value[1] == password:
            print(f"\nWelcome {username}!\n")
            print(f"Trip Date: {value[2]}\nFlight Name: {value[3]}\nSeat Number: {value[4]}\n")
            return
    print("Invalid credentials!\n")


while True:
    print("FLIGHT BOOKING SYSTEM")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        theRegister()
    elif choice == "2":
        theLogin()
    elif choice == "3":
        break
    else:
        print("Invalid choice!\n")



