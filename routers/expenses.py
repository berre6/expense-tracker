from fastapi import APIRouter, Query, Depends
import database
from utils import get_expense_or_404, expense_to_response
from services.expense_service import (
    create_expense as create_expense_service,
    update_expense as update_expense_service,
    patch_expense as patch_expense_service,
    delete_expense as delete_expense_service,
    get_expenses as get_expenses_service
)

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
    limit: int = Query(default=10, ge=1, le=100),
    session=Depends(database.get_session_dependency)
):
    result = get_expenses_service(
      category=category,
      page=page,
      limit=limit,
      session=session
    )

    expenses = result["items"]
    total = result["total"]
    total_pages = result["total_pages"]

    return {
        "items": [expense_to_response(expense) for expense in expenses],
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
def create_expense(
    expense: ExpenseCreate,
    session=Depends(database.get_session_dependency)
):
    created_expense = create_expense_service(
        expense.name,
        expense.amount,
        expense.category,
        session
    )
    return expense_to_response(created_expense)

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    existing_expense=Depends(get_expense_or_404),
    session=Depends(database.get_session_dependency)
):
    updated_expense = update_expense_service(
        expense_id,
        expense.amount,
        session
    )

    return expense_to_response(updated_expense)


@router.patch("/expenses/{expense_id}", response_model=ExpenseResponse)
def patch_expense(
    expense_id: int,
    expense: ExpensePatch,
    existing_expense=Depends(get_expense_or_404),
    session=Depends(database.get_session_dependency)
):
    updated_expense = patch_expense_service(
      expense_id,
      session,
      expense.name,
      expense.amount,
      expense.category
)

    return expense_to_response(updated_expense)


@router.delete(
    "/expenses/{expense_id}",
    status_code=204
)
def delete_expense(
    expense_id: int,
    expense=Depends(get_expense_or_404),
    session=Depends(database.get_session_dependency)
):
    delete_expense_service(
        expense_id,
        session
    )