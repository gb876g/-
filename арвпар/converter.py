import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

HISTORY_FILE = "history.json"

RATES = {
    "USD": 1.0000,
    "EUR": 0.9230,
    "RUB": 91.8500,
    "GBP": 0.7950,
    "CNY": 7.2350,
    "JPY": 154.2000
}

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def update_history_table():
    for row in tree.get_children():
        tree.delete(row)
    history = load_history()
    for record in reversed(history):
        tree.insert("", "end", values=(
            record["date"],
            record["from_currency"],
            record["to_currency"],
            f"{record['amount']:.2f}",
            f"{record['result']:.2f}"
        ))

def convert_currency():
    try:
        amount_text = entry_amount.get().strip()
        if not amount_text:
            messagebox.showwarning("Ошибка", "Введите сумму!")
            return
        amount = float(amount_text)
        if amount <= 0:
            messagebox.showwarning("Ошибка", "Сумма должна быть больше нуля!")
            return
        from_curr = combo_from.get()
        to_curr = combo_to.get()
        in_usd = amount / RATES[from_curr]
        result = in_usd * RATES[to_curr]
        label_result.config(text=f"{result:.2f} {to_curr}")
        history = load_history()
        history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from_currency": from_curr,
            "to_currency": to_curr,
            "amount": amount,
            "result": result
        })
        save_history(history)
        update_history_table()
    except ValueError:
        messagebox.showwarning("Ошибка", "Введите корректное число!")

def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        save_history([])
        update_history_table()
        messagebox.showinfo("Готово", "История очищена")

def swap_currencies():
    from_curr = combo_from.get()
    to_curr = combo_to.get()
    combo_from.set(to_curr)
    combo_to.set(from_curr)

root = tk.Tk()
root.title("Currency Converter")
root.geometry("800x600")
root.resizable(True, True)

currencies = list(RATES.keys())

title_label = tk.Label(root, text="Конвертер валют", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

converter_frame = tk.LabelFrame(main_frame, text="Конвертация", font=("Arial", 12, "bold"))
converter_frame.pack(fill="x", pady=10, padx=5)

tk.Label(converter_frame, text="Из валюты:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=15, sticky="w")
combo_from = ttk.Combobox(converter_frame, values=currencies, width=12, font=("Arial", 11))
combo_from.grid(row=0, column=1, padx=10, pady=15)
combo_from.set("USD")

swap_btn = tk.Button(converter_frame, text="⇄", font=("Arial", 12), command=swap_currencies)
swap_btn.grid(row=0, column=2, padx=10, pady=15)

tk.Label(converter_frame, text="В валюту:", font=("Arial", 11)).grid(row=0, column=3, padx=10, pady=15, sticky="w")
combo_to = ttk.Combobox(converter_frame, values=currencies, width=12, font=("Arial", 11))
combo_to.grid(row=0, column=4, padx=10, pady=15)
combo_to.set("RUB")

tk.Label(converter_frame, text="Сумма:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=15, sticky="w")
entry_amount = tk.Entry(converter_frame, width=15, font=("Arial", 11))
entry_amount.grid(row=1, column=1, padx=10, pady=15)

convert_btn = tk.Button(converter_frame, text="КОНВЕРТИРОВАТЬ", font=("Arial", 11, "bold"), bg="green", fg="white", command=convert_currency)
convert_btn.grid(row=1, column=2, padx=10, pady=15)

tk.Label(converter_frame, text="Результат:", font=("Arial", 11)).grid(row=1, column=3, padx=10, pady=15, sticky="w")
label_result = tk.Label(converter_frame, text="0.00", font=("Arial", 16, "bold"), fg="green")
label_result.grid(row=1, column=4, padx=10, pady=15)

history_frame = tk.LabelFrame(main_frame, text="История конвертаций", font=("Arial", 12, "bold"))
history_frame.pack(fill="both", expand=True, pady=10, padx=5)

clear_btn = tk.Button(history_frame, text="Очистить историю", font=("Arial", 10), command=clear_history)
clear_btn.pack(anchor="e", padx=10, pady=5)

columns = ("date", "from", "to", "amount", "result")
tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

tree.heading("date", text="Дата и время")
tree.heading("from", text="Из валюты")
tree.heading("to", text="В валюту")
tree.heading("amount", text="Сумма")
tree.heading("result", text="Результат")

tree.column("date", width=160)
tree.column("from", width=100)
tree.column("to", width=100)
tree.column("amount", width=100)
tree.column("result", width=120)

scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

update_history_table()

root.mainloop()