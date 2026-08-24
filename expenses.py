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

def calculate_category_total(expenses, category):
    total = 0
    for expense in expenses:
        if expense["category"] == category:
            total += expense["amount"]
    return total

def delete_expense(expenses, name, category):
    for expense in expenses:
        if expense["name"] == name and expense["category"] == category:
            expenses.remove(expense)
            return True
    return False

def update_expense(expenses, name, category, new_amount):
    for expense in expenses:
        if expense["name"] == name and expense["category"] == category:
           expense["amount"] = new_amount
           return True

    return False