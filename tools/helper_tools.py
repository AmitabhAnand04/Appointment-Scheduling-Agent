from typing import Optional, List, Dict, Any
from agent.state import AppointmentState
from datetime import datetime
import json

# def fill_state_tool(
#     state: AppointmentState,
#     first_name: Optional[str] = None,
#     last_name: Optional[str] = None,
#     dob: Optional[str] = None,
#     doctor_name: Optional[str] = None,
#     symptoms: Optional[str] = None,
#     appointment_date: Optional[str] = None,
# ) -> Dict[str, Any]:
#     """
#     Store or update any known information in the state.
    
#     Each parameter is optional — the tool can update a single field or multiple fields
#     depending on what information is currently available.
#     """
#     if first_name:
#         state.first_name = first_name
#     if last_name:
#         state.last_name = last_name
#     if dob:
#         state.dob = dob
#     if doctor_name:
#         state.doctor_name = doctor_name
#     if symptoms:
#         state.symptoms = symptoms
#     if appointment_date:
#         state.appointment_date = appointment_date
#     state.messages = []
    
#     return {"message": "State updated successfully", "updated_state": state}
def fill_state_tool(
    state = AppointmentState,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    dob: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None ,
    ssn: Optional[str] = None,
    speciality: Optional[str] = None,
    insurance_company: Optional[str] = None ,
    insurance_id: Optional[str] = None,
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    slot_id: Optional[int] = None,
    appointment_id: Optional[int] = None,
    appointment_date: Optional[str] = None,
    last_doctor_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Store or update any known information in the state.
    
    Each parameter is optional — the tool can update a single field or multiple fields
    depending on what information is currently available.
    """
    print("-------------Tool Called: fill_state_tool-------------")
    if first_name:
        state.first_name = first_name
    if last_name:
        state.last_name = last_name
    if dob:
        state.dob = dob
    if last_doctor_name:
        state.last_doctor_name = last_doctor_name
    if phone:
        state.phone = phone
    if email:
        state.email = email
    if ssn:
        state.ssn = ssn
    if speciality:
        state.speciality = speciality
    if insurance_company:
        state.insurance_company = insurance_company
    if insurance_id:
        state.insurance_id = insurance_id
    if patient_id:
        state.patient_id = patient_id
    if doctor_id:
        state.doctor_id = doctor_id
    if slot_id:
        state.slot_id = slot_id
    if appointment_id:
        state.appointment_id = appointment_id 
    if appointment_date:
        state.appointment_date = appointment_date
    print("-------------Tool Ended: fill_state_tool-------------")
    return {"message": "State updated successfully", "updated_state": state}


# def extract_state_tool(
#     state: AppointmentState,
#     fields: Optional[List[str]] = None
# ) -> Dict[str, Any]:
#     """
#     Retrieve specific fields or the entire state.
    
#     Args:
#         state: The shared conversation state.
#         fields: Optional list of field names to fetch. If not provided, returns all fields.
#     """
#     if not fields:
#         return {"state": state}
    
#     extracted = {k: state.get(k) for k in fields}
#     return {"requested_fields": extracted}
def extract_state_tool(
    state= AppointmentState,
    fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Retrieve specific fields or the entire state.
    
    Args:
        state: The shared conversation state (auto-injected by LangGraph).
        fields: Optional list of field names to fetch. If not provided, returns all fields.
    """
    print("-------------Tool Called: extract_state_tool-------------")
    # Convert to dict (safe way to inspect)
    state_dict = state.__dict__ if hasattr(state, "__dict__") else dict(state)

    # If no specific fields requested, return the entire state
    if not fields:
        return {"state": state_dict}

    # Otherwise extract only the requested ones
    extracted = {field: state_dict.get(field) for field in fields}
    print("-------------Tool Ended: extract_state_tool-------------")
    return {"requested_fields": extracted}

def get_current_datetime_tool() -> str:
    """
    Fetches the current date and time. Use this when the user's query 
    depends on the current time (e.g., 'What is the date today?', 'next five days', etc.).
    The time is returned in 'YYYY-MM-DD HH:MM:SS' format.
    """
    print("-------------Tool Called: get_current_datetime_tool-------------")
    now = datetime.now()
    print("-------------Tool Ended: get_current_datetime_tool-------------")
    return now.strftime("%Y-%m-%d %H:%M:%S")

