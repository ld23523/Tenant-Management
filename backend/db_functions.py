import mysql.connector
from typing import List, Tuple, Optional
from datetime import date

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pass",  # <- put your MySQL password
    "database": "tenant_management",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ------------------ TENANT ------------------ #

def create_tenant(ssn: str, email: str, name: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Tenant (SSN, Email, Name) VALUES (%s, %s, %s)",
        (ssn, email, name),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_tenant(ssn: str) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SSN, Email, Name FROM Tenant WHERE SSN = %s", (ssn,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_all_tenants() -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SSN, Email, Name FROM Tenant")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def update_tenant(ssn: str, email: str, name: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Tenant SET Email = %s, Name = %s WHERE SSN = %s",
        (email, name, ssn),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_tenant(ssn: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tenant WHERE SSN = %s", (ssn,))
    conn.commit()
    cur.close()
    conn.close()


# ------------------ TENANT_PHONE ------------------ #

def add_tenant_phone(ssn: str, phone_number: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Tenant_Phone (SSN, PhoneNumber) VALUES (%s, %s)",
        (ssn, phone_number),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_phones_for_tenant(ssn: str) -> List[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT SSN, PhoneNumber FROM Tenant_Phone WHERE SSN = %s",
        (ssn,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def delete_tenant_phone(ssn: str, phone_number: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM Tenant_Phone WHERE SSN = %s AND PhoneNumber = %s",
        (ssn, phone_number),
    )
    conn.commit()
    cur.close()
    conn.close()


# ------------------ UNIT ------------------ #

def create_unit(square_feet: int, street: str, city: str, state: str, zipcode: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Unit (SquareFeet, Street, City, State, Zipcode)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (square_feet, street, city, state, zipcode),
    )
    conn.commit()
    unit_id = cur.lastrowid
    cur.close()
    conn.close()
    return unit_id


def get_unit(unit_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT UnitID, SquareFeet, Street, City, State, Zipcode FROM Unit WHERE UnitID = %s",
        (unit_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_unit(unit_id: int, square_feet: int, street: str, city: str, state: str, zipcode: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Unit
        SET SquareFeet = %s, Street = %s, City = %s, State = %s, Zipcode = %s
        WHERE UnitID = %s
        """,
        (square_feet, street, city, state, zipcode, unit_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_unit(unit_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Unit WHERE UnitID = %s", (unit_id,))
    conn.commit()
    cur.close()
    conn.close()


# ------------------ LEASE ------------------ #

def create_lease(term: str, security_deposit: float, lease_type: str,
                 active_status: str, unit_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Lease (Term, SecurityDeposit, LeaseType, ActiveStatus, UnitID)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (term, security_deposit, lease_type, active_status, unit_id),
    )
    conn.commit()
    lease_id = cur.lastrowid
    cur.close()
    conn.close()
    return lease_id


def get_lease(lease_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT LeaseID, Term, SecurityDeposit, LeaseType, ActiveStatus, UnitID FROM Lease WHERE LeaseID = %s",
        (lease_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_lease(lease_id: int, term: str, security_deposit: float, lease_type: str,
                 active_status: str, unit_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Lease
        SET Term = %s,
            SecurityDeposit = %s,
            LeaseType = %s,
            ActiveStatus = %s,
            UnitID = %s
        WHERE LeaseID = %s
        """,
        (term, security_deposit, lease_type, active_status, unit_id, lease_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_lease(lease_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Lease WHERE LeaseID = %s", (lease_id,))
    conn.commit()
    cur.close()
    conn.close()


# ------------------ INVOICEPAYMENT ------------------ #

def create_invoice(invoice_date: str, due_date: str, amount: float,
                   description: str, paid_status: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO InvoicePayment (InvoiceDate, DueDate, Amount, InvoiceDescription, PaidStatus)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (invoice_date, due_date, amount, description, paid_status),
    )
    conn.commit()
    invoice_number = cur.lastrowid
    cur.close()
    conn.close()
    return invoice_number


def get_invoice(invoice_number: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT InvoiceNumber, InvoiceDate, DueDate, Amount, InvoiceDescription, PaidStatus "
        "FROM InvoicePayment WHERE InvoiceNumber = %s",
        (invoice_number,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_invoice(invoice_number: int, invoice_date: str, due_date: str, amount: float,
                   description: str, paid_status: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE InvoicePayment
        SET InvoiceDate = %s,
            DueDate = %s,
            Amount = %s,
            InvoiceDescription = %s,
            PaidStatus = %s
        WHERE InvoiceNumber = %s
        """,
        (invoice_date, due_date, amount, description, paid_status, invoice_number),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_invoice(invoice_number: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM InvoicePayment WHERE InvoiceNumber = %s", (invoice_number,))
    conn.commit()
    cur.close()
    conn.close()


# ------------------ SERVICEREQUEST ------------------ #

def create_service_request(lease_id: int, request_id: int, status: str,
                           request_date: str, description: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO ServiceRequest (LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (lease_id, request_id, status, request_date, description),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_service_request(lease_id: int, request_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription
        FROM ServiceRequest
        WHERE LeaseID = %s AND RequestID = %s
        """,
        (lease_id, request_id),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_service_request(lease_id: int, request_id: int, status: str,
                           request_date: str, description: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE ServiceRequest
        SET RequestStatus = %s,
            RequestDate = %s,
            RequestDescription = %s
        WHERE LeaseID = %s AND RequestID = %s
        """,
        (status, request_date, description, lease_id, request_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_service_request(lease_id: int, request_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM ServiceRequest WHERE LeaseID = %s AND RequestID = %s",
        (lease_id, request_id),
    )
    conn.commit()
    cur.close()
    conn.close()


# ------------------ COVERS ------------------ #

def create_covers(lease_id: int, unit_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Covers (LeaseID, UnitID) VALUES (%s, %s)",
        (lease_id, unit_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_covers(lease_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT LeaseID, UnitID FROM Covers WHERE LeaseID = %s",
        (lease_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_covers(lease_id: int, unit_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Covers SET UnitID = %s WHERE LeaseID = %s",
        (unit_id, lease_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_covers(lease_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Covers WHERE LeaseID = %s", (lease_id,))
    conn.commit()
    cur.close()
    conn.close()


# ------------------ HOLDS ------------------ #

def create_holds(lease_id: int, ssn: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Holds (LeaseID, SSN) VALUES (%s, %s)",
        (lease_id, ssn),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_holds(lease_id: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT LeaseID, SSN FROM Holds WHERE LeaseID = %s",
        (lease_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_holds(lease_id: int, ssn: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Holds SET SSN = %s WHERE LeaseID = %s",
        (ssn, lease_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_holds(lease_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Holds WHERE LeaseID = %s", (lease_id,))
    conn.commit()
    cur.close()
    conn.close()


# ------------------ HASPAYMENT ------------------ #

def create_has_payment(invoice_number: int, lease_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO HasPayment (InvoiceNumber, LeaseID) VALUES (%s, %s)",
        (invoice_number, lease_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_has_payment(invoice_number: int) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT InvoiceNumber, LeaseID FROM HasPayment WHERE InvoiceNumber = %s",
        (invoice_number,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_has_payment(invoice_number: int, lease_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE HasPayment SET LeaseID = %s WHERE InvoiceNumber = %s",
        (lease_id, invoice_number),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_has_payment(invoice_number: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM HasPayment WHERE InvoiceNumber = %s",
        (invoice_number,),
    )
    conn.commit()
    cur.close()
    conn.close()

# ============================================================
# BUSINESS LOGIC: RENT PAYMENTS & LATE FEES
# ============================================================

def create_rent_invoice(lease_id: int, amount: float,
                        invoice_date: str, due_date: str,
                        description: str | None = None) -> int:
    """
    Create an invoice for a lease and link it in HasPayment.
    Dates are strings 'YYYY-MM-DD'.
    """
    if description is None:
        description = f"Rent for lease {lease_id} ({invoice_date})"

    conn = get_connection()
    cur = conn.cursor()

    # Insert into InvoicePayment
    cur.execute(
        """
        INSERT INTO InvoicePayment (InvoiceDate, DueDate, Amount, InvoiceDescription, PaidStatus)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (invoice_date, due_date, amount, description, "Unpaid"),
    )
    conn.commit()
    invoice_number = cur.lastrowid

    # Link to lease in HasPayment
    cur.execute(
        "INSERT INTO HasPayment (InvoiceNumber, LeaseID) VALUES (%s, %s)",
        (invoice_number, lease_id),
    )
    conn.commit()

    cur.close()
    conn.close()
    return invoice_number


def mark_invoice_paid(invoice_number: int) -> None:
    """Set an invoice to Paid."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE InvoicePayment SET PaidStatus = 'Paid' WHERE InvoiceNumber = %s",
        (invoice_number,),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_lease_payment_history(lease_id: int) -> list[tuple]:
    """
    Return all invoices for a lease (joined via HasPayment).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ip.InvoiceNumber, ip.InvoiceDate, ip.DueDate, ip.Amount,
               ip.InvoiceDescription, ip.PaidStatus
        FROM InvoicePayment ip
        JOIN HasPayment hp ON ip.InvoiceNumber = hp.InvoiceNumber
        WHERE hp.LeaseID = %s
        ORDER BY ip.InvoiceDate
        """,
        (lease_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_overdue_invoices(as_of_date: str) -> list[tuple]:
    """
    Return all unpaid invoices with DueDate < as_of_date.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ip.InvoiceNumber, ip.InvoiceDate, ip.DueDate, ip.Amount,
               ip.InvoiceDescription, ip.PaidStatus, hp.LeaseID
        FROM InvoicePayment ip
        JOIN HasPayment hp ON ip.InvoiceNumber = hp.InvoiceNumber
        WHERE ip.PaidStatus = 'Unpaid'
          AND ip.DueDate < %s
        ORDER BY ip.DueDate
        """,
        (as_of_date,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def apply_late_fees_to_overdue_invoices(flat_fee: float, as_of_date: str) -> int:
    """
    Add a flat late fee to all unpaid invoices past due.
    Returns how many invoices were updated.
    WARNING: simple logic; call once per billing cycle.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Find overdue unpaid invoices
    cur.execute(
        """
        SELECT InvoiceNumber
        FROM InvoicePayment
        WHERE PaidStatus = 'Unpaid'
          AND DueDate < %s
        """,
        (as_of_date,),
    )
    overdue = [row[0] for row in cur.fetchall()]

    # Apply late fee
    for inv in overdue:
        cur.execute(
            """
            UPDATE InvoicePayment
            SET Amount = Amount + %s
            WHERE InvoiceNumber = %s
            """,
            (flat_fee, inv),
        )

    conn.commit()
    count = len(overdue)
    cur.close()
    conn.close()
    return count


# ============================================================
# BUSINESS LOGIC: SERVICE REQUEST TRACKING
# ============================================================

def open_service_request(lease_id: int, request_date: str,
                         description: str) -> int:
    """
    Create a new service request for a lease.
    Auto-assigns the next RequestID for that LeaseID.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Find next RequestID for this lease
    cur.execute(
        "SELECT COALESCE(MAX(RequestID), 0) + 1 FROM ServiceRequest WHERE LeaseID = %s",
        (lease_id,),
    )
    next_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT INTO ServiceRequest
            (LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (lease_id, next_id, "Open", request_date, description),
    )
    conn.commit()

    cur.close()
    conn.close()
    return next_id


def close_service_request(lease_id: int, request_id: int) -> None:
    """
    Mark a service request as Closed.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE ServiceRequest
        SET RequestStatus = 'Closed'
        WHERE LeaseID = %s AND RequestID = %s
        """,
        (lease_id, request_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_open_requests_for_lease(lease_id: int) -> list[tuple]:
    """
    Get all non-closed requests for a specific lease.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription
        FROM ServiceRequest
        WHERE LeaseID = %s AND RequestStatus <> 'Closed'
        ORDER BY RequestDate
        """,
        (lease_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_all_open_requests() -> list[tuple]:
    """
    Get all open service requests across all leases.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription
        FROM ServiceRequest
        WHERE RequestStatus <> 'Closed'
        ORDER BY RequestDate
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ------------------ LATE FEES (ADV) ------------------ #

def get_late_fee_policy():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT PolicyID, GracePeriodDays, FlatLateFee
        FROM LateFeePolicy
        ORDER BY PolicyID DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def update_late_fee_policy(grace_days: int, flat_fee: float):
    conn = get_connection()
    cur = conn.cursor()

    # simplest approach: insert new policy row (keeps history)
    cur.execute(
        "INSERT INTO LateFeePolicy (GracePeriodDays, FlatLateFee) VALUES (%s, %s)",
        (grace_days, flat_fee),
    )

    conn.commit()
    cur.close()
    conn.close()


def process_late_fees():
    """
    Insert a late-fee assessment for overdue unpaid invoices,
    once per invoice per day.
    """
    policy = get_late_fee_policy()
    grace_days = int(policy["GracePeriodDays"])
    flat_fee = float(policy["FlatLateFee"])

    today = date.today()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO LateFeeAssessment (InvoiceNumber, AssessmentDate, CalculatedFee)
        SELECT i.InvoiceNumber, %s, %s
        FROM InvoicePayment i
        WHERE i.PaidStatus = 'Unpaid'
          AND i.DueDate < DATE_SUB(%s, INTERVAL %s DAY)
          AND NOT EXISTS (
              SELECT 1 FROM LateFeeAssessment l
              WHERE l.InvoiceNumber = i.InvoiceNumber
                AND l.AssessmentDate = %s
          )
        """,
        (today, flat_fee, today, grace_days, today),
    )

    conn.commit()
    cur.close()
    conn.close()


def get_all_late_fees():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT
            l.AssessmentID,
            l.InvoiceNumber,
            l.AssessmentDate,
            l.CalculatedFee,
            i.DueDate,
            i.Amount,
            i.PaidStatus,
            i.InvoiceDescription
        FROM LateFeeAssessment l
        JOIN InvoicePayment i ON i.InvoiceNumber = l.InvoiceNumber
        ORDER BY l.AssessmentDate DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
