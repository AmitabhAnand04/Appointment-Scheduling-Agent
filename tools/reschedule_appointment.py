from db.connection import get_connection

def reschedule_appointment(appointment_id, new_slot_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT clinicapt.reschedule_appointment(%s, %s);", (appointment_id, new_slot_id))
    message = cur.fetchone()['reschedule_appointment']
    conn.commit()

    cur.close()
    conn.close()
    return {"message": message}
