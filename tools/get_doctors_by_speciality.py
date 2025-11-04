# from db.connection import get_connection

# def get_doctors_by_speciality(speciality):
#     conn = get_connection()
#     cur = conn.cursor()

#     query = """
#         SELECT doctorid, firstname, lastname, specialization
#         FROM clinicapt.doctor
#         WHERE specialization ILIKE %s AND status = 'Active';
#     """
#     cur.execute(query, (f"%{speciality}%",))
#     doctors = cur.fetchall()

#     cur.close()
#     conn.close()
#     return doctors

from db.connection import get_connection

# def search_doctors(speciality=None, name=None):
#     """
#     Search for active doctors by specialization, name, or both.

#     Args:
#         speciality (str, optional): Doctor's specialization (e.g., 'Cardiologist', 'Dermatologist').
#         name (str, optional): Full or partial name of the doctor to match first or last name.

#     Returns:
#         list: A list of doctors containing DoctorID, FirstName, LastName, and Specialization.
#     """
#     print("-------------Tool Called: search_doctors-------------")
#     conn = get_connection()
#     cur = conn.cursor()

#     # Base query
#     query = """
#         SELECT doctorid, firstname, lastname, specialization
#         FROM clinicapt.doctor
#         WHERE status = 'Active'
#     """
    
#     # List to hold dynamic WHERE clauses and parameters
#     where_clauses = []
#     params = []

#     # Check and add specialty search condition
#     if speciality:
#         where_clauses.append("specialization ILIKE %s")
#         params.append(f"%{speciality}%")

#     # Check and add name search condition
#     if name:
#         # Wildcard search across both first name OR last name
#         where_clauses.append("(firstname ILIKE %s OR lastname ILIKE %s)")
#         params.append(f"%{name}%")
#         params.append(f"%{name}%")

#     # Append WHERE clauses to the query if any exist
#     if where_clauses:
#         query += " AND " + " AND ".join(where_clauses)
    
#     # Finalize the query (optional: add ORDER BY)
#     query += ";"
#     print("Final Query:", query)
#     # Execute the query with the constructed parameters
#     cur.execute(query, tuple(params))
#     doctors = cur.fetchall()

#     cur.close()
#     conn.close()
#     print("-------------Tool Ended: search_doctors-------------")
#     return doctors


def search_doctors(speciality=None, name=None):
    """
    Search for active doctors by specialization, name, or both.

    Args:
        speciality (str, optional): Doctor's specialization (e.g., 'Cardiologist', 'Dermatologist').
        name (str, optional): Full or partial name of the doctor to match first or last name.

    Returns:
        list: A list of doctors containing DoctorID, FirstName, LastName, and Specialization.
    """
    print("-------------Tool Called: search_doctors-------------")
    conn = get_connection()
    cur = conn.cursor()

    # Base query
    query = """
        SELECT doctorid, firstname, lastname, specialization
        FROM clinicapt.doctor
        WHERE status = 'Active'
    """

    where_clauses = []
    params = []

    # Add specialization filter
    if speciality:
        where_clauses.append("specialization ILIKE %s")
        params.append(f"%{speciality}%")

    # Add name filter
    if name:
        name_parts = [part.strip() for part in name.split() if part.strip()]
        for part in name_parts:
            # For each name part, check if it exists in firstname OR lastname
            where_clauses.append("(firstname ILIKE %s OR lastname ILIKE %s)")
            params.extend([f"%{part}%", f"%{part}%"])

    # Combine all filters
    if where_clauses:
        query += " AND " + " AND ".join(where_clauses)

    query += ";"
    print("Final Query:", query)
    print("With Params:", params)

    cur.execute(query, tuple(params))
    doctors = cur.fetchall()

    cur.close()
    conn.close()
    print("-------------Tool Ended: search_doctors-------------")
    return doctors
