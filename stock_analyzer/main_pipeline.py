# main_pipeline.py
import pandas as pd
import requests
import json
import re
from sqlalchemy import create_engine, text
from datetime import date
from config import DB_CONFIG, API_KEY, API_BASE_URL

def clean_and_extract_value(metric_string):
    """Extracts a numerical value from a string like '10 Years: 21%'."""
    if not isinstance(metric_string, str):
        return None
    match = re.search(r'(-?\d+\.?\d*)', metric_string)
    return float(match.group(1)) if match else None

def analyze_data(api_data):
    """Applies the pros and cons logic based on the project documentation."""
    pros = []
    cons = []

    # Rule: Analyze financial metrics (e.g., ROE, profit growth)
    analysis_records = api_data.get('analysis', [])
    for record in analysis_records:
        roe = clean_and_extract_value(record.get('roe'))
        profit_growth = clean_and_extract_value(record.get('compounded_profit_growth'))

        if roe is not None:
            if roe > 10:
                pros.append(f"Company has a good return on equity (ROE) of {roe}%.")
            else:
                cons.append(f"Company has a low return on equity of {roe}%.")
        
        if profit_growth is not None:
            if profit_growth > 10:
                 pros.append(f"Company has delivered good profit growth of {profit_growth}%.")
            else:
                 cons.append(f"The company has delivered a poor sales growth of {profit_growth}%.")


    # Rule: Add predefined pros and cons from the API
    for item in api_data.get('prosandcons', []):
        if item.get('pros') and 'NULL' not in item['pros']:
            pros.append(item['pros'])
        if item.get('cons') and 'NULL' not in item['cons']:
            cons.append(item['cons'])

    # Select up to 3 unique pros and cons
    unique_pros = list(set(pros))[:3]
    unique_cons = list(set(cons))[:3]
    
    # Format for database storage (one string per list)
    pros_str = json.dumps(unique_pros)
    cons_str = json.dumps(unique_cons)
    
    return pros_str, cons_str

def main():
    """Main function to run the entire data pipeline."""
    print("--- Starting Financial Analysis Pipeline ---")

    # 1. Connect to the database
    try:
        db_connection_str = (
            f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        )
        engine = create_engine(db_connection_str)
        print("[SUCCESS] Database connection established.")
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return

    # 2. Read the list of company IDs from the CSV file
    try:
        companies_df = pd.read_excel('data/company_id.xlsx')
        company_ids = companies_df['company_id'].tolist()
        print(f"[INFO] Found {len(company_ids)} companies to analyze.")
    except FileNotFoundError:
        print("[ERROR] 'data/Nifty100Companies.csv' not found. Please check the file path.")
        return

    # 3. Process each company
    for company_id in company_ids:
        print(f"\nProcessing: {company_id}...")
        
        # Fetch data from API
        params = {'id': company_id, 'api_key': API_KEY}
        try:
            response = requests.get(API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"  [FAIL] API request failed: {e}")
            continue
        except json.JSONDecodeError:
            print("  [FAIL] Could not decode JSON from API response.")
            continue

        # Analyze data to get pros and cons
        pros, cons = analyze_data(data)
        print(f"  [SUCCESS] Analysis complete. Found {len(json.loads(pros))} pros and {len(json.loads(cons))} cons.")

        # Store results in MySQL    1ew43oi=-'][=-.]        today = date.today()
        with engine.connect() as conn:
            # Use INSERT...ON DUPLICATE KEY UPDATE to either add a new record or update an existing one for today
            stmt = text("""
                INSERT INTO ml (company_id, pros, cons, analysis_date)
                VALUES (:company_id, :pros, :cons, :analysis_date)
                ON DUPLICATE KEY UPDATE pros = VALUES(pros), cons = VALUES(cons);
            """)
            conn.execute(stmt, {
                'company_id': company_id,
                'pros': pros,
                'cons': cons,
                'analysis_date': today
            })
            conn.commit()
        print(f"  [SUCCESS] Results for {company_id} saved to database.")

    print("\n--- Pipeline execution complete! ---")

if __name__ == "__main__":
    main()




















