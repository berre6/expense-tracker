import database
from datetime import datetime
from math import ceil

def create_expense(name, amount, category, session):

    date = datetime.now().strftime("%Y-%m-%d")

    expense = database.add_expense_model(
        name,
        amount,
        category,
        date,
        session
    )

    return database.get_expense_model_by_id(expense.id, session)


def update_expense(expense_id, amount, session):
    return database.update_expense_model(
        expense_id,
        amount,
        session
    )

def patch_expense(
    expense_id,
    session,
    name=None,
    amount=None,
    category=None
):
    return database.patch_expense_model(
      expense_id,
      name,
      amount,
      category,
      session
)

def delete_expense(expense_id, session):
    return database.delete_expense_model(
        expense_id,
        session
    )

def get_expenses(category=None, page=1, limit=10, session=None):
    offset = (page - 1) * limit

    expenses = database.get_expense_models(
      category=category,
      limit=limit,
      offset=offset,
      session=session
    )

    total = database.get_expense_count_model(
      category=category,
      session=session
    )
    total_pages = ceil(total / limit)

    return {
        "items": expenses,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }