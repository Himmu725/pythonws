# webapp/app.py
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, text
import json
from config import DB_CONFIG # Import DB settings from the main config file

app = Flask(__name__)

# Connect to the database
db_connection_str = (
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)
engine = create_engine(db_connection_str)

@app.route('/')
def index():
    """Renders the main web page."""
    return render_template('index.html')

# --- MODIFIED API ENDPOINT ---
# The URL can now accept one or more company IDs separated by commas
@app.route('/api/get_analysis/<company_ids>')
def get_analysis(company_ids):
    """API endpoint to fetch the latest analysis for one or more companies."""
    
    # Split the string of IDs into a list
    id_list = [item.strip().upper() for item in company_ids.split(',')]
    
    analysis_results = []

    with engine.connect() as conn:
        for company_id in id_list:
            stmt = text("SELECT * FROM ml WHERE company_id = :id ORDER BY analysis_date DESC LIMIT 1")
            result = conn.execute(stmt, {'id': company_id}).fetchone()

            if result:
                # Safely load JSON data, providing an empty list [] if the data is missing or invalid.
                try:
                    pros_list = json.loads(result.pros) if result.pros else []
                except json.JSONDecodeError:
                    pros_list = []

                try:
                    cons_list = json.loads(result.cons) if result.cons else []
                except json.JSONDecodeError:
                    cons_list = []

                analysis_data = {
                    'company_id': result.company_id,
                    'pros': pros_list,
                    'cons': cons_list,
                    'analysis_date': result.analysis_date.isoformat()
                }
                analysis_results.append(analysis_data)

    if analysis_results:
        return jsonify(analysis_results)
    else:
        return jsonify({'error': 'No analysis found for the requested companies. Please run main_pipeline.py.'}), 404

if __name__ == '__main__':
    app.run(debug=True)