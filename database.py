import sqlite3
DB_PATH = "data/expenses.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_existing_expense(connection, name, category_id):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, amount
        FROM expenses
        WHERE name = ? AND category_id = ?
        """,
        (name, category_id)
    )

    return cursor.fetchone()



def add_expense(name, amount, category, date):
    category_id = get_category_id(category)

    if category_id is None:
      category_id = add_category(category)

    connection = get_connection()
    cursor = connection.cursor()

    existing_expense = get_existing_expense(
      connection,
      name,
      category_id
      )

    if existing_expense:

        new_amount = existing_expense[2] + amount

        cursor.execute(
            """
            UPDATE expenses
            SET amount = ?
            WHERE id = ?
            """,
            (new_amount, existing_expense[0])
        )

    else:

        cursor.execute(
            """
            INSERT INTO expenses (name, amount, category_id, date)
            VALUES (?, ?, ?, ?)
            """,
            (name, amount, category_id, date)
        )

    connection.commit()
    connection.close()

def get_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT expenses.id,
           expenses.name,
           expenses.amount,
           categories.name,
           expenses.date
    FROM expenses
    JOIN categories
    ON expenses.category_id = categories.id
""")
    expenses = cursor.fetchall()

    connection.close()

    return expenses

def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    connection.commit()
    connection.close()


def update_expense(expense_id, new_amount):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
    """
        UPDATE expenses
        SET amount = ?
        WHERE id = ?
    """,
    (new_amount, expense_id)
)
    connection.commit()
    connection.close()


def get_expenses_sorted_by_amount():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT expenses.name,
               expenses.amount,
               categories.name
        FROM expenses
        JOIN categories
        ON expenses.category_id = categories.id
        ORDER BY expenses.amount DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses

def get_category_expenses_sorted_by_amount(category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT expenses.name,
        expenses.amount,
        categories.name
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        WHERE categories.name = ?
        ORDER BY expenses.amount DESC
        """,
        (category,)
    )
    expenses = cursor.fetchall()

    connection.close()

    return expenses


def get_category_counts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT categories.name, COUNT(*) as count
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
        ORDER BY count DESC
        """
    )
    category_counts = cursor.fetchall()
    connection.close()
    return category_counts


def get_category_averages():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT categories.name, AVG(expenses.amount) as average
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
        ORDER BY average DESC"""
    )
    category_averages = cursor.fetchall()
    connection.close()
    return category_averages


def get_categories_sorted_by_total():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT categories.name, SUM(expenses.amount) as total
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
        ORDER BY total DESC """
    )
    categories_sorted_by_total = cursor.fetchall()
    connection.close()
    return categories_sorted_by_total

def get_categories_over_500():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT categories.name, SUM(expenses.amount) as total
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
        HAVING total > 500
        ORDER BY total DESC """
    )
    categories_over_500 = cursor.fetchall()
    connection.close()
    return categories_over_500

def get_categories_with_multiple_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT categories.name, COUNT(*) as count
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
        HAVING count >= 2
        ORDER BY count DESC """
    )
    categories_with_multiple_expenses = cursor.fetchall()
    connection.close()
    return categories_with_multiple_expenses


def add_category(category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO categories (name)
        VALUES (?)
        """,
        (category,)
    )

    category_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return category_id

def get_category_id(category):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id FROM categories 
        WHERE name = ?
        """
    , (category,))
    result = cursor.fetchone()
    connection.close()


    if result is None:
      return None

    return result[0]


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL 
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_categories_name
        ON categories(name)
    """)

    connection.commit()
    connection.close()

create_table()


