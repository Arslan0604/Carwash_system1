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
    "Içi-Daşy": 50,
    "Gubka-aprat": 30,
    "Daşy": 30,
    "Içi": 20 
}
# razobratsya s etoy funciey srochno
def add_car_entry(plate_number, car_type, service_type):
    now = datetime.datetime.now()
    price = PRICES.get(service_type, 0)
    entry = f"{now}, Plate: {plate_number}, Type: {car_type}, Service: {service_type}, Price: {price}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)
    return price