from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    conn = db_connection()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']
        conn.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)",
                     (name, age, gender, disease))
        conn.commit()
        return redirect('/patients')
    patients = conn.execute("SELECT * FROM patients").fetchall()
    return render_template('patients.html', patients=patients)

if __name__ == "__main__":
    app.run(debug=True)
