# data_fetcher.py
import requests
from config import FMP_API_KEY

def get_financial_data(ticker):
    """Fetches key financial data for a given ticker from FMP."""
    try:
        # Fetching Income Statement, Balance Sheet, and Profile
        income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"
        balance_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"
        profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
        cashflow_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"

        income_data = requests.get(income_url).json()
        balance_data = requests.get(balance_url).json()
        profile_data = requests.get(profile_url).json()
        cashflow_data = requests.get(cashflow_url).json()

        if not all([income_data, balance_data, profile_data, cashflow_data]):
            print(f"Error: Could not fetch complete data for {ticker}.")
            return None

        # Combine into a single dictionary
        latest_financials = {
            "profile": profile_data[0],
            "income": income_data[0],
            "balance": balance_data[0],
            "cashflow": cashflow_data[0]
        }
        return latest_financials

    except Exception as e:
        print(f"An error occurred while fetching data for {ticker}: {e}")
        return None