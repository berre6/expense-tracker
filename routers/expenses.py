from fastapi import APIRouter, Query, Depends
from math import ceil
import database
from datetime import datetime
from utils import get_expense_or_404, expense_to_response

from schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpensePatch,
    ExpenseListResponse,
    ExpenseResponse
)

router = APIRouter()

@router.get("/expenses", response_model=ExpenseListResponse)
def get_expenses(
    category: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):

    offset = (page - 1) * limit

    expenses = database.get_expenses(
        category=category,
        limit=limit,
        offset=offset
    )

    total = database.get_expense_count(category)
    total_pages = ceil(total / limit)

    return {
        "items": [
            {
                "id": expense[0],
                "name": expense[1],
                "amount": expense[2],
                "category": expense[3],
                "date": expense[4]
            }
            for expense in expenses
        ],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }

@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    expense=Depends(get_expense_or_404)
):
    return expense_to_response(expense)

@router.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=201
)
def create_expense(expense: ExpenseCreate):
    date = datetime.now().strftime("%Y-%m-%d")

    expense_id = database.add_expense(
        expense.name,
        expense.amount,
        expense.category,
        date
    )

    created_expense = database.get_expense_by_id(expense_id)

    return expense_to_response(created_expense)

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    existing_expense=Depends(get_expense_or_404)
):
    database.update_expense(expense_id, expense.amount)

    updated_expense = database.get_expense_by_id(expense_id)

    return expense_to_response(updated_expense)


@router.patch("/expenses/{expense_id}", response_model=ExpenseResponse)
def patch_expense(
    expense_id: int,
    expense: ExpensePatch,
    existing_expense=Depends(get_expense_or_404)
):
    database.patch_expense(
        expense_id,
        expense.name,
        expense.amount,
        expense.category
    )

    updated_expense = database.get_expense_by_id(expense_id)

    return expense_to_response(updated_expense)


@router.delete(
    "/expenses/{expense_id}",
    status_code=204
)
def delete_expense(
    expense_id: int,
    expense=Depends(get_expense_or_404)
):
    database.delete_expense(expense_id)