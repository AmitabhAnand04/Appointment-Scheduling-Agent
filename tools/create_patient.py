from db.connection import get_connection

def create_patient(first_name, last_name, dob, phone, email=None, ssn=None, insurance_company=None, insurance_id=None):
    """
    Create a new patient record in the clinic database.

    Args:
        first_name (str): Patient's first name.
        last_name (str): Patient's last name.
        dob (str): Date of birth of the patient in YYYY-MM-DD format.
        phone (str): Patient's phone number.
        email (str, optional): Patient's email address.
        ssn (str, optional): Patient's Social Security Number.
        insurance_company (str, optional): Name of the patient’s insurance provider.
        insurance_id (str, optional): Patient’s insurance identification number.

    Returns:
        dict: A confirmation message and the newly created patient ID.
    """
    print("-------------Tool Called: create_patient-------------")
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
    print("-------------Tool Ended: create_patient-------------")
    return {"message": "✅ Patient created", "patient_id": patient_id}
