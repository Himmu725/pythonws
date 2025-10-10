# db_manager.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import date

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=None):
    """General purpose query executor."""
    connection = create_connection()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True if fetch else False)
    try:
        cursor.execute(query, params or ())
        if fetch == 'one':
            result = cursor.fetchone()
            return result
        elif fetch == 'all':
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Query failed: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def save_company_and_financials(ticker, data):
    """Saves company profile and financial data to the database."""
    profile = data['profile']
    income = data['income']
    balance = data['balance']
    cashflow = data['cashflow']
    
    # Insert or update company info
    query = "INSERT INTO companies (ticker, company_name, sector, industry) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE company_name=VALUES(company_name), sector=VALUES(sector)"
    execute_query(query, (ticker, profile.get('companyName'), profile.get('sector'), profile.get('industry')))
    
    # Get company ID
    company_id = execute_query("SELECT id FROM companies WHERE ticker = %s", (ticker,), fetch='one')['id']
    
    # Insert financial data
    query = """
        INSERT INTO financial_data (company_id, report_date, revenue, net_income, total_assets, total_liabilities, cash_flow) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE revenue=VALUES(revenue), net_income=VALUES(net_income)
    """
    params = (company_id, income.get('date'), income.get('revenue'), income.get('netIncome'), balance.get('totalAssets'), balance.get('totalLiabilities'), cashflow.get('netCashProvidedByOperatingActivities'))
    execute_query(query, params)
    
    return company_id

def save_ml_insight(company_id, ratios, score):
    """Saves the generated ML insights to the database."""
    query = """
        INSERT INTO ml_insights (company_id, analysis_date, debt_to_equity_ratio, return_on_equity_ratio, net_profit_margin, financial_health_score)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE analysis_date=VALUES(analysis_date), debt_to_equity_ratio=VALUES(debt_to_equity_ratio), financial_health_score=VALUES(financial_health_score)
    """
    params = (company_id, date.today(), ratios['debt_to_equity'], ratios['return_on_equity'], ratios['net_profit_margin'], score)
    execute_query(query, params)
    
def get_company_insights(ticker):
    """Fetches all insights for a given ticker for the web display."""
    query = """
        SELECT c.ticker, c.company_name, c.sector, mi.*
        FROM companies c
        JOIN ml_insights mi ON c.id = mi.company_id
        WHERE c.ticker = %s
        ORDER BY mi.analysis_date DESC
        LIMIT 1
    """
    return execute_query(query, (ticker,), fetch='one')