from db.connection import get_connection

def cancel_appointment(appointment_id):
    """
    Cancel an existing appointment for a patient.

    Args:
        appointment_id (int): ID of the appointment to be cancelled.

    Returns:
        dict: A message confirming the successful cancellation of the appointment.
    """
    print("-------------Tool Called: cancel_appointment-------------")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT clinicapt.cancel_appointment(%s);", (appointment_id,))
    message = cur.fetchone()['cancel_appointment']
    conn.commit()

    cur.close()
    conn.close()
    print("-------------Tool Ended: cancel_appointment-------------")
    return {"message": message}
