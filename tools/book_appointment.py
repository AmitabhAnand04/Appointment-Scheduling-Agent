from db.connection import get_connection

def book_appointment(patient_id, doctor_id, slot_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT clinicapt.book_appointment(%s, %s, %s);", (patient_id, doctor_id, slot_id))
    message = cur.fetchone()['book_appointment']
    conn.commit()

    cur.close()
    conn.close()
    return {"message": message}
