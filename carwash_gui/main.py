import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
import csv
import os

LOG_FILE = "car_wash_log.txt"
CSV_FILE = "car_wash_log.csv"

# Service type to price mapping
PRICES = {
    "Basic": 10,
    "Premium": 20,
    "Deluxe": 30
}

# Add a new car entry and return the price
def add_car_entry(plate_number, car_type, service_type):
    now = datetime.datetime.now()
    price = PRICES.get(service_type, 0)
    entry = f"{now}, Plate: {plate_number}, Type: {car_type}, Service: {service_type}, Price: ${price}\n"
    with open(LOG_FILE, "a") as file:
        file.write(entry)
    return price

# Read all entries
def show_all_entries():
    try:
        with open(LOG_FILE, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No entries found yet."

# Export entries to CSV
def export_to_csv():
    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE, "r") as log_file, open(CSV_FILE, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Date", "Plate", "Car Type", "Service Type", "Price"])
        for line in log_file:
            try:
                parts = line.strip().split(", ")
                date = parts[0]
                plate = parts[1].split(": ")[1]
                car_type = parts[2].split(": ")[1]
                service = parts[3].split(": ")[1]
                price = parts[4].split(": ")[1]
                writer.writerow([date, plate, car_type, service, price])
            except IndexError:
                continue
    return True

# Calculate total earnings
def calculate_total_earnings():
    total = 0
    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                if "Price: $" in line:
                    try:
                        price_str = line.strip().split("Price: $")[1]
                        total += float(price_str)
                    except (IndexError, ValueError):
                        continue
        return total
    except FileNotFoundError:
        return 0

# GUI Class
class CarWashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Wash System with Pricing & CSV Export")
        self.root.geometry("520x580")

        tk.Label(root, text="🚗 Car Wash Entry", font=("Arial", 16)).pack(pady=10)

        # Plate Number
        tk.Label(root, text="License Plate:").pack()
        self.plate_entry = tk.Entry(root)
        self.plate_entry.pack()

        # Car Type
        tk.Label(root, text="Car Type (Sedan, SUV, etc.):").pack()
        self.car_type_entry = tk.Entry(root)
        self.car_type_entry.pack()

        # Service Type Dropdown
        tk.Label(root, text="Service Type:").pack()
        self.service_type = tk.StringVar()
        self.service_type.set("Basic")
        tk.OptionMenu(root, self.service_type, *PRICES.keys()).pack()

        # Buttons
        tk.Button(root, text="Add Entry", command=self.handle_add_entry).pack(pady=10)
        tk.Button(root, text="Show All Entries", command=self.handle_show_entries).pack()
        tk.Button(root, text="Export to CSV", command=self.handle_export_csv).pack(pady=5)
        tk.Button(root, text="Show Total Earnings", command=self.handle_total_earnings).pack(pady=5)

        # Output Box
        self.output_text = scrolledtext.ScrolledText(root, width=60, height=15)
        self.output_text.pack(pady=10)

    def handle_add_entry(self):
        plate = self.plate_entry.get().strip()
        car_type = self.car_type_entry.get().strip()
        service = self.service_type.get()

        if not plate or not car_type:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        price = add_car_entry(plate, car_type, service)
        messagebox.showinfo("Success", f"Car entry added.\nService cost: ${price}")
        self.clear_entries()

    def handle_show_entries(self):
        log = show_all_entries()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, log)

    def handle_export_csv(self):
        success = export_to_csv()
        if success:
            messagebox.showinfo("Export Complete", f"Data exported to {CSV_FILE}")
        else:
            messagebox.showerror("Error", "No entries to export.")

    def handle_total_earnings(self):
        total = calculate_total_earnings()
        messagebox.showinfo("Total Earnings", f"Total income from services: ${total:.2f}")

    def clear_entries(self):
        self.plate_entry.delete(0, tk.END)
        self.car_type_entry.delete(0, tk.END)
        self.service_type.set("Basic")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CarWashApp(root)
    root.mainloop()