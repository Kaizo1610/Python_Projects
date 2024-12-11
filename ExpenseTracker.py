import datetime
import tkinter as tk
from tkinter import messagebox

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, amount, date=None):
        if date is None:
            date = datetime.date.today().strftime("%Y-%m-%d")
        self.expenses.append({"category": category, "amount": amount, "date": date})

    def remove_expense(self, category, amount, date=None):
        for expense in self.expenses:
            if expense["category"] == category and expense["amount"] == amount and (date is None or expense["date"] == date):
                self.expenses.remove(expense)
                break
        else:
            print(f"No matching expense found for category: {category}, amount: {amount}, date: {date}")

    def list_expenses(self):
        return self.expenses

    def total_expenses(self):
        return sum(expense["amount"] for expense in self.expenses)

    def total_expenses_in_date_range(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        total = sum(expense["amount"] for expense in self.expenses if start_date <= datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date() <= end_date)
        return total

    def average_expenses_per_day(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        total = self.total_expenses_in_date_range(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        num_days = (end_date - start_date).days + 1
        return total / num_days if num_days > 0 else 0

class ExpenseTrackerUI:
    def __init__(self, root):
        self.tracker = ExpenseTracker()
        self.root = root
        self.root.title("Expense Tracker")

        self.category_label = tk.Label(root, text="Category")
        self.category_label.grid(row=0, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=0, column=1)

        self.amount_label = tk.Label(root, text="Amount")
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1)

        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD)")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.remove_button = tk.Button(root, text="Remove Expense", command=self.remove_expense)
        self.remove_button.grid(row=4, column=0, columnspan=2)

        self.expenses_listbox = tk.Listbox(root, width=50)
        self.expenses_listbox.grid(row=5, column=0, columnspan=2)

        self.total_label = tk.Label(root, text="Total Expenses: $0.00")
        self.total_label.grid(row=6, column=0, columnspan=2)

        self.avg_label = tk.Label(root, text="Average Expenses per Day: $0.00")
        self.avg_label.grid(row=7, column=0, columnspan=2)

    def add_expense(self):
        category = self.category_entry.get()
        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        self.tracker.add_expense(category, amount, date)
        self.update_expenses_list()
        self.update_totals()

    def remove_expense(self):
        selected = self.expenses_listbox.curselection()
        if selected:
            expense = self.tracker.list_expenses()[selected[0]]
            self.tracker.remove_expense(expense["category"], expense["amount"], expense["date"])
            self.update_expenses_list()
            self.update_totals()
        else:
            messagebox.showwarning("Warning", "No expense selected")

    def update_expenses_list(self):
        self.expenses_listbox.delete(0, tk.END)
        for expense in self.tracker.list_expenses():
            self.expenses_listbox.insert(tk.END, f"{expense['category']}: ${expense['amount']:.2f} on {expense['date']}")

    def update_totals(self):
        total = self.tracker.total_expenses()
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")

        start_date = "2023-10-01"  # Example start date
        end_date = datetime.date.today().strftime("%Y-%m-%d")  # Today's date as end date
        avg = self.tracker.average_expenses_per_day(start_date, end_date)
        self.avg_label.config(text=f"Average Expenses per Day: ${avg:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerUI(root)
    root.mainloop()