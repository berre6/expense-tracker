from storage import load_expenses, save_expenses
from datetime import datetime
from zoneinfo import ZoneInfo


class Expense:

    def __init__(self, name, amount, category, date=None):
        self.name = name
        self.amount = amount
        self.category = category

        if date is None:
          self.date = datetime.now(ZoneInfo("Europe/Istanbul"))
        else:
          self.date = date



    def __str__(self):
      return f"{self.name} - {self.category} - {self.amount} TL"


    def to_dict(self):
      return {
        "name": self.name,
        "amount": self.amount,
        "category": self.category,
        "date": self.date.isoformat()
    
    }


    @classmethod
    def from_dict(cls, data):
     return cls(
        data["name"],
        data["amount"],
        data["category"],
        datetime.fromisoformat(data["date"])
    )

  

    

    
   
 

class ExpenseTracker:

    def __init__(self):
      loaded_expenses = load_expenses()

      self.expenses = []

      for expense in loaded_expenses:
        self.expenses.append(
            Expense.from_dict(expense)
        )

    def get_expense_count(self):
        return len(self.expenses)

    def save(self):
         save_expenses(self.expenses)

    def add_expense(self, name, amount, category):
        for expense in self.expenses:
            if expense.name == name and expense.category == category:
                expense.amount += amount
                return

        self.expenses.append(
            Expense(name, amount, category)
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
                self.expenses.remove(expense)
                return True

        return False

    def update_expense(self, name, category, new_amount):
        for expense in self.expenses:
            if expense.name == name and expense.category == category:
                expense.amount = new_amount
                return True

        return False



