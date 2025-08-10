from flask import Flask, render_template, request, redirect
import sqlite3
from models import init_db

app = Flask(__name__)
init_db()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        query_db("INSERT INTO patients (name, age, gender, contact) VALUES (?, ?, ?, ?)",
                 (request.form['name'], request.form['age'], request.form['gender'], request.form['contact']))
        return redirect('/patients')
    data = query_db("SELECT * FROM patients")
    return render_template('patients.html', patients=data)

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    if request.method == 'POST':
        query_db("INSERT INTO doctors (name, specialization, contact) VALUES (?, ?, ?)",
                 (request.form['name'], request.form['specialization'], request.form['contact']))
        return redirect('/doctors')
    data = query_db("SELECT * FROM doctors")
    return render_template('doctors.html', doctors=data)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        query_db("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                 (request.form['patient_id'], request.form['doctor_id'], request.form['date'], request.form['time']))
        return redirect('/appointments')
    data = query_db("SELECT * FROM appointments")
    return render_template('appointments.html', appointments=data)

if __name__ == '__main__':
    app.run(debug=True)
