# ml_analyzer.py
import pandas as pd

def calculate_financial_ratios(data):
    """Calculates key financial ratios from raw data."""
    try:
        revenue = data['income']['revenue']
        net_income = data['income']['netIncome']
        total_assets = data['balance']['totalAssets']
        total_liabilities = data['balance']['totalLiabilities']
        total_equity = total_assets - total_liabilities

        # Avoid division by zero
        ratios = {
            'net_profit_margin': net_income / revenue if revenue else 0,
            'return_on_equity': net_income / total_equity if total_equity > 0 else 0,
            'debt_to_equity': total_liabilities / total_equity if total_equity > 0 else 0
        }
        return ratios
    except (KeyError, ZeroDivisionError) as e:
        print(f"Could not calculate ratios. Missing data or division by zero: {e}")
        return None


def generate_health_score(ratios):
    """
    Generates a financial health score.
    NOTE: This is a simplified, rule-based model. A real implementation would
    use a trained model (e.g., RandomForestClassifier) loaded from a file.
    """
    if not ratios:
        return 'Not Available'
        
    score = 0
    
    # Rule 1: Profitability (Return on Equity)
    if ratios['return_on_equity'] > 0.15:
        score += 2 # Strong
    elif ratios['return_on_equity'] > 0.05:
        score += 1 # Average
        
    # Rule 2: Leverage (Debt to Equity)
    if ratios['debt_to_equity'] < 0.5:
        score += 2 # Low debt is good
    elif ratios['debt_to_equity'] < 1.0:
        score += 1 # Manageable debt
        
    # Rule 3: Margin
    if ratios['net_profit_margin'] > 0.10:
        score += 1 # Healthy margin

    # Final Score based on points
    if score >= 4:
        return 'Strong'
    elif score >= 2:
        return 'Average'
    else:
        return 'Weak'