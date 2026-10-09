from fastapi import HTTPException, Depends

import database


def expense_to_response(expense):
    return {
        "id": expense.id,
        "name": expense.name,
        "amount": expense.amount,
        "category": expense.category.name,
        "date": expense.date
    }


def get_expense_or_404(
    expense_id: int,
    session=Depends(database.get_session_dependency)
):
    expense = database.get_expense_model_by_id(expense_id, session)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense