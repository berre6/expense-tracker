from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, model_validator
import database
from datetime import datetime
from math import ceil

class ExpenseCreate(BaseModel):
    name: str = Field(min_length=1)
    amount: int = Field(gt=0)
    category: str

class ExpenseUpdate(BaseModel):
    amount: int

class ExpensePatch(BaseModel):

    name: str | None = None
    amount: int | None = Field(default=None, gt=0)
    category: str | None = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.name is None and self.amount is None and self.category is None:
            raise ValueError("At least one field must be provided")

        return self

class ExpenseResponse(BaseModel):
    id: int
    name: str
    amount: int
    category: str
    date: str

class ExpenseListResponse(BaseModel):
    items: list[ExpenseResponse]
    page: int
    limit: int
    total: int
    total_pages: int

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

app = FastAPI()

@app.get("/")

def home():
    return {"message": "Hello"}

@app.get("/expenses", response_model=ExpenseListResponse)
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

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    expense=Depends(get_expense_or_404)
):
    return expense_to_response(expense)

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    existing_expense=Depends(get_expense_or_404)
):

    database.update_expense(expense_id, expense.amount)

    updated_expense = database.get_expense_by_id(expense_id)

    return expense_to_response(updated_expense)

@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    expense=Depends(get_expense_or_404)
):
    database.delete_expense(expense_id)

@app.patch("/expenses/{expense_id}", response_model=ExpenseResponse)
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


@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
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

    return {
        "id": created_expense[0],
        "name": created_expense[1],
        "amount": created_expense[2],
        "category": created_expense[3],
        "date": created_expense[4]
    }
