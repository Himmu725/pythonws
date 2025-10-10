# terminal_display.py
from sqlalchemy import create_engine, text
import json
from rich.console import Console
from rich.table import Table

# Import database settings from our central config file
from config import DB_CONFIG

def display_analysis_table():
    """
    Connects to the database, fetches all the latest analysis,
    and prints it in a formatted table in the terminal.
    """
    # 1. Connect to the database
    try:
        db_connection_str = (
            f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        )
        engine = create_engine(db_connection_str)
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return

    # 2. Fetch all records from the 'ml' table
    with engine.connect() as conn:
        stmt = text("SELECT company_id, pros, cons FROM ml ORDER BY company_id")
        results = conn.execute(stmt).fetchall()

    if not results:
        print("[INFO] No data found in the database. Please run 'main_pipeline.py' first.")
        return

    # 3. Create and format the output table
    console = Console()
    table = Table(show_header=True, header_style="bold magenta", title="Financial Analysis Summary")
    table.add_column("Company ID", style="cyan", width=12)
    table.add_column("✅ Pros", style="green")
    table.add_column("❌ Cons", style="red")

    for row in results:
        # Safely load the JSON data for pros and cons
        pros_list = json.loads(row.pros) if row.pros else []
        cons_list = json.loads(row.cons) if row.cons else []
        
        # Format the lists into a readable string for the table
        pros_str = "\n".join(f"- {p}" for p in pros_list)
        cons_str = "\n".join(f"- {c}" for c in cons_list)
        
        table.add_row(row.company_id, pros_str, cons_str)

    # 4. Print the table to the console
    console.print(table)


if __name__ == "__main__":
    display_analysis_table()