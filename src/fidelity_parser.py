import csv
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class StatementHeader:
    account_id: str
    account_type: str
    beginning_value: float
    ending_value: float
    dividends: float

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
            dividends       = float(statement_header[7]) if statement_header[7] else 0.0
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
    header1, holdings1 = parse_fidelity_statement(indiv_1_31_2026)

    print(f"Header: {header1}")
    for holding in holdings1:
        print(holding)