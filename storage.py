import json
from pathlib import Path

file_path = Path("data") / "expenses.json"
file_path.parent.mkdir(exist_ok=True)


def save_expenses(expenses):
    data = []

    for expense in expenses:
        data.append(expense.to_dict())

    with open(file_path, "w") as file:
        json.dump(data, file)


def load_expenses():
    try:
        with open(file_path, "r") as file:
            expenses = json.load(file)
            return expenses

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []