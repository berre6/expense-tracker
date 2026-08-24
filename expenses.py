def add_expense(expenses, name, amount, category):
    for expense in expenses:
        if expense["name"] == name and expense["category"] == category:
            expense["amount"] += amount
            return

    expenses.append({
        "name": name,
        "category": category,
        "amount": amount
    })


def calculate_total(expenses):
    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total


def show_expenses(expenses):
    if not expenses:
        print("Harcama yok.")
        return

    for expense in expenses:
        print(
            f"Name: {expense['name']}, "
            f"Category: {expense['category']}, "
            f"Amount: {expense['amount']}"
        )


def get_by_category(expenses, category):
    filtered_expenses = []

    for expense in expenses:
        if expense["category"] == category:
            filtered_expenses.append(expense)

    return filtered_expenses