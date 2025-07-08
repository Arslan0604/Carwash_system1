import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
import os
from collections import defaultdict
from openpyxl import Workbook
import matplotlib.pyplot as plt
# have to start in here this project 

LOG_FILE = "car_wash_log.txt"
EXCEL_FILE = "car_wash_log.xlsx"

PRICES = {
    "Içi-daşy": 50,
    "Gubka-aprat": 30,
    "Daşy": 30,
    "Içi": 20 
}

def add_car_entry(plate_number, car_type, service_type):
    now = datetime.datetime.now()
    price = PRICES.get(service_type, 0)
    entry = f"{now}, Plate: {plate_number}, Type: {car_type}, Service: {service_type}, Price: {price}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)
    return price

def show_all_entries():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No entries found yet."
    
def export_to_excel():
    if not os.path.exists(LOG_FILE):
        return False
    
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Car Wash Log"
    ws.append(["Date", "Plate", "Car Type", "Service Type", "Price"])
    
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            try:
                parts = line.strip().split(", ")
                date = parts[0]
                plate = parts[1].split(": ")[1]
                car_type = parts[2].split(": ")[1]
                service = parts[3].split(": ")[1]
                price_str = parts[4].replace("Price: ", "")  # Fixed line
                ws.append([date, plate, car_type, service, float(price_str)])
            except (IndexError, ValueError):
                continue

    wb.save(EXCEL_FILE)
    return True

def calculate_total_earnings():
    total = 0
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "Price: " in line:
                    try:
                        price_str = line.strip().split("Price: ")[1]
                        total += float(price_str)
                    except (IndexError, ValueError):
                        continue
        return total
    except FileNotFoundError:
        return 0
    
def calculate_earnings_by_period(start_date=None, end_date=None):
    daily = defaultdict(float)
    weekly = defaultdict(float)
    monthly = defaultdict(float)

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "Price: " in line:
                    try:
                        parts = line.strip().split(", ")
                        date_str = parts[0]
                        price_str = parts[-1].split("Price: ")[1].lstrip("m")  # Remove optional "m" prefix
                        price = float(price_str)

                        # Fix: match correct format of the datetime string
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

                        if start_date and date < start_date:
                            continue
                        if end_date and date > end_date:
                            continue

                        daily[date.strftime("%d-%m-%Y")] += price
                        weekly[f"{date.year}-W{date.isocalendar()[1]}"] += price
                        monthly[date.strftime("%Y-%m")] += price

                    except (IndexError, ValueError):
                        continue
    except FileNotFoundError:
        pass

    return daily, weekly, monthly

def plot_daily_earnings(daily_earnings):
    if not daily_earnings:
        messagebox.showinfo("No Data", "No earnings data to plot.")
        return
    
    dates = sorted(daily_earnings.keys())
    values = [daily_earnings[d] for d in dates]
    
    
    plt.figure(figsize=(10, 5))
    plt.bar(dates, values, color="skyblue")
    plt.xlabel("Date")
    plt.ylabel("Earnings (m)")
    plt.title("Daily Car Wash Earnings")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
class CarWashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления мойкой машин район 3 школы")
        self.root.geometry("540x740")
        
        tk.Label(root, text="🚗 Крутая мойка машин", font=("Arial", 16)).pack(pady=10)

        tk.Label(root, text="Номер машины:").pack()
        self.plate_entry = tk.Entry(root)
        self.plate_entry.pack()
        
        tk.Label(root, text="Модель машины (Djeep, sedan etc.):").pack()
        self.car_type_entry = tk.Entry(root)
        self.car_type_entry.pack()
        
        tk.Label(root, text="Виды обслуживание:").pack()
        self.service_type = tk.StringVar(value="Вид работ")
        tk.OptionMenu(root, self.service_type, *PRICES.keys()).pack()
        
        tk.Button(root, text="Добавить", command=self.handle_add_entry).pack(pady=10)
        tk.Button(root, text="Просмотр всех добавленных", command=self.handle_show_entries).pack()
        tk.Button(root, text="Выгрузить в Excel", command=self.handle_export_excel).pack(pady=5)
        tk.Button(root, text="Показать общий заработок", command=self.handle_total_earnings).pack(pady=5)
        
        tk.Label(root, text="Начало периода (YYYY-MM-DD):").pack()
        self.start_date_entry = tk.Entry(root)
        self.start_date_entry.pack()
        
        tk.Label(root, text="Конец периода (YYYY-MM-DD):").pack()
        self.end_date_entry = tk.Entry(root)
        self.end_date_entry.pack()
        
        tk.Button(root, text="Показать доходы по периодам", command=self.handle_period_earnings).pack(pady=5)
        tk.Button(root, text="Диограмма ежедневного заробока", command=self.handle_plot_chart).pack(pady=5)
        
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
        messagebox.showinfo("Success", f"Car entry added.\nService cost: {price}")
        self.clear_entries()

    def handle_show_entries(self):
        log = show_all_entries()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, log)
        
    def handle_export_excel(self):
        if export_to_excel():
            messagebox.showinfo("Export Complete", f"Data exported to {EXCEL_FILE}")
        else:
            messagebox.showerror("Error", "No entries to export.")
