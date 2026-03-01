import csv
from dataclasses import dataclass

def parse_statement(file_path: str):
    """ Parses a CSV statement and returns a list of transactions """

    # Open file
    with open(file_path, "r") as f:
        reader = csv.reader(f)

        # Skip Header
        next(reader)

        statement_header = next(reader)        
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
            description: str
            quantity: int
            price: float
            beginning_value: float
            ending_value: float
            cost_basis: float

        header = StatementHeader(
            account_id      = statement_header[1],
            account_type    = statement_header[0],
            beginning_value = float(statement_header[2]),
            ending_value    = float(statement_header[4]),
            dividends       = float(statement_header[7]) if statement_header[7] else 0.0
        )

        print(statement_header)

        # Read row by row
        for i, row in enumerate(reader):


            # Skip blank rows
            if not row or len(row) == 0 or row[0].strip() == "":
                continue
            
            # Note selection changes
            current_selection = ""
            match row[0].strip():
                case "Stocks":
                    current_selection = "Stock"
                    continue
                case "Mutual Funds":
                    current_selection = "Mutual Fund"
                    continue
                case "Core Account":
                    current_selection = "Money Market"
                    continue
                case _:
                    pass

            print(f"Row {i}: {row}")
    
if __name__ == "__main__":

    test1 = "data/raw/fidelity/Statement1312026.csv"
    parse_statement(test1)