import datetime

# File to store the log
LOG_FILE = "car_wash_log.txt"

# Function to add a new car entry
def add_car_entry(plate_number, car_type, service_type):
    now = datetime.datetime.now()
    entry = f"{now}, Plate: {plate_number}, Type: {car_type}, Service: {service_type}\n"
    with open(LOG_FILE, "a") as file:
        file.write(entry)
    print("Car entry added.")

# Function to show all cars served
def show_all_entries():
    try:
        with open(LOG_FILE, "r") as file:
            print("\n--- Car Wash Log ---")
            print(file.read())
    except FileNotFoundError:
        print("No entries found yet.")

# Main menu
def menu():
    while True:
        print("\nCar Wash Tracking System")
        print("1. Новая машина Camry you have to add")
        print("2. Show all served cars")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            plate = input("Enter license plate: ")
            ctype = input("Enter car type (Sedan, SUV, etc.): ")
            service = input("Enter service type (Basic, Premium, etc.): ")
            add_car_entry(plate, ctype, service)
        elif choice == "2":
            show_all_entries()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    menu()