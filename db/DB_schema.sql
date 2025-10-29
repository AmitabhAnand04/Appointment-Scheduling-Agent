-- ==============================================
--  Appointment Scheduling Agent Database Schema
--  Compatible with Azure Database for PostgreSQL
--  Schema: clinicapt
--  Author: Amitabh Anand
-- ==============================================

-- Create schema (if not exists)
CREATE SCHEMA IF NOT EXISTS clinicapt;

-- ==============================================
-- 1. Doctor Table
-- ==============================================
CREATE TABLE IF NOT EXISTS clinicapt.Doctor (
    DoctorID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Specialization VARCHAR(100) NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Active'   -- Active / Inactive
);

-- ==============================================
-- 2. Patient Table
-- ==============================================
CREATE TABLE IF NOT EXISTS clinicapt.Patient (
    PatientID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DateOfBirth DATE NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,   -- Filled at registration
    Email VARCHAR(100),                 -- Optional, filled later
    SSN VARCHAR(15),                    -- Optional, filled later
    InsuranceCompany VARCHAR(100),
    InsuranceID VARCHAR(50)
);

-- ==============================================
-- 3. DoctorSlot Table
-- ==============================================
CREATE TABLE IF NOT EXISTS clinicapt.DoctorSlot (
    SlotID SERIAL PRIMARY KEY,
    DoctorID INT NOT NULL REFERENCES clinicapt.Doctor(DoctorID) ON DELETE CASCADE,
    SlotDate DATE NOT NULL,
    SlotStartTime TIME NOT NULL,
    SlotEndTime TIME NOT NULL,
    IsBooked BOOLEAN NOT NULL DEFAULT FALSE
);

-- ==============================================
-- 4. Appointment Table
-- ==============================================
CREATE TABLE IF NOT EXISTS clinicapt.Appointment (
    AppointmentID SERIAL PRIMARY KEY,
    PatientID INT NOT NULL REFERENCES clinicapt.Patient(PatientID) ON DELETE CASCADE,
    DoctorID INT NOT NULL REFERENCES clinicapt.Doctor(DoctorID) ON DELETE CASCADE,
    SlotID INT NOT NULL REFERENCES clinicapt.DoctorSlot(SlotID) ON DELETE CASCADE,
    AppointmentStatus VARCHAR(20) NOT NULL DEFAULT 'Booked',  -- Booked / Cancelled / Rescheduled
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================
-- Indexes for faster lookup
-- ==============================================
CREATE INDEX IF NOT EXISTS idx_doctor_specialization ON clinicapt.Doctor(Specialization);
CREATE INDEX IF NOT EXISTS idx_patient_dob ON clinicapt.Patient(DateOfBirth);
CREATE INDEX IF NOT EXISTS idx_slot_date ON clinicapt.DoctorSlot(SlotDate);
CREATE INDEX IF NOT EXISTS idx_appointment_status ON clinicapt.Appointment(AppointmentStatus);

-- ==============================================
-- Done ✅
-- ==============================================




-- ==============================================
-- Sample Data for Appointment Scheduling Agent
-- Schema: clinicapt
-- ==============================================

-- ===== Insert Doctors =====
INSERT INTO clinicapt.Doctor (FirstName, LastName, Specialization, Status)
VALUES
('John', 'Carter', 'Cardiologist', 'Active'),
('Emily', 'Stone', 'Dermatologist', 'Active'),
('Raj', 'Patel', 'Orthopedic Surgeon', 'Active'),
('Sophia', 'Kim', 'Pediatrician', 'Inactive');

-- ===== Insert Patients =====
INSERT INTO clinicapt.Patient (FirstName, LastName, DateOfBirth, PhoneNumber, Email, SSN, InsuranceCompany, InsuranceID)
VALUES
('Amit', 'Anand', '1998-03-12', '9876543210', 'amit.anand@example.com', 'SSN12345', 'Aetna', 'AIN56789'),
('Sarah', 'Williams', '1985-07-25', '9998887776', 'sarah.w@example.com', 'SSN45678', 'BlueCross', 'BC12345'),
('Liam', 'Johnson', '2001-11-05', '8887776665', NULL, NULL, 'UnitedHealth', 'UH99887');

-- ===== Insert Doctor Slots =====
-- Dr. John Carter (Cardiologist)
INSERT INTO clinicapt.DoctorSlot (DoctorID, SlotDate, SlotStartTime, SlotEndTime, IsBooked)
VALUES
(1, '2025-10-25', '09:00', '09:30', FALSE),
(1, '2025-10-25', '09:30', '10:00', FALSE),
(1, '2025-10-25', '10:00', '10:30', TRUE),  -- already booked
(1, '2025-10-26', '11:00', '11:30', FALSE);

-- Dr. Emily Stone (Dermatologist)
INSERT INTO clinicapt.DoctorSlot (DoctorID, SlotDate, SlotStartTime, SlotEndTime, IsBooked)
VALUES
(2, '2025-10-25', '13:00', '13:30', FALSE),
(2, '2025-10-25', '13:30', '14:00', FALSE),
(2, '2025-10-26', '14:00', '14:30', TRUE);

-- Dr. Raj Patel (Orthopedic)
INSERT INTO clinicapt.DoctorSlot (DoctorID, SlotDate, SlotStartTime, SlotEndTime, IsBooked)
VALUES
(3, '2025-10-27', '15:00', '15:30', FALSE),
(3, '2025-10-27', '15:30', '16:00', FALSE),
(3, '2025-10-28', '10:00', '10:30', FALSE);

-- ===== Insert Appointments =====
-- Book one slot for Amit Anand with Dr. John Carter
INSERT INTO clinicapt.Appointment (PatientID, DoctorID, SlotID, AppointmentStatus)
VALUES
(1, 1, 3, 'Booked');  -- SlotID 3 was marked booked above

-- Book one slot for Sarah with Dr. Emily Stone
INSERT INTO clinicapt.Appointment (PatientID, DoctorID, SlotID, AppointmentStatus)
VALUES
(2, 2, 7, 'Booked');  -- SlotID 7 was marked booked above

-- ==============================================
-- ✅ Sample Data Inserted
-- ==============================================