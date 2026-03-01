CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    account_type TEXT NOT NULL,
    current_value REAL NOT NULL DEFAULT 0.0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS current_holdings (
    account_id TEXT NOT NULL,
    ticker TEXT NOT NULL,
    type TEXT NOT NULL, -- e.g., Stock, Bond, Mutual Fund
    description TEXT,
    quantity REAL NOT NULL DEFAULT 0.0,
    market_value REAL NOT NULL DEFAULT 0.0,
    cost_basis REAL NOT NULL DEFAULT 0.0,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (account_id, ticker),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS monthly_statements (
    monthly_statement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT NOT NULL,
    statement_date DATE NOT NULL,
    beginning_value REAL NOT NULL DEFAULT 0.0,
    ending_value REAL NOT NULL DEFAULT 0.0,
    dividends REAL NOT NULL DEFAULT 0.0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS statement_holdings (
    statement_holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_statement_id INTEGER NOT NULL,
    type TEXT NOT NULL, -- e.g., Stock, Bond, Mutual Fund, Money Market Fund
    ticker TEXT NOT NULL,
    description TEXT,
    quantity REAL NOT NULL DEFAULT 0.0,
    beginning_value REAL NOT NULL DEFAULT 0.0,
    ending_value REAL NOT NULL DEFAULT 0.0, 
    cost_basis REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (monthly_statement_id) REFERENCES monthly_statements(monthly_statement_id)
);