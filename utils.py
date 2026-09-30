from fastapi import HTTPException

import database


def expense_to_response(expense):
    return {
        "id": expense["id"],
        "name": expense["name"],
        "amount": expense["amount"],
        "category": expense["category"],
        "date": expense["date"]
    }


def get_expense_or_404(expense_id: int):
    expense = database.get_expense_by_id(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense