from db.connection import get_connection

# def find_patient(first_name=None, last_name=None, dob=None, phone=None, ssn=None):
#     conn = get_connection()
#     cur = conn.cursor()

#     query = """
#         SELECT PatientID, FirstName, LastName, DateOfBirth, PhoneNumber, Email
#         FROM clinicapt.patient
#         WHERE
#             (%s IS NULL OR firstname ILIKE %s) AND
#             (%s IS NULL OR lastname ILIKE %s) AND
#             (%s IS NULL OR dateofbirth = %s) AND
#             (%s IS NULL OR PhoneNumber = %s) AND
#             (%s IS NULL OR ssn = %s);
#     """
#     cur.execute(query, (first_name, first_name, last_name, last_name, dob, dob, phone, phone, ssn, ssn))
#     result = cur.fetchall()

#     cur.close()
#     conn.close()
#     return result

def find_patient(first_name=None, last_name=None, dob=None, phone=None, ssn=None):
    """
    Find an existing patient by their last name and at least one unique identifier (date of birth, phone, or SSN).

    Args:
        first_name (str, optional): Patient's first name for refining the search.
        last_name (str): Patient's last name. (Required)
        dob (str, optional): Date of birth in YYYY-MM-DD format.
        phone (str, optional): Patient's phone number.
        ssn (str, optional): Patient's SSN.

    Note:
        Either `dob`, `phone`, or `ssn` must be provided along with `last_name`.

    Returns:
        list: A list of matching patients with details like PatientID, name, contact info, and last seen doctor.
    """
    print("-------------Tool Called: find_patient-------------")
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT 
            p.PatientID,
            p.FirstName,
            p.LastName,
            p.DateOfBirth,
            p.PhoneNumber,
            p.Email,
            -- Subquery to fetch last appointed doctor
            (
                SELECT CONCAT(d.FirstName, ' ', d.LastName)
                FROM clinicapt.Appointment a
                JOIN clinicapt.Doctor d ON a.DoctorID = d.DoctorID
                WHERE a.PatientID = p.PatientID
                ORDER BY a.CreatedAt DESC
                LIMIT 1
            ) AS LastDoctorName
        FROM clinicapt.Patient p
        WHERE
            (%s IS NULL OR p.FirstName ILIKE %s) AND
            (%s IS NULL OR p.LastName ILIKE %s) AND
            (%s IS NULL OR p.DateOfBirth = %s) AND
            (%s IS NULL OR p.PhoneNumber = %s) AND
            (%s IS NULL OR p.SSN = %s);
    """

    cur.execute(query, (first_name, first_name, last_name, last_name, dob, dob, phone, phone, ssn, ssn))
    result = cur.fetchall()

    cur.close()
    conn.close()

    # Return clean formatted results
    patients = []
    for row in result:
        patients.append({
            "PatientID": row["patientid"],
            "FirstName": row["firstname"],
            "LastName": row["lastname"],
            "DateOfBirth": row["dateofbirth"],
            "PhoneNumber": row["phonenumber"],
            "Email": row["email"],
            "LastDoctorName": row["lastdoctorname"] or "No previous doctor"
        })
    print("-------------Tool Ended: find_patient-------------")
    return patients
