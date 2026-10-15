import sqlite3
from datetime import datetime
from config import settings

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
    func
)
from sqlalchemy.orm import (
    DeclarativeBase,
    joinedload,
    relationship,
    sessionmaker
)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String,
        nullable=False
    )

    expenses = relationship(
        "Expense",
        back_populates="category"
    )


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String,
        nullable=False
    )

    amount = Column(
        Integer,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="expenses"
    )

    date = Column(
        String,
        nullable=False
    )



DB_PATH = settings.database_path


def create_db_engine(database_url: str):
    return create_engine(database_url)


engine = create_db_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_session():
    return SessionLocal()

def get_session_dependency():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()



def init_db(db_engine=None):
    if db_engine is None:
        db_engine = engine

    Base.metadata.create_all(db_engine)



def create_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_categories_name
        ON categories(name)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (category_id)
            REFERENCES categories(id)
        )
    """)

    connection.commit()
    connection.close()


def add_category(name):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (name,)
    )

    category_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return category_id


def get_category_by_name(name):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM categories WHERE name = ?",
        (name,)
    )

    category = cursor.fetchone()

    connection.close()

    return category


def add_expense(name, amount, category, date):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM categories WHERE name = ?",
        (category,)
    )

    category_row = cursor.fetchone()

    if category_row is None:
        cursor.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category,)
        )

        category_id = cursor.lastrowid

    else:
        category_id = category_row[0]

    cursor.execute(
        """
        SELECT id, amount
        FROM expenses
        WHERE name = ?
        AND category_id = ?
        """,
        (name, category_id)
    )

    existing_expense = cursor.fetchone()

    if existing_expense is not None:
        expense_id = existing_expense[0]
        new_amount = existing_expense[1] + amount

        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?
            WHERE id = ?
            """,
            (new_amount, expense_id)
        )

    else:
        cursor.execute(
            """
            INSERT INTO expenses
            (name, amount, category_id, date)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                amount,
                category_id,
                date
            )
        )

        expense_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return expense_id


def add_expense_model(name, amount, category, date, session):
    try:
        statement = select(Category).where(Category.name == category)

        result = session.execute(statement)
        category_model = result.scalar_one_or_none()

        if category_model is None:
            category_model = Category(name=category)
            session.add(category_model)
            session.flush()

        statement = select(Expense).where(
            Expense.name == name,
            Expense.category_id == category_model.id
        )

        result = session.execute(statement)
        existing_expense = result.scalar_one_or_none()

        if existing_expense is not None:
            existing_expense.amount += amount
            expense = existing_expense
        else:
            expense = Expense(
                name=name,
                amount=amount,
                category_id=category_model.id,
                date=date
            )
            session.add(expense)
            session.flush()

        session.commit()
        return expense

    except Exception:
        session.rollback()
        raise

def update_expense_model(expense_id, amount, session):
    try:
        statement = select(Expense).where(Expense.id == expense_id)

        result = session.execute(statement)
        expense = result.scalar_one_or_none()

        if expense is not None:
            expense.amount = amount

        session.commit()
        return expense

    except Exception:
        session.rollback()
        raise

def patch_expense_model(
    expense_id,
    name=None,
    amount=None,
    category=None,
    session=None
):
    try:
        statement = select(Expense).where(Expense.id == expense_id)

        result = session.execute(statement)
        expense = result.scalar_one_or_none()

        if expense is not None:
            if name is not None:
                expense.name = name

            if amount is not None:
                expense.amount = amount

            if category is not None:
                statement = select(Category).where(
                    Category.name == category
                )

                result = session.execute(statement)
                category_model = result.scalar_one_or_none()

                if category_model is None:
                    category_model = Category(name=category)
                    session.add(category_model)
                    session.flush()

                expense.category_id = category_model.id

        session.commit()
        return expense

    except Exception:
        session.rollback()
        raise

def get_expense_by_id(expense_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.id,
            expenses.name,
            expenses.amount,
            categories.name AS category,
            expenses.date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.id
        WHERE expenses.id = ?
        """,
        (expense_id,)
    )

    expense = cursor.fetchone()

    connection.close()

    return expense

def get_expense_model_by_id(expense_id, session):
   

    statement = (
        select(Expense)
        .options(joinedload(Expense.category))
        .where(Expense.id == expense_id)
    )

    expense = session.execute(statement).scalar_one_or_none()

    return expense


