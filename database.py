import mysql.connector

# 1. Connect to MySQL server (no database selected yet)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword"   # <- put your MySQL password
)

cur = conn.cursor()

# 2. Drop and recreate database to start clean
cur.execute("DROP DATABASE IF EXISTS tenant_management")
cur.execute("CREATE DATABASE tenant_management")
cur.execute("USE tenant_management")

# 3. TABLES (order matters: parents first, then children)

# Tenant
cur.execute("""
    CREATE TABLE Tenant (
        SSN   CHAR(9)       NOT NULL,
        Email VARCHAR(100)  NOT NULL,
        Name  VARCHAR(100)  NOT NULL,
        PRIMARY KEY (SSN)
    )
""")

# Tenant_Phone (references Tenant)
cur.execute("""
    CREATE TABLE Tenant_Phone (
        SSN         CHAR(9)      NOT NULL,
        PhoneNumber VARCHAR(20)  NOT NULL,
        PRIMARY KEY (SSN, PhoneNumber),
        FOREIGN KEY (SSN) REFERENCES Tenant(SSN)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    )
""")

# Unit
cur.execute("""
    CREATE TABLE Unit (
        UnitID      INT          NOT NULL AUTO_INCREMENT,
        SquareFeet  INT          NOT NULL,
        Street      VARCHAR(100) NOT NULL,
        City        VARCHAR(100) NOT NULL,
        State       CHAR(2)      NOT NULL,
        Zipcode     VARCHAR(10)  NOT NULL,
        PRIMARY KEY (UnitID)
    )
""")

# Lease (references Unit)
cur.execute("""
    CREATE TABLE Lease (
        LeaseID         INT           NOT NULL AUTO_INCREMENT,
        Term            VARCHAR(50)   NOT NULL,
        SecurityDeposit DECIMAL(10,2) NOT NULL,
        LeaseType       VARCHAR(50)   NOT NULL,
        ActiveStatus    VARCHAR(20)   NOT NULL,
        UnitID          INT           NOT NULL,
        PRIMARY KEY (LeaseID),
        FOREIGN KEY (UnitID) REFERENCES Unit(UnitID)
    )
""")

# InvoicePayment
cur.execute("""
    CREATE TABLE InvoicePayment (
        InvoiceNumber      INT           NOT NULL AUTO_INCREMENT,
        InvoiceDate        DATE          NOT NULL,
        DueDate            DATE          NOT NULL,
        Amount             DECIMAL(10,2) NOT NULL,
        InvoiceDescription VARCHAR(255)  NOT NULL,
        PaidStatus         VARCHAR(20)   NOT NULL,
        PRIMARY KEY (InvoiceNumber)
    )
""")

# ServiceRequest (references Lease)
cur.execute("""
    CREATE TABLE ServiceRequest (
        LeaseID            INT           NOT NULL,
        RequestID          INT           NOT NULL,
        RequestStatus      VARCHAR(20)   NOT NULL,
        RequestDate        DATE          NOT NULL,
        RequestDescription VARCHAR(255)  NOT NULL,
        PRIMARY KEY (LeaseID, RequestID),
        FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID)
    )
""")

# Covers (references Lease, Unit)
cur.execute("""
    CREATE TABLE Covers (
        LeaseID INT NOT NULL,
        UnitID  INT NOT NULL,
        PRIMARY KEY (LeaseID),
        FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID),
        FOREIGN KEY (UnitID)  REFERENCES Unit(UnitID)
    )
""")

# Holds (references Lease, Tenant)
cur.execute("""
    CREATE TABLE Holds (
        LeaseID INT     NOT NULL,
        SSN     CHAR(9) NOT NULL,
        PRIMARY KEY (LeaseID),
        FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID),
        FOREIGN KEY (SSN)     REFERENCES Tenant(SSN)
    )
""")

# HasPayment (references InvoicePayment, Lease)
cur.execute("""
    CREATE TABLE HasPayment (
        InvoiceNumber INT NOT NULL,
        LeaseID       INT NOT NULL,
        PRIMARY KEY (InvoiceNumber),
        FOREIGN KEY (InvoiceNumber) REFERENCES InvoicePayment(InvoiceNumber),
        FOREIGN KEY (LeaseID)       REFERENCES Lease(LeaseID)
    )
""")

print(" Database and all tables created successfully.")

# ---------- TENANT ----------
tenants = [
    ("123456789", "alice.nguyen@example.com", "Alice Nguyen"),
    ("987654321", "bob.tran@example.com", "Bob Tran"),
    ("555443333", "carol.lee@example.com", "Carol Lee")
]

