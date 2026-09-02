from expense_tracker_oop import ExpenseTracker,Expense
import pytest

@pytest.fixture
def tracker():
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


def test_expense_conversion():
    expense = Expense("Kahve", 80, "Food")
    expense_dict = expense.to_dict()
    assert expense_dict == {"name": "Kahve", "amount": 80, "category": "Food", "date": expense.date.isoformat()}
    new_expense = Expense.from_dict(expense_dict)
    assert new_expense.name == "Kahve"
    assert new_expense.amount == 80
    assert new_expense.category == "Food"



