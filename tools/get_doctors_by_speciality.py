from db.connection import get_connection

def get_doctors_by_speciality(speciality):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT doctorid, firstname, lastname, specialization
        FROM clinicapt.doctor
        WHERE specialization ILIKE %s AND status = 'Active';
    """
    cur.execute(query, (f"%{speciality}%",))
    doctors = cur.fetchall()

    cur.close()
    conn.close()
    return doctors
