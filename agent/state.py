from typing import Optional
from langgraph.graph import MessagesState

class AppointmentState(MessagesState):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None 
    ssn: Optional[str] = None
    speciality: Optional[str] = None
    insurance_company: Optional[str] = None 
    insurance_id: Optional[str] = None
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    slot_id: Optional[int] = None
    appointment_id: Optional[int] = None
    appointment_date: Optional[str] = None
    last_doctor_name: Optional[str] = None
