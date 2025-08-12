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
        action = request.form.get('action')

        if action == 'add':
            query_db("INSERT INTO patients (name, age, gender, contact) VALUES (?, ?, ?, ?)",
                     (request.form['name'], request.form['age'], request.form['gender'], request.form['contact']))
            return redirect('/patients')

        elif action == 'update':
            query_db("UPDATE patients SET name=?, age=?, gender=?, contact=? WHERE id=?",
                     (request.form['name'], request.form['age'], request.form['gender'], request.form['contact'], request.form['id']))
            return redirect('/patients')

        elif action == 'search':
            keyword = request.form['keyword']
            data = query_db("SELECT * FROM patients WHERE name LIKE ?", ('%' + keyword + '%',))
            return render_template('patients.html', patients=data, search_keyword=keyword)

    data = query_db("SELECT * FROM patients")
    return render_template('patients.html', patients=data)


@app.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if request.method == 'POST':
        # Update the patient
        query_db("UPDATE patients SET name=?, age=?, gender=?, contact=? WHERE id=?",
                 (request.form['name'], request.form['age'], request.form['gender'], request.form['contact'], id))
        return redirect('/patients')

    # GET request - show form pre-filled
    patient = query_db("SELECT * FROM patients WHERE id=?", (id,), one=True)
    data = query_db("SELECT * FROM patients")
    return render_template('patients.html', patients=data, edit_patient=patient)



@app.route('/patients/delete/<int:id>')
def delete_patient(id):
    query_db("DELETE FROM patients WHERE id=?", (id,))
    return redirect('/patients')




@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            query_db("INSERT INTO doctors (name, specialization, contact) VALUES (?, ?, ?)",
                     (request.form['name'], request.form['specialization'], request.form['contact']))
            return redirect('/doctors')

        elif action == 'search':
            keyword = request.form['keyword']
            data = query_db("SELECT * FROM doctors WHERE name LIKE ?", ('%' + keyword + '%',))
            return render_template('doctors.html', doctors=data, search_keyword=keyword)

        elif action == 'update':
            query_db("UPDATE doctors SET name=?, specialization=?, contact=? WHERE id=?",
                     (request.form['name'], request.form['specialization'], request.form['contact'], request.form['id']))
            return redirect('/doctors')

        elif action == 'delete':
            query_db("DELETE FROM doctors WHERE id=?", (request.form['id'],))
            return redirect('/doctors')

    data = query_db("SELECT * FROM doctors")
    return render_template('doctors.html', doctors=data)


@app.route('/doctors/edit/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    if request.method == 'POST':
        query_db("UPDATE doctors SET name=?, specialization=?, contact=? WHERE id=?",
                 (request.form['name'], request.form['specialization'], request.form['contact'], id))
        return redirect('/doctors')

    doctor = query_db("SELECT * FROM doctors WHERE id=?", (id,), one=True)
    data = query_db("SELECT * FROM doctors")
    return render_template('doctors.html', doctors=data, edit_doctor=doctor)


@app.route('/doctors/delete/<int:id>')
def delete_doctor(id):
    query_db("DELETE FROM doctors WHERE id=?", (id,))
    return redirect('/doctors')


@app.route('/appointments', methods=['GET', 'POST'])
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            query_db("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                     (request.form['patient_id'], request.form['doctor_id'], request.form['date'], request.form['time']))
            return redirect('/appointments')

        elif action == 'update':
            query_db("UPDATE appointments SET patient_id=?, doctor_id=?, date=?, time=? WHERE id=?",
                     (request.form['patient_id'], request.form['doctor_id'], request.form['date'], request.form['time'], request.form['id']))
            return redirect('/appointments')

        elif action == 'search':
            keyword = request.form['keyword']
            # Optional: search by patient name or doctor name - requires JOIN queries
            # For now, let's just show all or implement basic search later
            pass

    # Load patients and doctors for dropdowns
    patients = query_db("SELECT id, name FROM patients")
    doctors = query_db("SELECT id, name FROM doctors")

    # Load all appointments (you might want to join to show patient/doctor names)
    data = query_db("""
        SELECT a.id, p.name, d.name, a.date, a.time 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    """)

    return render_template('appointments.html', appointments=data, patients=patients, doctors=doctors)


@app.route('/appointments/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    if request.method == 'POST':
        query_db("UPDATE appointments SET patient_id=?, doctor_id=?, date=?, time=? WHERE id=?",
                 (request.form['patient_id'], request.form['doctor_id'], request.form['date'], request.form['time'], id))
        return redirect('/appointments')

    appointment = query_db("SELECT * FROM appointments WHERE id=?", (id,), one=True)
    patients = query_db("SELECT id, name FROM patients")
    doctors = query_db("SELECT id, name FROM doctors")
    data = query_db("""
        SELECT a.id, p.name, d.name, a.date, a.time 
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    """)
    return render_template('appointments.html', appointments=data, edit_appointment=appointment, patients=patients, doctors=doctors)


@app.route('/appointments/delete/<int:id>')
def delete_appointment(id):
    query_db("DELETE FROM appointments WHERE id=?", (id,))
    return redirect('/appointments')


if __name__ == '__main__':
    app.run(debug=True)
