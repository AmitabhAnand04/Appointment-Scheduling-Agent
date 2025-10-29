## 🧩 **Simplified Database Schema (4 Tables)**

-- ==============================================
--  Appointment Scheduling Agent Database Schema
--  Compatible with Azure Database for PostgreSQL
--  Schema: clinicapt
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


---

✅ **Total Tables: 4**
Doctor | Patient | DoctorSlot | Appointment

This is normalized yet compact enough for the first version of scheduling.

---

## ⚙️ **Agent + Tools Architecture**

You’ll use **LangGraph Agent** with **tools** (not external APIs).
Each “tool” directly performs a DB operation via SQL queries (using SQLAlchemy or pyodbc).

### 🧠 LangGraph Agent

* Core orchestrator that manages conversation context and flow.
* Memory: Keeps track of patient info, doctor selection, and preferences.
* Tools: Used to query or update DB.

---

### 🧰 Tools

| Tool Name                   | Purpose                                                   |
| --------------------------- | --------------------------------------------------------- |
| `find_patient`              | Looks up existing patient by name + DOB(or anything else like phone number or SSN)                   |
| `create_patient`            | Adds new patient record                                   |
| `get_doctors_by_speciality` | Lists available doctors by specialization                 |
| `get_available_slots`       | Returns all unbooked slots for a doctor or specialization |
| `book_appointment`          | Creates an Appointment record and marks slot as booked    |
| `cancel_appointment`        | Cancels appointment (updates Appointment + frees slot)    |
| `reschedule_appointment`    | Cancels old + books new slot                              |

Each tool corresponds to a DB action.
They are called by the **agent** as it converses — not through REST API calls.

---

## 🧭 **Updated Agent Workflow**

### **1️⃣ Identify Patient**

* Ask: “Are you an existing patient or new?”
* If **existing**, collect `first_name`, `last_name`, `dob`.

  * Use `find_patient` tool to validate.
* If **new**, collect same plus `insurance info` and `last appointment's doctor name`.

  * Use `create_patient` tool to insert record.

---

### **2️⃣ Doctor Selection**

Ask:

* “Would you like to see your previous doctor, a specific doctor, or any available doctor from a particular specialty?”
* Based on reply:

  * Use `get_doctors_by_speciality` tool or retrieve previous doctor from Appointment history.

---

### **3️⃣ Slot Selection**

Ask:

* “Which date do you prefer?”
* “Morning or afternoon?”
* Use `get_available_slots(doctor_id, date, time_preference)` to fetch.

If no slots → suggest alternate times or nearby date.

---

### **4️⃣ Confirm and Book**

Once user confirms doctor and slot:

* Use `book_appointment(patient_id, doctor_id, slot_id)` tool

  * Marks slot as booked and inserts Appointment record.

Reply:
“Your appointment with Dr. Sharma (Cardiologist) is booked for 25th Oct at 10:00 AM.”

---

### **5️⃣ Cancellation or Reschedule (if requested)**

If patient says “I want to cancel my appointment”:

* Use `cancel_appointment(appointment_id)`
* If reschedule:

  * Call `cancel_appointment()` then `get_available_slots()` → `book_appointment()`

---

## 🔄 **Why Tools Instead of API**

* **Tools are local connectors** for DB or functions within LangGraph.
* Faster, no REST overhead.
* Useful for internal systems where agent directly manipulates DB.
* API layer can be added later when exposing to external clients.

---

## 📘 **Document Summary**

### **Scheduling Agent Design Document**

**Objective:**
Automate appointment scheduling between patients and doctors using an intelligent LangGraph Agent that interfaces with the clinic’s EHR scheduling system.

**Core Entities:**
Doctor, Patient, DoctorSlot, Appointment

**Agent Responsibilities:**

* Identify and register patients
* Match based on doctor or specialization
* Check real-time slot availability
* Confirm, book, cancel, or reschedule appointments

**Architecture Overview:**

* **LangGraph Agent**: Conversational logic, state management.
* **Tools**: DB operations.
* **DB**: Stores doctor, patient, slot, and appointment data.

**Workflow Summary:**

1. Identify Patient (existing/new)
2. Determine Doctor (specific/specialization/previous)
3. Find Available Slots
4. Confirm Appointment
5. Handle Cancellation/Reschedule

**Example Dialogue:**

> Agent: Are you an existing patient?
> Patient: Yes.
> Agent: Please provide your full name and date of birth.
> (Agent validates via `find_patient`)
> Agent: Would you like to meet Dr. Verma again or any available Cardiologist? (Ans:->PAtient can say things like Friday afternoon etc)
> (Agent checks `get_doctors_by_speciality`)
> Agent: I found Dr. Verma available on 25th Oct at 11 AM. Shall I book it?
> Patient: Yes.
> (Agent uses `book_appointment`)
> ✅ Appointment booked.