cur.executemany(
    "INSERT INTO Tenant (SSN, Email, Name) VALUES (%s, %s, %s) "
    "ON DUPLICATE KEY UPDATE Email = VALUES(Email), Name = VALUES(Name)",
    tenants
)

# ---------- TENANT_PHONE ----------
tenant_phones = [
    ("123456789", "404-555-1000"),
    ("123456789", "404-555-1001"),
    ("987654321", "678-555-2000"),
    ("555443333", "770-555-3000")
]

cur.executemany(
    "INSERT INTO Tenant_Phone (SSN, PhoneNumber) VALUES (%s, %s) "
    "ON DUPLICATE KEY UPDATE PhoneNumber = PhoneNumber",
    tenant_phones
)

# ---------- UNIT ----------
units = [
    (1, 850,  "123 Peach St",  "Atlanta", "GA", "30301"),
    (2, 1100, "45 Oak Lane",   "Duluth",  "GA", "30096"),
    (3, 650,  "789 Pine Ave",  "Norcross","GA", "30071")
]

cur.executemany(
    "INSERT INTO Unit (UnitID, SquareFeet, Street, City, State, Zipcode) "
    "VALUES (%s, %s, %s, %s, %s, %s) "
    "ON DUPLICATE KEY UPDATE SquareFeet = VALUES(SquareFeet)",
    units
)

# ---------- LEASE ----------
leases = [
    (1, "12 months", 1200.00, "Residential", "Active",   1),
    (2, "6 months",   800.00, "Residential", "Active",   2),
    (3, "12 months", 1500.00, "Commercial",  "Inactive", 3)
]

cur.executemany(
    "INSERT INTO Lease (LeaseID, Term, SecurityDeposit, LeaseType, ActiveStatus, UnitID) "
    "VALUES (%s, %s, %s, %s, %s, %s) "
    "ON DUPLICATE KEY UPDATE ActiveStatus = VALUES(ActiveStatus)",
    leases
)

# ---------- INVOICEPAYMENT ----------
invoices = [
    (1, "2025-11-01", "2025-11-05", 1200.00, "November rent - Unit 1",   "Paid"),
    (2, "2025-11-01", "2025-11-05",  800.00, "November rent - Unit 2",   "Unpaid"),
    (3, "2025-10-01", "2025-10-05", 1500.00, "October rent - Unit 3",    "Paid")
]

cur.executemany(
    "INSERT INTO InvoicePayment (InvoiceNumber, InvoiceDate, DueDate, Amount, InvoiceDescription, PaidStatus) "
    "VALUES (%s, %s, %s, %s, %s, %s) "
    "ON DUPLICATE KEY UPDATE PaidStatus = VALUES(PaidStatus)",
    invoices
)

# ---------- SERVICEREQUEST ----------
service_requests = [
    (1, 1, "Open",   "2025-11-02", "Leaking faucet in bathroom"),
    (1, 2, "Closed", "2025-10-15", "AC filter replacement"),
    (2, 1, "Open",   "2025-11-03", "Dishwasher not working")
]

cur.executemany(
    "INSERT INTO ServiceRequest (LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription) "
    "VALUES (%s, %s, %s, %s, %s) "
    "ON DUPLICATE KEY UPDATE RequestStatus = VALUES(RequestStatus)",
    service_requests
)

# ---------- COVERS (LeaseID -> UnitID) ----------
covers = [
    (1, 1),
    (2, 2),
    (3, 3)
]

cur.executemany(
    "INSERT INTO Covers (LeaseID, UnitID) VALUES (%s, %s) "
    "ON DUPLICATE KEY UPDATE UnitID = VALUES(UnitID)",
    covers
)

# ---------- HOLDS (LeaseID -> SSN) ----------
holds = [
    (1, "123456789"),
    (2, "987654321"),
    (3, "555443333")
]

cur.executemany(
    "INSERT INTO Holds (LeaseID, SSN) VALUES (%s, %s) "
    "ON DUPLICATE KEY UPDATE SSN = VALUES(SSN)",
    holds
)

# ---------- HASPAYMENT (InvoiceNumber -> LeaseID) ----------
has_payment = [
    (1, 1),
    (2, 2),
    (3, 3)
]

cur.executemany(
    "INSERT INTO HasPayment (InvoiceNumber, LeaseID) VALUES (%s, %s) "
    "ON DUPLICATE KEY UPDATE LeaseID = VALUES(LeaseID)",
    has_payment
)

conn.commit()

print(" Sample data inserted successfully.")

cur.close()
conn.close()
