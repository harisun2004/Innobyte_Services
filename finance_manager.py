import sqlite3
import hashlib
import shutil

# Connect to SQLite database (it will create one if it doesn't exist)
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Create necessary tables if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    amount REAL,
    category TEXT,
    type TEXT,
    date TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY,
    category TEXT,
    budget REAL,
    month TEXT,
    year TEXT
)
''')


# Hash the password before storing it for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function to register user
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try again with a different username.")


# Function to authenticate user during login
def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()

    if user:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False


# Function to add a transaction
def add_transaction():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    transaction_type = input("Enter type (income/expense): ").lower()
    date = input("Enter date (YYYY-MM-DD): ")

    cursor.execute("INSERT INTO transactions (amount, category, type, date) VALUES (?, ?, ?, ?)",
                   (amount, category, transaction_type, date))
    conn.commit()
    print("Transaction added successfully!")


# Function to update a transaction
def update_transaction():
    transaction_id = int(input("Enter transaction ID to update: "))
    amount = float(input("Enter new amount: "))
    category = input("Enter new category: ")
    transaction_type = input("Enter new type (income/expense): ").lower()
    date = input("Enter new date (YYYY-MM-DD): ")

    cursor.execute("UPDATE transactions SET amount = ?, category = ?, type = ?, date = ? WHERE id = ?",
                   (amount, category, transaction_type, date, transaction_id))
    conn.commit()
    print("Transaction updated successfully!")


# Function to delete a transaction
def delete_transaction():
    transaction_id = int(input("Enter transaction ID to delete: "))
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    print("Transaction deleted successfully!")


# Function to generate monthly or yearly financial report
def generate_report():
    choice = input("Generate monthly (M) or yearly (Y) report? ").lower()
    if choice == 'm':
        month = input("Enter month (MM): ")
        year = input("Enter year (YYYY): ")
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month, year))
        income = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ? AND type = 'expense'", (month, year))
        expense = cursor.fetchone()[0] or 0
        net_savings = income - expense
        print(f"Monthly Report for {month}/{year}:")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expense: ${expense:.2f}")
        print(f"Net Savings: ${net_savings:.2f}")
    elif choice == 'y':
        year = input("Enter year (YYYY): ")
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE strftime('%Y', date) = ?", (year,))
        income = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE strftime('%Y', date) = ? AND type = 'expense'", (year,))
        expense = cursor.fetchone()[0] or 0
        net_savings = income - expense
        print(f"Yearly Report for {year}:")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expense: ${expense:.2f}")
        print(f"Net Savings: ${net_savings:.2f}")


# Function to set budget for a category
def set_budget():
    category = input("Enter category: ")
    budget = float(input("Enter budget amount: "))
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    cursor.execute("INSERT INTO budgets (category, budget, month, year) VALUES (?, ?, ?, ?)",
                   (category, budget, month, year))
    conn.commit()
    print(f"Budget for {category} set successfully!")


# Function to check if the user has exceeded their budget
def check_budget():
    category = input("Enter category: ")
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    cursor.execute("SELECT budget FROM budgets WHERE category = ? AND month = ? AND year = ?", (category, month, year))
    budget = cursor.fetchone()
    if budget:
        budget = budget[0]
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ? AND type = 'expense'", (category, month, year))
        total_expense = cursor.fetchone()[0] or 0
        if total_expense > budget:
            print(f"You have exceeded your budget of ${budget} for {category}. Total expense: ${total_expense:.2f}")
        else:
            print(f"You are within your budget for {category}. Total expense: ${total_expense:.2f}")
    else:
        print(f"No budget set for {category} in {month}/{year}.")


# Function to back up the database
def backup_database():
    shutil.copy('finance_manager.db', 'finance_manager_backup.db')
    print("Database backed up successfully!")


# Function to restore the database from backup
def restore_database():
    shutil.copy('finance_manager_backup.db', 'finance_manager.db')
    print("Database restored successfully!")


# Main menu
def main():
    while True:
        print("\nPersonal Finance Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        action = input("Choose an option: ")

        if action == '1':
            register_user()
        elif action == '2':
            if login_user():
                while True:
                    print("\n1. Add Transaction")
                    print("2. Update Transaction")
                    print("3. Delete Transaction")
                    print("4. Generate Monthly Report")
                    print("5. Generate Yearly Report")
                    print("6. Set Budget")
                    print("7. Check Budget")
                    print("8. Backup Database")
                    print("9. Restore Database")
                    print("10. Logout")
                    choice = input("Choose an action: ")

                    if choice == '1':
                        add_transaction()
                    elif choice == '2':
                        update_transaction()
                    elif choice == '3':
                        delete_transaction()
                    elif choice == '4':
                        generate_report()
                    elif choice == '5':
                        generate_report()
                    elif choice == '6':
                        set_budget()
                    elif choice == '7':
                        check_budget()
                    elif choice == '8':
                        backup_database()
                    elif choice == '9':
                        restore_database()
                    elif choice == '10':
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif action == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
