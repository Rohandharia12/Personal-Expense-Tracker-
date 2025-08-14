from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtSql import QSqlError

def init_db(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        print("Database failed to open:", database.lastError().text())
        return False

    query = QSqlQuery()
    if not query.exec("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """):
        print("Table creation failed:", query.lastError().text())
        return False

    return True


def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []

    if query.lastError().isValid():
        print("Fetch error:", query.lastError().text())

    while query.next():
        expenses.append([query.value(i) for i in range(5)])

    return expenses


def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    if not query.exec():
        print("Insert failed:", query.lastError().text())
        return False

    return True


def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)

    if not query.exec():
        print("Delete failed:", query.lastError().text())
        return False

    return True
