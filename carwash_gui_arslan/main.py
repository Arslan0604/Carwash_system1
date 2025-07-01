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
    "I\u00e7i-da\u015fy": 50,
    "Gubka-aprat": 30,
    "Da\u015fy": 30,
    "I\u00e7i": 20 
}