def get_expenses(
    category=None,
    limit=10,
    offset=0
):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    if category:
        cursor.execute(
            """
            SELECT
                expenses.id,
                expenses.name,
                expenses.amount,
                categories.name AS category,
                expenses.date
            FROM expenses
            JOIN categories
                ON expenses.category_id = categories.id
            WHERE categories.name = ?
            ORDER BY expenses.id DESC
            LIMIT ? OFFSET ?
            """,
            (category, limit, offset)
        )
    else:
        cursor.execute(
            """
            SELECT
                expenses.id,
                expenses.name,
                expenses.amount,
                categories.name AS category,
                expenses.date
            FROM expenses
            JOIN categories
                ON expenses.category_id = categories.id
            ORDER BY expenses.id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )

    expenses = cursor.fetchall()

    connection.close()

    return expenses

def get_expense_models(session, category=None, limit=10, offset=0):
    statement = (
        select(Expense)
        .options(joinedload(Expense.category))
        .order_by(Expense.id.desc())
        .limit(limit)
        .offset(offset)
    )

    if category:
        statement = (
            statement
            .join(Expense.category)
            .where(Category.name == category)
        )

    expenses = session.execute(statement).scalars().all()

    return expenses


def get_expense_count(category=None):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if category:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM expenses
            JOIN categories
                ON expenses.category_id = categories.id
            WHERE categories.name = ?
            """,
            (category,)
        )

    else:
        cursor.execute(
            "SELECT COUNT(*) FROM expenses"
        )

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_expense_count_model(category=None, session=None):
    statement = select(func.count()).select_from(Expense)

    if category:
        statement = (
            statement
            .join(Expense.category)
            .where(Category.name == category)
        )

    count = session.execute(statement).scalar_one()

    return count


def update_expense(expense_id, amount):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET amount = ?
        WHERE id = ?
        """,
        (
            amount,
            expense_id
        )
    )

    connection.commit()
    connection.close()


def patch_expense(
    expense_id,
    name=None,
    amount=None,
    category=None
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if name is not None:
        cursor.execute(
            """
            UPDATE expenses
            SET name = ?
            WHERE id = ?
            """,
            (
                name,
                expense_id
            )
        )

    if amount is not None:
        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?
            WHERE id = ?
            """,
            (
                amount,
                expense_id
            )
        )

    if category is not None:
        cursor.execute(
            "SELECT id FROM categories WHERE name = ?",
            (category,)
        )

        category_row = cursor.fetchone()

        if category_row is None:
            cursor.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (category,)
            )

            category_id = cursor.lastrowid

        else:
            category_id = category_row[0]

        cursor.execute(
            """
            UPDATE expenses
            SET category_id = ?
            WHERE id = ?
            """,
            (
                category_id,
                expense_id
            )
        )

    connection.commit()
    connection.close()


def delete_expense(expense_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()

def delete_expense_model(expense_id, session):
    try:
        statement = select(Expense).where(Expense.id == expense_id)

        result = session.execute(statement)
        expense = result.scalar_one_or_none()

        if expense is not None:
            session.delete(expense)
            session.commit()

        return expense

    except Exception:
        session.rollback()
        raise

def get_total_expenses():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total or 0


def get_expenses_by_category(category):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.id,
            expenses.name,
            expenses.amount,
            categories.name AS category,
            expenses.date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.id
        WHERE categories.name = ?
        ORDER BY expenses.id DESC
        """,
        (category,)
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_expenses_sorted_by_amount():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.id,
            expenses.name,
            expenses.amount,
            categories.name AS category,
            expenses.date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.id
        ORDER BY expenses.amount DESC
        """
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_category_expenses_sorted_by_amount(category):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.id,
            expenses.name,
            expenses.amount,
            categories.name AS category,
            expenses.date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.id
        WHERE categories.name = ?
        ORDER BY expenses.amount DESC
        """,
        (category,)
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_expenses_by_date(date):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.id,
            expenses.name,
            expenses.amount,
            categories.name AS category,
            expenses.date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.id
        WHERE expenses.date = ?
        ORDER BY expenses.id DESC
        """,
        (date,)
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_expenses_between_dates(start_date, end_date):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            expenses.id,
            expenses.name,
            expenses.amount,
            categories.name AS category,
            expenses.date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.id
        WHERE expenses.date BETWEEN ? AND ?
        ORDER BY expenses.date ASC
        """,
        (
            start_date,
            end_date
        )
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses
