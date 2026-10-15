from expense_tracker_oop import ExpenseTracker,Expense
import pytest
import database
from fastapi.testclient import TestClient
from api import create_app

app = create_app(initialize_db=False)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.expense_service import patch_expense
from services.expense_service import delete_expense

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_get_expenses():
    
   connection = database.get_connection()
   cursor = connection.cursor()

   cursor.execute("DELETE FROM expenses")

   connection.commit()
   connection.close()
   database.add_expense(
    "Test Kahve",
    100,
    "Food",
    "2026-09-11"
)
   response = client.get("/expenses")

   assert response.status_code == 200
   data = response.json()

   assert isinstance(data, dict)
   assert isinstance(data["items"], list)
   assert data["items"][0]["name"] == "Test Kahve"
   assert data["page"] == 1
   assert data["limit"] == 10
   assert data["total"] == 1

def test_get_expense():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")

    connection.commit()
    connection.close()

    expense_id = database.add_expense(
        "Test Yemek",
        150,
        "Food",
        "2026-09-11"
    )
    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Test Yemek"
    assert response.json()["amount"] == 150

def test_get_nonexistent_expense():
    response = client.get("/expenses/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_create_expense():
    response = client.post(
        "/expenses",
        json={
            "name": "Test Kitap",
            "amount": 200,
            "category": "Education"
        }
    )

    assert response.status_code == 201

    data = response.json()
    expense_id = data["id"]
    saved_expense = database.get_expense_by_id(expense_id)
    assert saved_expense is not None
    assert saved_expense[1] == "Test Kitap"
    assert saved_expense[2] == 200

   
    assert data["name"] == "Test Kitap"
    assert data["amount"] == 200
    assert data["category"] == "Education"

def test_create_expense_invalid_amount():
        response = client.post(
            "/expenses",
            json={
                "name": "Test",
                "amount": -100,
                "category": "Food"
            }
        )

        assert response.status_code == 422



def test_create_expense_invalid_name():
    response = client.post(
        "/expenses",
        json={
            "name": "",
            "amount": 100,
            "category": "Food"
        }
    )

    assert response.status_code == 422

def test_create_expense_whitespace_name():
    response = client.post(
        "/expenses",
        json={
            "name": "   ",
            "amount": 100,
            "category": "Food"
        }
    )

    assert response.status_code == 422


def test_create_expense_whitespace_category():
    response = client.post(
        "/expenses",
        json={
            "name": "Test",
            "amount": 100,
            "category": "   "
        }
    )

    assert response.status_code == 422

def test_api_patch_whitespace_name():
    expense_id = database.add_expense(
        "Patch Test",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.patch(
        f"/expenses/{expense_id}",
        json={"name": "   "}
    )

    assert response.status_code == 422


def test_api_patch_whitespace_category():
    expense_id = database.add_expense(
        "Patch Test",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.patch(
        f"/expenses/{expense_id}",
        json={"category": "   "}
    )

    assert response.status_code == 422

def test_api_delete_expense():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")

    connection.commit()
    connection.close()

    expense_id = database.add_expense(
        "Silinecek Test",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 204

    deleted_expense = database.get_expense_by_id(expense_id)

    assert deleted_expense is None


def test_get_expense_count_model(session):
    database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    database.add_expense_model(
        "Ekmek",
        20,
        "Market",
        "2026-10-07",
        session
    )

    total = database.get_expense_count_model(
        session=session
    )

    food_total = database.get_expense_count_model(
        category="Yemek",
        session=session
    )

    assert total == 2
    assert food_total == 1


def test_api_update_expense():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")

    connection.commit()
    connection.close()

    expense_id = database.add_expense(
        "Güncellenecek Test",
        100,
        "Food",
        "2026-09-11"
    )
    response = client.put(
    f"/expenses/{expense_id}",
    json={
        "amount": 250
    }
)
    assert response.status_code == 200
    data = response.json()

    assert data["amount"] == 250

    updated_expense = database.get_expense_by_id(expense_id)

    assert updated_expense is not None
    assert updated_expense[2] == 250


def test_api_update_nonexistent_expense():
    response = client.put(
        "/expenses/999999",
        json={
            "amount": 250
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_api_patch_expense():
    expense_id = database.add_expense(
        "Patch Test",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.patch(
        f"/expenses/{expense_id}",
        json={
            "amount": 250
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["name"] == "Patch Test"
    assert data["amount"] == 250
    assert data["category"] == "Food"
    assert data["date"] == "2026-09-11"


def test_api_patch_nonexistent_expense():
    response = client.patch(
        "/expenses/999999",
        json={
            "amount": 250
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_api_patch_multiple_fields():
    expense_id = database.add_expense(
        "Eski İsim",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.patch(
        f"/expenses/{expense_id}",
        json={
            "name": "Yeni İsim",
            "amount": 300,
            "category": "Transport"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["name"] == "Yeni İsim"
    assert data["amount"] == 300
    assert data["category"] == "Transport"
    assert data["date"] == "2026-09-11"


def test_api_patch_empty_body():
    expense_id = database.add_expense(
        "Empty Patch Test",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.patch(
        f"/expenses/{expense_id}",
        json={}
    )

    assert response.status_code == 422

def test_api_patch_invalid_amount():
    expense_id = database.add_expense(
        "Invalid Patch Test",
        100,
        "Food",
        "2026-09-11"
    )

    response = client.patch(
        f"/expenses/{expense_id}",
        json={
            "amount": -100
        }
    )

    assert response.status_code == 422


def test_get_expenses_pagination():
    for i in range(5):
        database.add_expense(
            f"Pagination Test {i}",
            100 + i,
            "Pagination",
            "2026-09-11"
        )

    response = client.get("/expenses?page=1&limit=2")

    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 5
    assert data["total_pages"] == 3



def test_get_expenses_second_page():
    for i in range(5):
        database.add_expense(
            f"Second Page Test {i}",
            200 + i,
            "Pagination",
            "2026-09-11"
        )

    first_page = client.get("/expenses?page=1&limit=2")
    second_page = client.get("/expenses?page=2&limit=2")

    assert first_page.status_code == 200
    assert second_page.status_code == 200

    first_data = first_page.json()
    second_data = second_page.json()

    assert len(first_data["items"]) == 2
    assert len(second_data["items"]) == 2
    assert first_data["items"] != second_data["items"]
    assert first_data["page"] == 1
    assert second_data["page"] == 2
    assert first_data["total"] == 5
    assert second_data["total_pages"] == 3


def test_get_expense_count_by_category():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")
    connection.commit()
    connection.close()

    database.add_expense(
        "Kahve",
        80,
        "Food",
        "2026-09-11"
    )

    database.add_expense(
        "Yemek",
        120,
        "Food",
        "2026-09-11"
    )

    database.add_expense(
        "Otobüs",
        50,
        "Transport",
        "2026-09-11"
    )

    assert database.get_expense_count("Food") == 2
    assert database.get_expense_count("Transport") == 1

def test_get_expenses_invalid_page():
    response = client.get("/expenses?page=0")

    assert response.status_code == 422

def test_get_expenses_invalid_limit_too_low():
    response = client.get("/expenses?limit=0")

    assert response.status_code == 422


def test_get_expenses_invalid_limit_too_high():
    response = client.get("/expenses?limit=101")

    assert response.status_code == 422

def test_get_expense_count():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")
    connection.commit()
    connection.close()

    database.add_expense(
        "Kahve",
        80,
        "Food",
        "2026-09-11"
    )

    database.add_expense(
        "Yemek",
        120,
        "Food",
        "2026-09-11"
    )

    assert database.get_expense_count() == 2

def test_get_expenses_category_filter():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")
    connection.commit()
    connection.close()

    database.add_expense("Kahve", 80, "Food", "2026-09-11")
    database.add_expense("Yemek", 120, "Food", "2026-09-11")
    database.add_expense("Otobüs", 50, "Transport", "2026-09-11")

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["total"] == 2
    assert data["items"][0]["category"] == "Food"
    assert data["items"][1]["category"] == "Food"

def test_get_expenses_total_pages():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")
    connection.commit()
    connection.close()

    for i in range(25):
        database.add_expense(
            f"Test {i}",
            100,
            "Food",
            "2026-09-11"
        )

    response = client.get("/expenses?page=1&limit=10")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] == 25
    assert data["total_pages"] == 3

def test_get_expense_not_found():
    response = client.get("/expenses/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Expense not found"
    }


database.DB_PATH = "data/test_expenses.db"

test_engine = create_engine("sqlite:///data/test_expenses.db")
database.Base.metadata.create_all(test_engine)

database.SessionLocal = sessionmaker(bind=test_engine)

database.engine = test_engine


def override_get_session():
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[database.get_session_dependency] = override_get_session


@pytest.fixture(autouse=True)
def clean_test_database():
    with database.SessionLocal() as session:
        session.execute(database.Expense.__table__.delete())
        session.execute(database.Category.__table__.delete())
        session.commit()

@pytest.fixture
def session():
    db_session = database.get_session()

    try:
        yield db_session
    finally:
        db_session.close()



@pytest.fixture
def tracker():
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses")
    connection.commit()
    connection.close()

    tracker = ExpenseTracker()
    tracker.expenses = []
    return tracker


def test_calculate_total(tracker):

    

    tracker.add_expense("Kahve", 80, "Food")
    tracker.add_expense("Yemek", 120, "Food")
    tracker.add_expense("Ulaşım", 50, "Transport")

    assert tracker.calculate_total() == 250


def test_add_expense(tracker):
    tracker.add_expense("Kahve", 80, "Food")
    tracker.add_expense("Kahve", 30, "Food")

    assert len(tracker.expenses) == 1
    assert tracker.expenses[0].amount == 110


def test_delete_expense(tracker):
    tracker.add_expense("Kitap", 50, "Education")
    tracker.delete_expense("Kitap","Education")
    assert tracker.expenses == []


def test_delete_nonexistent_expense(tracker):
    tracker.add_expense("Kitap", 50, "Education")
    result =  tracker.delete_expense("Kahve", "Food")
    assert result == False


def test_update_expense(tracker):
    tracker.add_expense("Kitap", 50, "Education")
    result = tracker.update_expense("Kitap", "Education", 100)
    assert result == True
    assert tracker.expenses[0].amount == 100


def test_update_nonexistent_expense(tracker):
    tracker.add_expense("Kitap", 50, "Education")
    result = tracker.update_expense("Kahve", "Food", 100)
    assert result == False


def test_get_by_category(tracker):
    tracker.add_expense("Kahve", 80, "Food")
    tracker.add_expense("Yemek", 120, "Food")
    tracker.add_expense("Ulaşım", 50, "Transport")
    result = tracker.get_by_category("Food")
    assert len(result) == 2
    assert result[0].name == "Kahve"
    assert result[1].name == "Yemek"


def test_get_by_nonexistent_category(tracker):
    tracker.add_expense("Kahve", 80, "Food")
    result = tracker.get_by_category("Gaming")
    assert result == []


def test_calculate_category_total(tracker):
    tracker.add_expense("Kahve", 80, "Food")
    tracker.add_expense("Yemek", 120, "Food")
    tracker.add_expense("Ulaşım", 50, "Transport")
    result = tracker.calculate_category_total("Food")
    assert result == 200


def test_calculate_nonexistent_category_total(tracker):
    tracker.add_expense("Kahve", 80, "Food")
    result = tracker.calculate_category_total("Gaming")
    assert result == 0

def test_add_expense_model(session):
    database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    database.add_expense_model(
        "Ekmek",
        20,
        "Market",
        "2026-10-07",
        session
    )

    total = database.get_expense_count_model(
        session=session
    )

    assert total == 2


def test_update_expense_model(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    updated_expense = database.update_expense_model(
        expense.id,
        100,
        session
    )

    assert updated_expense.id == expense.id
    assert updated_expense.amount == 100


def test_patch_expense_model(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    patched_expense = database.patch_expense_model(
        expense.id,
        name="Latte",
        amount=80,
        category="İçecek",
        session=session
    )

    assert patched_expense.id == expense.id
    assert patched_expense.name == "Latte"
    assert patched_expense.amount == 80
    assert patched_expense.category.name == "İçecek"


def test_patch_expense_model_partial(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    patched_expense = database.patch_expense_model(
        expense.id,
        name="Latte",
        session=session
    )

    assert patched_expense.id == expense.id
    assert patched_expense.name == "Latte"
    assert patched_expense.amount == 50
    assert patched_expense.category.name == "Yemek"

def test_patch_expense_service_sqlalchemy(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    patched_expense = patch_expense(
        expense.id,
        session,
        amount=100
    )

    assert patched_expense.id == expense.id
    assert patched_expense.amount == 100
    assert patched_expense.name == "Kahve"
    assert patched_expense.category.name == "Yemek"


def test_patch_expense_model_amount_only(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    patched_expense = database.patch_expense_model(
        expense.id,
        amount=100,
        session=session
    )

    assert patched_expense.id == expense.id
    assert patched_expense.name == "Kahve"
    assert patched_expense.amount == 100
    assert patched_expense.category.name == "Yemek"

def test_patch_expense_model_category_only(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    patched_expense = database.patch_expense_model(
        expense.id,
        category="İçecek",
        session=session
    )

    assert patched_expense.id == expense.id
    assert patched_expense.name == "Kahve"
    assert patched_expense.amount == 50
    assert patched_expense.category.name == "İçecek"


def test_delete_expense_model(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    deleted_expense = database.delete_expense_model(
        expense.id,
        session
    )

    assert deleted_expense.id == expense.id

    remaining_expense = database.get_expense_model_by_id(
        expense.id,
        session
    )

    assert remaining_expense is None


def test_create_expense_success():
    response = client.post(
        "/expenses",
        json={
            "name": "API Kahve",
            "amount": 40,
            "category": "API Test"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "API Kahve"
    assert response.json()["amount"] == 40
    assert response.json()["category"] == "API Test"


def test_delete_expense_service(session):
    expense = database.add_expense_model(
        "Kahve",
        50,
        "Yemek",
        "2026-10-07",
        session
    )

    deleted_expense = delete_expense(
        expense.id,
        session
    )

    assert deleted_expense.id == expense.id

    remaining_expense = database.get_expense_model_by_id(
        expense.id,
        session
    )

    assert remaining_expense is None

def test_add_expense_model_rolls_back_on_error(session, monkeypatch):
    def raise_error(*args, **kwargs):
        raise RuntimeError("Database error")

    monkeypatch.setattr(session, "commit", raise_error)

    with pytest.raises(RuntimeError, match="Database error"):
        database.add_expense_model(
            "Kahve",
            50,
            "Yemek",
            "2026-10-07",
            session
        )

    assert session.is_active


