from db.connection import get_connection

def reschedule_appointment(appointment_id, new_slot_id):
    """
    Reschedule an existing appointment to a new available time slot.

    Args:
        appointment_id (int): ID of the appointment to be rescheduled.
        new_slot_id (int): ID of the new available time slot.

    Returns:
        dict: A message confirming the successful rescheduling of the appointment.
    """
    print("-------------Tool Called: reschedule_appointment-------------")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT clinicapt.reschedule_appointment(%s, %s);", (appointment_id, new_slot_id))
    message = cur.fetchone()['reschedule_appointment']
    conn.commit()

    cur.close()
    conn.close()
    print("-------------Tool Ended: reschedule_appointment-------------")
    return {"message": message}
