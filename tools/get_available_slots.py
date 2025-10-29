from db.connection import get_connection

def get_available_slots(doctor_id=None, date=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT slotid, doctorid, slotdate, slotstarttime, slotendtime
        FROM clinicapt.doctorslot
        WHERE isbooked = FALSE
        AND (%s IS NULL OR doctorid = %s)
        AND (%s IS NULL OR slotdate = %s)
        ORDER BY slotdate, slotstarttime;
    """
    cur.execute(query, (doctor_id, doctor_id, date, date))
    slots = cur.fetchall()

    cur.close()
    conn.close()
    return slots
