import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime
import os
from collections import defaultdict
from openpyxl import Workbook
import matplotlib.pyplot as plt


LOG_FILE = "car_wash_log.txt"
EXCEL_FILE = "car_wash_log.xlsx"