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

def get_valid_amount():
    while True:
        try:
            amount = int(input("Harcama miktarını giriniz: "))

            if amount <= 0:
                print("0'dan büyük bir sayı giriniz.")
                continue

            return amount

        except ValueError:
            print("Geçerli bir sayı giriniz.")


def get_valid_choice():
    while True:
        try:
            seçim = int(input("Seçiminizi yapın (1-8): "))

            if seçim < 1 or seçim > 8:
                print("1 ile 8 arasında bir seçim yapın.")
                continue

            return seçim

        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
        


    