# Expense Tracker API

A RESTful expense tracking application built with Python, FastAPI, and SQLAlchemy. The project supports expense management, category-based filtering, pagination, and data validation using a SQLite database.

## Features

- Create, retrieve, update, partially update, and delete expenses
- Organize expenses by category
- Filter expenses by category
- Paginate expense lists
- Validate request data and reject invalid inputs
- Return appropriate HTTP status codes for successful requests and errors
- Persist data in SQLite
- Use SQLAlchemy ORM for database operations
- Test API endpoints and application logic with pytest

## Tech Stack

- **Python**
- **FastAPI** — REST API development
- **SQLAlchemy** — ORM and database operations
- **SQLite** — relational data storage
- **Pydantic** — request validation and response schemas
- **Pytest** — automated testing

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| POST | `/expenses` | Create an expense |
| GET | `/expenses` | List expenses |
| GET | `/expenses/{expense_id}` | Retrieve one expense |
| PUT | `/expenses/{expense_id}` | Update an expense amount |
| PATCH | `/expenses/{expense_id}` | Partially update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |

### Filtering and Pagination

The expense list endpoint supports category filtering and pagination.

Example:

`GET /expenses?category=Food&page=1&limit=10`

Pagination parameters:
- `page`: page number, starting at 1
- `limit`: number of items per page, between 1 and 100

The response includes the items, current page, page size, total item count, and total page count.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/berre6/expense-tracker.git
cd expense-tracker
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn api:app --reload
```

Once the server starts, open `http://127.0.0.1:8000/docs` to explore and test the API through the interactive Swagger UI.

## Running Tests

Run the automated test suite with:

```bash
pytest -q
```

The current test suite covers API endpoints, validation errors, pagination, category filtering, and application/database operations.

## What I Learned

Through this project, I practiced:

- Designing RESTful API endpoints
- Separating API routes, business logic, and database operations
- Using SQLAlchemy ORM with SQLite
- Validating request data with Pydantic
- Handling HTTP errors and status codes
- Writing automated tests with pytest
- Using Git to track development progress

## Future Improvements

- Add authentication and user-specific expenses
- Improve configuration and database session management
- Add more comprehensive API tests
- Deploy the API to a hosting platform
