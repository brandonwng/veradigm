from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    print('running')
    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()
    c.execute('SELECT * FROM doctors')
    doctors = c.fetchall()
    conn.close()
    if doctors:
        print(doctors)
    else:
        print('hello')
    return render_template('index.html', doctors=doctors)

@app.route('/doctor/<int:doctor_id>')
def doctor(doctor_id):
    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()
    c.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,))
    doctor = c.fetchone()
    
    c.execute('SELECT * FROM doctors WHERE specialty = ? AND location = ? AND id != ?', 
              (doctor[2], doctor[3], doctor[0]))
    similar_doctors = c.fetchall()
    similar_doctors = sorted(similar_doctors, key=lambda x: x[4], reverse=True)
    conn.close()
    return render_template('doctors.html', doctor=doctor, similar_doctors=similar_doctors)

if __name__ == '__main__':
    app.run(debug=True)
