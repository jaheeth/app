import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate comprehensive sample data for Lanka Medical Center"""
    
    # Connect to SQLite database
    conn = sqlite3.connect('hospital_data.db')
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Generate sample data
    departments = generate_departments()
    doctors = generate_doctors(departments)
    services = generate_services(departments)
    patients = generate_patients()
    appointments = generate_appointments(patients, doctors, services)
    billing = generate_billing(appointments, services)
    
    # Insert data into database
    insert_departments(cursor, departments)
    insert_doctors(cursor, doctors)
    insert_services(cursor, services)
    insert_patients(cursor, patients)
    insert_appointments(cursor, appointments)
    insert_billing(cursor, billing)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Sample data generated successfully!")

def create_tables(cursor):
    """Create database tables"""
    
    # Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT,
            head_doctor_id INTEGER
        )
    ''')
    
    # Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            specialization TEXT,
            department_id INTEGER,
            hire_date DATE,
            salary REAL,
            FOREIGN KEY (department_id) REFERENCES departments (department_id)
        )
    ''')
    
    # Services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            department_id INTEGER,
            cost REAL,
            duration_minutes INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (department_id)
        )
    ''')
    
    # Patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact TEXT,
            address TEXT,
            registration_date DATE,
            emergency_contact TEXT
        )
    ''')
    
    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            doctor_id INTEGER,
            service_id INTEGER,
            appointment_date DATE,
            appointment_time TIME,
            status TEXT,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id),
            FOREIGN KEY (service_id) REFERENCES services (service_id)
        )
    ''')
    
    # Billing table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS billing (
            billing_id INTEGER PRIMARY KEY,
            appointment_id INTEGER,
            amount REAL,
            payment_date DATE,
            payment_status TEXT,
            payment_method TEXT,
            FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id)
        )
    ''')

def generate_departments():
    """Generate sample departments"""
    departments = [
        {'department_id': 1, 'name': 'General Medicine', 'location': 'Ground Floor'},
        {'department_id': 2, 'name': 'Surgery', 'location': 'First Floor'},
        {'department_id': 3, 'name': 'Cardiology', 'location': 'Second Floor'},
        {'department_id': 4, 'name': 'Pediatrics', 'location': 'Ground Floor'},
        {'department_id': 5, 'name': 'Orthopedics', 'location': 'First Floor'},
        {'department_id': 6, 'name': 'Gynecology', 'location': 'Second Floor'},
        {'department_id': 7, 'name': 'Radiology', 'location': 'Basement'},
        {'department_id': 8, 'name': 'Laboratory', 'location': 'Basement'},
        {'department_id': 9, 'name': 'Pharmacy', 'location': 'Ground Floor'},
        {'department_id': 10, 'name': 'Emergency', 'location': 'Ground Floor'}
    ]
    return departments

def generate_doctors(departments):
    """Generate sample doctors"""
    doctor_names = [
        "Dr. Anil Perera", "Dr. Sunil Fernando", "Dr. Priya Silva", "Dr. Rajith Bandara",
        "Dr. Nimal Jayawardena", "Dr. Kamal Mendis", "Dr. Dilini Wijesekara", "Dr. Ashan Rathnayake",
        "Dr. Tharindu Abeysekara", "Dr. Sanduni Perera", "Dr. Dinesh Gunasekara", "Dr. Lakshmi Fernando",
        "Dr. Ramesh Silva", "Dr. Nadeeka Jayawardena", "Dr. Chaminda Mendis", "Dr. Gayani Wijesekara",
        "Dr. Nuwan Rathnayake", "Dr. Ishara Abeysekara", "Dr. Chathura Perera", "Dr. Dinusha Gunasekara"
    ]
    
    specializations = [
        "General Physician", "Cardiologist", "Surgeon", "Pediatrician", "Orthopedic Surgeon",
        "Gynecologist", "Radiologist", "Pathologist", "Emergency Medicine", "Internal Medicine"
    ]
    
    doctors = []
    for i, name in enumerate(doctor_names):
        dept = random.choice(departments)
        doctors.append({
            'doctor_id': i + 1,
            'name': name,
            'specialization': random.choice(specializations),
            'department_id': dept['department_id'],
            'hire_date': datetime.now() - timedelta(days=random.randint(365, 2555)),
            'salary': random.randint(80000, 200000)
        })
    
    return doctors

def generate_services(departments):
    """Generate sample services"""
    services = [
        # General Medicine
        {'name': 'General Consultation', 'type': 'Consultation', 'department_id': 1, 'cost': 1500, 'duration_minutes': 30},
        {'name': 'Follow-up Consultation', 'type': 'Consultation', 'department_id': 1, 'cost': 1000, 'duration_minutes': 20},
        {'name': 'Health Check-up', 'type': 'Check-up', 'department_id': 1, 'cost': 2500, 'duration_minutes': 60},
        
        # Surgery
        {'name': 'Minor Surgery', 'type': 'Surgery', 'department_id': 2, 'cost': 25000, 'duration_minutes': 120},
        {'name': 'Major Surgery', 'type': 'Surgery', 'department_id': 2, 'cost': 75000, 'duration_minutes': 240},
        {'name': 'Surgical Consultation', 'type': 'Consultation', 'department_id': 2, 'cost': 2000, 'duration_minutes': 45},
        
        # Cardiology
        {'name': 'ECG', 'type': 'Diagnostic', 'department_id': 3, 'cost': 3000, 'duration_minutes': 30},
        {'name': 'Echocardiogram', 'type': 'Diagnostic', 'department_id': 3, 'cost': 8000, 'duration_minutes': 60},
        {'name': 'Cardiac Consultation', 'type': 'Consultation', 'department_id': 3, 'cost': 2500, 'duration_minutes': 45},
        
        # Pediatrics
        {'name': 'Child Consultation', 'type': 'Consultation', 'department_id': 4, 'cost': 1200, 'duration_minutes': 30},
        {'name': 'Vaccination', 'type': 'Treatment', 'department_id': 4, 'cost': 800, 'duration_minutes': 15},
        {'name': 'Growth Monitoring', 'type': 'Check-up', 'department_id': 4, 'cost': 1500, 'duration_minutes': 45},
        
        # Orthopedics
        {'name': 'X-Ray', 'type': 'Diagnostic', 'department_id': 5, 'cost': 2500, 'duration_minutes': 30},
        {'name': 'Physiotherapy', 'type': 'Treatment', 'department_id': 5, 'cost': 2000, 'duration_minutes': 60},
        {'name': 'Orthopedic Consultation', 'type': 'Consultation', 'department_id': 5, 'cost': 2000, 'duration_minutes': 45},
        
        # Gynecology
        {'name': 'Gynecological Consultation', 'type': 'Consultation', 'department_id': 6, 'cost': 2000, 'duration_minutes': 45},
        {'name': 'Ultrasound Scan', 'type': 'Diagnostic', 'department_id': 6, 'cost': 5000, 'duration_minutes': 45},
        {'name': 'Prenatal Care', 'type': 'Check-up', 'department_id': 6, 'cost': 3000, 'duration_minutes': 60},
        
        # Radiology
        {'name': 'CT Scan', 'type': 'Diagnostic', 'department_id': 7, 'cost': 15000, 'duration_minutes': 45},
        {'name': 'MRI Scan', 'type': 'Diagnostic', 'department_id': 7, 'cost': 25000, 'duration_minutes': 60},
        {'name': 'Ultrasound', 'type': 'Diagnostic', 'department_id': 7, 'cost': 4000, 'duration_minutes': 30},
        
        # Laboratory
        {'name': 'Blood Test', 'type': 'Diagnostic', 'department_id': 8, 'cost': 1500, 'duration_minutes': 15},
        {'name': 'Urine Test', 'type': 'Diagnostic', 'department_id': 8, 'cost': 800, 'duration_minutes': 15},
        {'name': 'Stool Test', 'type': 'Diagnostic', 'department_id': 8, 'cost': 1000, 'duration_minutes': 15},
        
        # Pharmacy
        {'name': 'Medicine Dispensing', 'type': 'Treatment', 'department_id': 9, 'cost': 500, 'duration_minutes': 10},
        {'name': 'Prescription Review', 'type': 'Consultation', 'department_id': 9, 'cost': 300, 'duration_minutes': 15},
        
        # Emergency
        {'name': 'Emergency Consultation', 'type': 'Consultation', 'department_id': 10, 'cost': 3000, 'duration_minutes': 30},
        {'name': 'Emergency Treatment', 'type': 'Treatment', 'department_id': 10, 'cost': 5000, 'duration_minutes': 60}
    ]
    
    for i, service in enumerate(services):
        service['service_id'] = i + 1
    
    return services

def generate_patients():
    """Generate sample patients"""
    patient_names = [
        "A.M. Silva", "K.L. Fernando", "P.R. Perera", "N.S. Bandara", "M.K. Jayawardena",
        "S.T. Mendis", "R.D. Wijesekara", "L.A. Rathnayake", "C.B. Abeysekara", "G.M. Perera",
        "D.K. Gunasekara", "I.S. Fernando", "T.N. Silva", "N.R. Jayawardena", "C.M. Mendis",
        "G.L. Wijesekara", "N.A. Rathnayake", "I.B. Abeysekara", "C.M. Perera", "D.S. Gunasekara",
        "A.K. Silva", "K.M. Fernando", "P.S. Perera", "N.K. Bandara", "M.S. Jayawardena",
        "S.L. Mendis", "R.M. Wijesekara", "L.K. Rathnayake", "C.S. Abeysekara", "G.K. Perera"
    ]
    
    patients = []
    for i, name in enumerate(patient_names):
        patients.append({
            'patient_id': i + 1,
            'name': name,
            'age': random.randint(18, 80),
            'gender': random.choice(['Male', 'Female']),
            'contact': f"0{random.randint(70, 77)}{random.randint(1000000, 9999999)}",
            'address': f"Address {i + 1}, Matugama",
            'registration_date': datetime.now() - timedelta(days=random.randint(30, 1095)),
            'emergency_contact': f"0{random.randint(70, 77)}{random.randint(1000000, 9999999)}"
        })
    
    return patients

def generate_appointments(patients, doctors, services):
    """Generate sample appointments"""
    appointments = []
    appointment_id = 1
    
    # Generate appointments for the last 2 years
    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()
    
    current_date = start_date
    while current_date <= end_date:
        # Generate 5-15 appointments per day
        daily_appointments = random.randint(5, 15)
        
        for _ in range(daily_appointments):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            service = random.choice(services)
            
            # Skip if service doesn't match doctor's department
            if service['department_id'] != doctor['department_id']:
                continue
            
            appointment_time = datetime.combine(
                current_date.date(),
                datetime.strptime(f"{random.randint(8, 17)}:{random.randint(0, 59):02d}", "%H:%M").time()
            )
            
            appointments.append({
                'appointment_id': appointment_id,
                'patient_id': patient['patient_id'],
                'doctor_id': doctor['doctor_id'],
                'service_id': service['service_id'],
                'appointment_date': current_date.date(),
                'appointment_time': appointment_time.time(),
                'status': random.choice(['Completed', 'Completed', 'Completed', 'No-show', 'Cancelled']),
                'notes': random.choice(['', 'Follow-up required', 'Patient requested', 'Regular check-up'])
            })
            
            appointment_id += 1
        
        current_date += timedelta(days=1)
    
    return appointments

def generate_billing(appointments, services):
    """Generate sample billing records using in-memory service costs"""
    billing = []
    
    # Build a quick lookup for service costs
    service_id_to_cost = {s['service_id']: s['cost'] for s in services}
    
    for appointment in appointments:
        if appointment['status'] == 'Completed':
            service_cost = service_id_to_cost.get(appointment['service_id'], 0)
            # Add some variation to costs
            actual_cost = service_cost * random.uniform(0.9, 1.1)
            # Payment date within 30 days of appointment
            payment_date = appointment['appointment_date'] + timedelta(days=random.randint(0, 30))
            billing.append({
                'billing_id': len(billing) + 1,
                'appointment_id': appointment['appointment_id'],
                'amount': round(actual_cost, 2),
                'payment_date': payment_date,
                'payment_status': random.choice(['Paid', 'Paid', 'Paid', 'Pending', 'Overdue']),
                'payment_method': random.choice(['Cash', 'Card', 'Bank Transfer', 'Insurance'])
            })
    
    return billing

def insert_departments(cursor, departments):
    """Insert departments into database"""
    for dept in departments:
        cursor.execute('''
            INSERT OR REPLACE INTO departments (department_id, name, location)
            VALUES (?, ?, ?)
        ''', (dept['department_id'], dept['name'], dept['location']))

def insert_doctors(cursor, doctors):
    """Insert doctors into database"""
    for doctor in doctors:
        hire_date_str = doctor['hire_date'].strftime('%Y-%m-%d') if isinstance(doctor['hire_date'], datetime) else str(doctor['hire_date'])
        cursor.execute('''
            INSERT OR REPLACE INTO doctors (doctor_id, name, specialization, department_id, hire_date, salary)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (doctor['doctor_id'], doctor['name'], doctor['specialization'], 
              doctor['department_id'], hire_date_str, doctor['salary']))

def insert_services(cursor, services):
    """Insert services into database"""
    for service in services:
        cursor.execute('''
            INSERT OR REPLACE INTO services (service_id, name, type, department_id, cost, duration_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (service['service_id'], service['name'], service['type'], 
              service['department_id'], service['cost'], service['duration_minutes']))

def insert_patients(cursor, patients):
    """Insert patients into database"""
    for patient in patients:
        reg_date = patient['registration_date']
        reg_date_str = reg_date.strftime('%Y-%m-%d') if hasattr(reg_date, 'strftime') else str(reg_date)
        cursor.execute('''
            INSERT OR REPLACE INTO patients (patient_id, name, age, gender, contact, address, registration_date, emergency_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient['patient_id'], patient['name'], patient['age'], patient['gender'],
              patient['contact'], patient['address'], reg_date_str, patient['emergency_contact']))

def insert_appointments(cursor, appointments):
    """Insert appointments into database"""
    for appointment in appointments:
        appt_date = appointment['appointment_date']
        appt_time = appointment['appointment_time']
        appt_date_str = appt_date.strftime('%Y-%m-%d') if hasattr(appt_date, 'strftime') else str(appt_date)
        appt_time_str = appt_time.strftime('%H:%M:%S') if hasattr(appt_time, 'strftime') else str(appt_time)
        cursor.execute('''
            INSERT OR REPLACE INTO appointments (appointment_id, patient_id, doctor_id, service_id, appointment_date, appointment_time, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (appointment['appointment_id'], appointment['patient_id'], appointment['doctor_id'],
              appointment['service_id'], appt_date_str, appt_time_str,
              appointment['status'], appointment['notes']))

def insert_billing(cursor, billing):
    """Insert billing records into database"""
    for bill in billing:
        pay_date = bill['payment_date']
        pay_date_str = pay_date.strftime('%Y-%m-%d') if hasattr(pay_date, 'strftime') else str(pay_date)
        cursor.execute('''
            INSERT OR REPLACE INTO billing (billing_id, appointment_id, amount, payment_date, payment_status, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (bill['billing_id'], bill['appointment_id'], bill['amount'],
              pay_date_str, bill['payment_status'], bill['payment_method']))

if __name__ == "__main__":
    generate_sample_data()
