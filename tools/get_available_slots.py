from db.connection import get_connection

def get_available_slots(doctor_id=None, date=None):
    """
    Retrieve all unbooked time slots for a specific doctor on a given date.

    Args:
        doctor_id (int): Unique ID of the doctor. (Required)
        date (str): Date for which to fetch available slots in YYYY-MM-DD format. (Required)

    Returns:
        list: A list of available slots with SlotID, DoctorID, Date, StartTime, and EndTime.
    """
    print("-------------Tool Called: get_available_slots-------------")
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT slotid, doctorid, slotdate, slotstarttime, slotendtime
        FROM clinicapt.doctorslot
        WHERE isbooked = FALSE
        AND (%s IS NULL OR doctorid = %s)
        AND (%s IS NULL OR slotdate >= %s)
        ORDER BY slotdate, slotstarttime;
    """
    # query = """
    #     SELECT slotid, doctorid, slotdate, slotstarttime, slotendtime
    #     FROM clinicapt.doctorslot
    #     WHERE isbooked = FALSE
    #     AND (%s IS NULL OR doctorid = %s)
    #     AND (%s IS NULL OR slotdate = %s)
    #     ORDER BY slotdate, slotstarttime;
    # """
    cur.execute(query, (doctor_id, doctor_id, date, date))
    slots = cur.fetchall()

    cur.close()
    conn.close()
    print("-------------Tool Ended: get_available_slots-------------")
    return slots
