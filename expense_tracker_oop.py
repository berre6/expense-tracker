from datetime import datetime
from zoneinfo import ZoneInfo
from database import add_expense, get_expenses, delete_expense as delete_expense_from_db, update_expense as update_expense_from_db

class Expense:

    def __init__(self, name, amount, category, date=None, id=None): 
        self.name = name
        self.amount = amount
        self.category = category
        self.id = id

        if date is None:
          self.date = datetime.now(ZoneInfo("Europe/Istanbul"))
        else:
          self.date = date



    def __str__(self):
      return f"{self.name} - {self.category} - {self.amount} TL"



class ExpenseTracker:

    def __init__(self):
      loaded_expenses = sorted(
      get_expenses(),
      key=lambda expense: expense[0]
)
      self.expenses = []

      for expense in loaded_expenses:
        self.expenses.append(
            Expense(
                expense[1],
                expense[2],
                expense[3],
                datetime.fromisoformat(expense[4]),
                expense[0]
            )
        )

    def get_expense_count(self):
        return len(self.expenses)


    def add_expense(self, name, amount, category):

      expense = Expense(name, amount, category)

      add_expense(
        name,
        amount,
        category,
        expense.date.isoformat()
    )

      self.expenses = []

      for expense in sorted(
      get_expenses(),
      key=lambda expense: expense[0]
       ):
       self.expenses.append(
            Expense(
                expense[1],
                expense[2],
                expense[3],
                datetime.fromisoformat(expense[4]),
                expense[0]
            )
        )
        

    def calculate_total(self):
        total = 0

        for expense in self.expenses:
            total += expense.amount

        return total

    def show_expenses(self):
        if not self.expenses:
            print("Harcama yok.")
            return

        for expense in self.expenses:
          print(expense)

    def get_by_category(self, category):
        filtered_expenses = []

        for expense in self.expenses:
            if expense.category == category:
                filtered_expenses.append(expense)

        return filtered_expenses

    def calculate_category_total(self, category):
        total = 0

        for expense in self.expenses:
            if expense.category == category:
                total += expense.amount

        return total

    def delete_expense(self, name, category):
        for expense in self.expenses:
            if expense.name == name and expense.category == category:
                delete_expense_from_db(expense.id)
                self.expenses.remove(expense)
                return True

        return False

    def update_expense(self, name, category, new_amount):
        for expense in self.expenses:
            if expense.name == name and expense.category == category:
                update_expense_from_db(expense.id, new_amount)
                expense.amount = new_amount
                return True

        return False



