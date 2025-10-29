-- ====================================================== 
-- 🩺 Appointment Management Functions (Schema: clinicapt)
-- Author: Amitabh Anand
-- Purpose: Booking, Cancelling, and Rescheduling Appointments
-- ======================================================

-- ======================================================
-- 1️⃣ Function: book_appointment
-- ======================================================
CREATE OR REPLACE FUNCTION clinicapt.book_appointment(
    p_patient_id INT,
    p_doctor_id INT,
    p_slot_id INT
)
RETURNS TABLE(message TEXT, appointment_id INT) AS $$
DECLARE
    slot_status TEXT;
    new_appointment_id INT;
BEGIN
    -- Check if slot exists and is available
    SELECT CASE WHEN isbooked THEN 'booked' ELSE 'available' END
    INTO slot_status
    FROM clinicapt.doctorslot
    WHERE slotid = p_slot_id;

    IF slot_status IS NULL THEN
        RETURN QUERY SELECT '❌ Slot not found', NULL;
        RETURN;
    ELSIF slot_status = 'booked' THEN
        RETURN QUERY SELECT '⚠️ Slot already booked', NULL;
        RETURN;
    END IF;

    -- Mark slot as booked
    UPDATE clinicapt.doctorslot
    SET isbooked = TRUE
    WHERE slotid = p_slot_id;

    -- Create appointment record and capture ID
    INSERT INTO clinicapt.appointment (patientid, doctorid, slotid, appointmentstatus, createdat)
    VALUES (p_patient_id, p_doctor_id, p_slot_id, 'Booked', NOW())
    RETURNING appointmentid INTO new_appointment_id;

    -- Return confirmation message with appointment ID
    RETURN QUERY SELECT '✅ Appointment successfully booked', new_appointment_id;
END;
$$ LANGUAGE plpgsql;

-- ======================================================
-- 2️⃣ Function: cancel_appointment
-- ======================================================
CREATE OR REPLACE FUNCTION clinicapt.cancel_appointment(
    p_appointment_id INT
)
RETURNS TEXT AS $$
DECLARE
    v_slot_id INT;
    v_status TEXT;
BEGIN
    -- Verify appointment exists and is active
    SELECT slotid, appointmentstatus 
    INTO v_slot_id, v_status
    FROM clinicapt.appointment
    WHERE appointmentid = p_appointment_id;

    IF v_slot_id IS NULL THEN
        RETURN '❌ Appointment not found';
    ELSIF v_status != 'Booked' THEN
        RETURN '⚠️ Appointment already cancelled or rescheduled';
    END IF;

    -- Mark appointment as cancelled
    UPDATE clinicapt.appointment
    SET appointmentstatus = 'Cancelled'
    WHERE appointmentid = p_appointment_id;

    -- Free the slot
    UPDATE clinicapt.doctorslot
    SET isbooked = FALSE
    WHERE slotid = v_slot_id;

    RETURN '✅ Appointment cancelled and slot released';
END;
$$ LANGUAGE plpgsql;

-- ======================================================
-- 3️⃣ Function: reschedule_appointment
-- ======================================================
CREATE OR REPLACE FUNCTION clinicapt.reschedule_appointment(
    p_appointment_id INT,
    p_new_slot_id INT
)
RETURNS TEXT AS $$
DECLARE
    v_patient_id INT;
    v_doctor_id INT;
    v_old_slot_id INT;
    v_old_status TEXT;
    v_new_slot_status TEXT;
BEGIN
    -- Check old appointment
    SELECT patientid, doctorid, slotid, appointmentstatus
    INTO v_patient_id, v_doctor_id, v_old_slot_id, v_old_status
    FROM clinicapt.appointment
    WHERE appointmentid = p_appointment_id;

    IF v_old_slot_id IS NULL THEN
        RETURN '❌ Appointment not found';
    ELSIF v_old_status != 'Booked' THEN
        RETURN '⚠️ Appointment not eligible for reschedule';
    END IF;

    -- Check new slot availability
    SELECT CASE WHEN isbooked THEN 'booked' ELSE 'available' END 
    INTO v_new_slot_status 
    FROM clinicapt.doctorslot 
    WHERE slotid = p_new_slot_id;

    IF v_new_slot_status IS NULL THEN
        RETURN '❌ New slot not found';
    ELSIF v_new_slot_status = 'booked' THEN
        RETURN '⚠️ New slot is already booked';
    END IF;

    -- Cancel old appointment and free old slot
    UPDATE clinicapt.appointment 
    SET appointmentstatus = 'Cancelled' 
    WHERE appointmentid = p_appointment_id;

    UPDATE clinicapt.doctorslot 
    SET isbooked = FALSE 
    WHERE slotid = v_old_slot_id;

    -- Book new slot
    UPDATE clinicapt.doctorslot 
    SET isbooked = TRUE 
    WHERE slotid = p_new_slot_id;

    INSERT INTO clinicapt.appointment (patientid, doctorid, slotid, appointmentstatus, createdat)
    VALUES (v_patient_id, v_doctor_id, p_new_slot_id, 'Booked', NOW());

    RETURN '✅ Appointment successfully rescheduled';
END;
$$ LANGUAGE plpgsql;

-- ======================================================
-- ✅ End of Script
-- ======================================================
