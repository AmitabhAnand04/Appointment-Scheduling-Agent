from db.connection import get_connection

def book_appointment(patient_id, doctor_id, slot_id):
    """
    Book an appointment for a patient with a doctor using a specific available slot.

    Args:
        patient_id (int): ID of the patient booking the appointment.
        doctor_id (int): ID of the doctor for the appointment.
        slot_id (int): ID of the available time slot to be booked.

    Returns:
        dict: A message confirming the successful appointment booking.
    """
    print("-------------Tool Called: book_appointment-------------")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT clinicapt.book_appointment(%s, %s, %s);", (patient_id, doctor_id, slot_id))
    message = cur.fetchone()['book_appointment']
    conn.commit()

    cur.close()
    conn.close()
    print("-------------Tool Ended: book_appointment-------------")
    return {"message": message}
