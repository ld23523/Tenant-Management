-- sample_data.sql
USE tenant_management;

-- TENANT Data
INSERT INTO Tenant (SSN, Email, Name) VALUES
('123456789', 'alice.nguyen@example.com', 'Alice Nguyen'),
('987654321', 'bob.tran@example.com', 'Bob Tran'),
('555443333', 'carol.lee@example.com', 'Carol Lee');

-- TENANT_PHONE Data
INSERT INTO Tenant_Phone (SSN, PhoneNumber) VALUES
('123456789', '404-555-1000'),
('123456789', '404-555-1001'),
('987654321', '678-555-2000'),
('555443333', '770-555-3000');

-- UNIT Data
INSERT INTO Unit (UnitID, SquareFeet, Street, City, State, Zipcode) VALUES
(1, 850,  '123 Peach St',  'Atlanta', 'GA', '30301'),
(2, 1100, '45 Oak Lane',   'Duluth',  'GA', '30096'),
(3, 650,  '789 Pine Ave',  'Norcross','GA', '30071');

-- LEASE Data
INSERT INTO Lease (LeaseID, Term, SecurityDeposit, LeaseType, ActiveStatus, UnitID) VALUES
(1, '12 months', 1200.00, 'Residential', 'Active',   1),
(2, '6 months',   800.00, 'Residential', 'Active',   2),
(3, '12 months', 1500.00, 'Commercial',  'Inactive', 3);

-- INVOICEPAYMENT Data
INSERT INTO InvoicePayment (InvoiceNumber, InvoiceDate, DueDate, Amount, InvoiceDescription, PaidStatus) VALUES
(1, '2025-11-01', '2025-11-05', 1200.00, 'November rent - Unit 1',   'Paid'),
(2, '2025-11-01', '2025-11-05',  800.00, 'November rent - Unit 2',   'Unpaid'),
(3, '2025-10-01', '2025-10-05', 1500.00, 'October rent - Unit 3',    'Paid');

-- SERVICEREQUEST Data
INSERT INTO ServiceRequest (LeaseID, RequestID, RequestStatus, RequestDate, RequestDescription) VALUES
(1, 1, 'Open',   '2025-11-02', 'Leaking faucet in bathroom'),
(1, 2, 'Closed', '2025-10-15', 'AC filter replacement'),
(2, 1, 'Open',   '2025-11-03', 'Dishwasher not working');

-- COVERS Data (LeaseID -> UnitID)
INSERT INTO Covers (LeaseID, UnitID) VALUES
(1, 1),
(2, 2),
(3, 3);

-- HOLDS Data (LeaseID -> SSN)
INSERT INTO Holds (LeaseID, SSN) VALUES
(1, '123456789'),
(2, '987654321'),
(3, '555443333');

-- HASPAYMENT Data (InvoiceNumber -> LeaseID)
INSERT INTO HasPayment (InvoiceNumber, LeaseID) VALUES
(1, 1),
(2, 2),
(3, 3);

-- LATE FEE POLICY DEFAULT
INSERT INTO LateFeePolicy (GracePeriodDays, FlatLateFee)
VALUES (5, 50.00);
