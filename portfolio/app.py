from flask import Flask, render_template
from db_connection import get_db

app = Flask(__name__)

@app.route('/')
def home():
    db = get_db()
    profile = db.profile.find_one({}, {'_id': 0})
    projects = list(db.projects.find({}, {'_id': 0}))
    return render_template('index.html', profile=profile, projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
