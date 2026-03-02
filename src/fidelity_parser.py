import csv
from dataclasses import dataclass
from typing import Tuple, List
import os
import re
from datetime import date

@dataclass
class StatementHeader:
    account_id: str
    account_type: str
    beginning_value: float
    ending_value: float
    dividends: float
    statement_date: date

@dataclass
class Holding:
    ticker: str
    type: str
    description: str
    quantity: float
    price: float
    beginning_value: float
    ending_value: float
    cost_basis: float

def parse_date_from_filename(file_path: str) -> date:
    """ Parses date from filename e.g. Statement1312026.csv → 2026-01-31 """
    filename = os.path.basename(file_path)
    filename = os.path.splitext(filename)[0] 

    # extract digits after "Statement"
    digits = re.search(r'Statement(\d+)', filename).group(1)

    # extract month, day, & year, check if month is 1 or 2 digits
    if len(digits) == 7: # e.g. "1312026" → M DD YYYY
        month = int(digits[0:1])
        day   = int(digits[1:3])
        year  = int(digits[3:])
    elif len(digits) == 8: # e.g. "10122026" → MM DD YYYY
        month = int(digits[0:2])
        day   = int(digits[2:4])
        year  = int(digits[4:])

    return date(year, month, day)


def parse_fidelity_statement(file_path: str) -> tuple[StatementHeader, List[Holding]]:
    """ Parses a CSV statement and returns a list of transactions """

    # Open file
    with open(file_path, "r") as f:
        reader = csv.reader(f)

        # Skip Header
        next(reader)

        statement_header = next(reader)        
        # Set header values
        header = StatementHeader(
            account_id      = statement_header[1],
            account_type    = statement_header[0],
            beginning_value = float(statement_header[2]),
            ending_value    = float(statement_header[4]),
            dividends       = float(statement_header[7]) if statement_header[7] else 0.0,
            statement_date  = parse_date_from_filename(file_path)
        )

        # Read row by row
        holdings = []
        current_section = None
        for i, row in enumerate(reader):

            # Skip non-important rows
            if not row or len(row) == 0 or row[0].strip() == "" or row[0].strip().startswith("Subtotal") or row[0].strip() == header.account_id:
                continue
            
            # Note selection changes
            match row[0].strip():
                case "Stocks":
                    current_section = "Stock"
                    continue
                case "Mutual Funds":
                    current_section = "Mutual Fund"
                    continue
                case "Core Account":
                    current_section = "Money Market"
                    continue
                case _:
                    pass

            if current_section and len(row) >= 6:
                holding = Holding(
                    ticker = row[0].strip(),
                    description = row[1].strip(),
                    quantity = float(row[2]),
                    price = float(row[3]),
                    beginning_value = float(row[4]),
                    ending_value = float(row[5]),
                    cost_basis = float(row[6]) if row[6].strip() != "not applicable" else 0.0,
                    type = current_section   # set from current_section
                )
                holdings.append(holding)
    
    return header, holdings
    
if __name__ == "__main__":

    indiv_1_31_2026 = "data/raw/fidelity/Statement1312026.csv"
    indiv_12_31_2025 = "data/raw/fidelity/Statement12312025.csv"
    # header1, holdings1 = parse_fidelity_statement(indiv_1_31_2026)
    header2, holdings2 = parse_fidelity_statement(indiv_12_31_2025)

    print(f"Header: {header2}")
    for holding in holdings2:
        print(holding)