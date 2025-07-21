# Arslan you have to start from here your app
# Sostavit structury srochno
import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
import os
from collections import defaultdict
from openpyxl import Workbook
import matplotlib.pyplot as plt

LOG_FILE = "car_wash_log.txt"
EXCEL_FILE = "car_wash_log.xlsx"

PRICES = {
    "Içi-daşy": 50,
    "Gubka-aprat": 30,
    "Daşy": 30,
    "Içi": 20,
    "Daşy-Içi-Polirowka" : 80 
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