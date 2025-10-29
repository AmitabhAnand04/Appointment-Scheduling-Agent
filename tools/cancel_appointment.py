from db.connection import get_connection

def cancel_appointment(appointment_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT clinicapt.cancel_appointment(%s);", (appointment_id,))
    message = cur.fetchone()['cancel_appointment']
    conn.commit()

    cur.close()
    conn.close()
    return {"message": message}
