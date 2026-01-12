
-- ============================================
-- Personal Finance Tracker Database (SQLite)
-- ============================================

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category_id INTEGER,
    amount REAL NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('income', 'expense')),
    transaction_date DATE,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT INTO users (name, email) VALUES ('Sanjay', 'sanjay@email.com');

INSERT INTO categories (category_name) VALUES
('Food'),
('Rent'),
('Travel'),
('Entertainment'),
('Salary');

INSERT INTO transactions (user_id, category_id, amount, transaction_type, transaction_date, description)
VALUES
(1, 5, 40000, 'income', '2025-01-01', 'Monthly Salary'),
(1, 1, 3000, 'expense', '2025-01-05', 'Groceries'),
(1, 2, 12000, 'expense', '2025-01-06', 'House Rent'),
(1, 3, 1500, 'expense', '2025-01-10', 'Travel'),
(1, 4, 2000, 'expense', '2025-01-15', 'Movies');

SELECT SUM(amount) AS total_income
FROM transactions
WHERE transaction_type = 'income';

SELECT SUM(amount) AS total_expense
FROM transactions
WHERE transaction_type = 'expense';

SELECT c.category_name, SUM(t.amount) AS total_spent
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.transaction_type = 'expense'
GROUP BY c.category_name
ORDER BY total_spent DESC;

SELECT
    (SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income') -
    (SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense')
    AS remaining_balance;
