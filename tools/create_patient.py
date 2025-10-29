from db.connection import get_connection

def create_patient(first_name, last_name, dob, phone, email=None, ssn=None, insurance_company=None, insurance_id=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO clinicapt.patient (FirstName, LastName, DateOfBirth, PhoneNumber, Email, SSN, InsuranceCompany, InsuranceID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING patientid;
    """
    cur.execute(query, (first_name, last_name, dob, phone, email, ssn, insurance_company, insurance_id))
    patient_id = cur.fetchone()['patientid']
    conn.commit()

    cur.close()
    conn.close()
    return {"message": "✅ Patient created", "patient_id": patient_id}
