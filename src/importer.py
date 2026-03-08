import sqlite3
from datetime import date
from src.fidelity_parser import StatementHeader, Holding
from src.fidelity_parser import parse_fidelity_statement
from src.database import get_connection
import os

# upsert -> insert or update if exists
# excluded. -> values you tried to insert but caused conflicts
def upsert_account(conn: sqlite3.Connection, header: StatementHeader) -> None:
    """ Insert account or update if exists """
    conn.execute("""
        INSERT INTO accounts (account_id, account_type, current_value)
        VALUES (?, ?, ?)
        ON CONFLICT(account_id) DO UPDATE SET
            account_type = excluded.account_type,
            current_value = excluded.current_value,
            updated_at = CURRENT_TIMESTAMP
    """, (header.account_id, header.account_type, header.ending_value))

def upsert_current_holdings(conn: sqlite3.Connection, header: StatementHeader, holdings: list[Holding]) -> None:
    """ Insert current holding or update if exists """
    for holding in holdings:
        conn.execute("""
            INSERT INTO current_holdings (account_id, ticker, type, description, quantity, price, market_value, cost_basis, statement_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(account_id, ticker) DO UPDATE SET
                type = excluded.type,
                description = excluded.description,
                quantity = excluded.quantity,
                price = excluded.price,
                market_value = excluded.market_value,
                cost_basis = excluded.cost_basis,
                statement_date = excluded.statement_date
            WHERE excluded.statement_date > current_holdings.statement_date
        """, (header.account_id, holding.ticker, holding.type, holding.description, holding.quantity, holding.price, holding.ending_value, holding.cost_basis, header.statement_date))

def insert_monthly_statement(conn: sqlite3.Connection, header: StatementHeader) -> int:
    """ Insert monthly statement, returns the generated statement_id """
    cursor = conn.execute("""
        INSERT INTO monthly_statements (account_id, statement_date, beginning_value, ending_value, dividends)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(account_id, statement_date) DO NOTHING
    """, (header.account_id, header.statement_date, header.beginning_value, header.ending_value, header.dividends))

    if cursor.lastrowid is None:
        raise ValueError("Failed to insert monthly statement")

    return cursor.lastrowid # returns auto-generated statement_id

def insert_statement_holdings(conn: sqlite3.Connection, monthly_statement_id: int, holdings: list[Holding]) -> None:
    """ Insert all statement holdings for a given statement """
    for holding in holdings:
        conn.execute("""
            INSERT INTO statement_holdings (monthly_statement_id, type, ticker, description, quantity, price, beginning_value, ending_value, cost_basis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (monthly_statement_id, holding.type, holding.ticker, holding.description, holding.quantity, holding.price, holding.beginning_value, holding.ending_value, holding.cost_basis))

def import_statement(file_path: str) -> None:
    """ Main import function - ties the parser and the importer together """

    # parse the CSV
    header, holdings = parse_fidelity_statement(file_path)

    # import to DB
    with get_connection() as conn:
        upsert_account(conn, header)
        upsert_current_holdings(conn, header, holdings)
        statement_id = insert_monthly_statement(conn, header)
        insert_statement_holdings(conn, statement_id, holdings)

if __name__ == "__main__":

    folders = [
        "data/raw/fidelity/Individual",
        "data/raw/fidelity/Roth"
    ]

    for folder in folders:
        for filename in os.listdir(folder):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder, filename)
                print(f"Importing {file_path}")
                try:
                    import_statement(file_path)
                except Exception as e:
                    print(f"Error importing {file_path}: {e}")
                print("Finished importing")