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
                price_str = parts[4].replace("Price: ", "")
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
                        price_str = parts[4].split("Price: ")[1]
                        price = float(price_str)
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

                        if start_date and date < start_date:
                            continue
                        if end_date and date > end_date:
                            continue

                        daily[date.strftime("%d-%m-%Y")] += price
                        weekly[f"{date.year}-W{date.isocalendar().week}"] += price
                        monthly[date.strftime("%Y-%m")] += price
                    except (IndexError, ValueError):
                        continue
    except FileNotFoundError:
        pass

    return daily, weekly, monthly

def plot_daily_earnings(daily_earnings):
    if not daily_earnings:
        messagebox.showinfo("Нет данных", "Нет данных о заработке.")
        return

    dates = sorted(daily_earnings.keys())
    values = [daily_earnings[d] for d in dates]

    plt.figure(figsize=(10, 5))
    plt.bar(dates, values, color="skyblue")
    plt.xlabel("Дата")
    plt.ylabel("Заработано (манат)")
    plt.title("Заработок по дням")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

class CarWashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления мойкой машин район 3 школы")
        self.root.geometry("540x740")

        tk.Label(root, text="\ud83d\ude97 Крутая мойка машин", font=("Arial", 16)).pack(pady=10)

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
        tk.Button(root, text="Доход за сегодня", command=self.handle_today_earnings).pack(pady=5)

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
            messagebox.showwarning("Input Error", "Пожалуйста, заполните все поля.")
            return

        price = add_car_entry(plate, car_type, service)
        messagebox.showinfo("Успешно", f"Машина добавлена.\nСтоимость услуги: {price} манат")
        self.clear_entries()

    def handle_show_entries(self):
        log = show_all_entries()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, log)

    def handle_export_excel(self):
        if export_to_excel():
            messagebox.showinfo("Экспорт завершён", f"Данные выгружены в {EXCEL_FILE}")
        else:
            messagebox.showerror("Ошибка", "Нет данных для экспорта.")

    def handle_total_earnings(self):
        total = calculate_total_earnings()
        messagebox.showinfo("Общий доход", f"Доход со всех услуг: {total:.2f} манат")

    def handle_today_earnings(self):
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        daily, _, _ = calculate_earnings_by_period()
        earnings = daily.get(today, 0.0)
        messagebox.showinfo("Доход за сегодня", f"Сегодня ({today}) заработано: {earnings:.2f} манат")

    def handle_period_earnings(self):
        start, end = self.start_date_entry.get().strip(), self.end_date_entry.get().strip()
        try:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d") if start else None
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1) if end else None
        except ValueError:
            messagebox.showerror("Ошибка формата", "Пожалуйста, используйте формат YYYY-MM-DD.")
            return

        daily, weekly, monthly = calculate_earnings_by_period(start_date, end_date)
        self.output_text.delete(1.0, tk.END)

        self.output_text.insert(tk.END, "\ud83d\udcc5 Доход по дням:\n")
        for day, total in sorted(daily.items()):
            self.output_text.insert(tk.END, f"{day}: {total:.2f} манат\n")

        self.output_text.insert(tk.END, "\n\ud83d\uddd3 Доход по неделям:\n")
        for week, total in sorted(weekly.items()):
            self.output_text.insert(tk.END, f"{week}: {total:.2f} манат\n")

        self.output_text.insert(tk.END, "\n\ud83d\udcc6 Доход по месяцам:\n")
        for month, total in sorted(monthly.items()):
            self.output_text.insert(tk.END, f"{month}: {total:.2f} манат\n")

        self.output_text.insert(tk.END, "\n\ud83d\udcb0 ИТОГО:\n")
        self.output_text.insert(tk.END, f"Всего за период (день): {sum(daily.values()):.2f} манат\n")
        self.output_text.insert(tk.END, f"Всего за период (неделя): {sum(weekly.values()):.2f} манат\n")
        self.output_text.insert(tk.END, f"Всего за период (месяц): {sum(monthly.values()):.2f} манат\n")

    def handle_plot_chart(self):
        start, end = self.start_date_entry.get().strip(), self.end_date_entry.get().strip()
        try:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d") if start else None
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1) if end else None
        except ValueError:
            messagebox.showerror("Ошибка формата", "Пожалуйста, используйте формат YYYY-MM-DD.")
            return

        daily, _, _ = calculate_earnings_by_period(start_date, end_date)
        plot_daily_earnings(daily)

    def clear_entries(self):
        self.plate_entry.delete(0, tk.END)
        self.car_type_entry.delete(0, tk.END)
        self.service_type.set("Вид работ")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarWashApp(root)
    root.mainloop()
