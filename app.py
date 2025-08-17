from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv
import io

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            message TEXT NOT NULL,
            rating INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    department = request.form['department']
    year = request.form['year']
    message = request.form['message']
    rating = request.form['rating']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (name, department, year, message, rating) VALUES (?, ?, ?, ?, ?)",
              (name, department, year, message, rating))
    conn.commit()
    conn.close()
    return redirect('/feedbacks')

@app.route('/feedbacks')
def feedbacks():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedback ORDER BY id DESC")
    feedbacks = c.fetchall()
    conn.close()
    return render_template('feedbacks.html', feedbacks=feedbacks)

@app.route('/download')
def download_csv():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    rows = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Department', 'Year', 'Message', 'Rating'])
    writer.writerows(rows)
    output.seek(0)

    return send_file(io.BytesIO(output.read().encode()), mimetype='text/csv',
                     as_attachment=True, download_name='feedbacks.csv')

if __name__ == '__main__':
    app.run(debug=True)
