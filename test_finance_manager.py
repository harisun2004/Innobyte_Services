import unittest
import sqlite3
from finance_manager import hash_password, add_transaction, set_budget, check_budget, generate_report

class TestFinanceManager(unittest.TestCase):
    
    def setUp(self):
        # Set up a temporary in-memory SQLite database for testing
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY,
            amount REAL,
            category TEXT,
            type TEXT,
            date TEXT
        )''')
        self.cursor.execute('''
        CREATE TABLE budgets (
            id INTEGER PRIMARY KEY,
            category TEXT,
            budget REAL,
            month TEXT,
            year TEXT
        )''')

    def test_hash_password(self):
        password = "secure123"
        hashed = hash_password(password)
        self.assertEqual(len(hashed), 64)  # SHA256 hash length is 64 chars

    def test_add_transaction(self):
        # Add a test transaction
        add_transaction()
        self.cursor.execute("SELECT * FROM transactions")
        transactions = self.cursor.fetchall()
        self.assertEqual(len(transactions), 1)

    def test_set_budget(self):
        set_budget()
        self.cursor.execute("SELECT * FROM budgets")
        budgets = self.cursor.fetchall()
        self.assertGreater(len(budgets), 0)

    def tearDown(self):
        # Close the in-memory database
        self.conn.close()

if __name__ == "__main__":
    unittest.main()
