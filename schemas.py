from pydantic import BaseModel, Field, model_validator


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