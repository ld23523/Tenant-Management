-- schema.sql
CREATE DATABASE IF NOT EXISTS tenant_management;
USE tenant_management;

-- Tenant
CREATE TABLE Tenant (
    SSN   CHAR(9)       NOT NULL,
    Email VARCHAR(100)  NOT NULL,
    Name  VARCHAR(100)  NOT NULL,
    PRIMARY KEY (SSN)
);

-- Tenant_Phone (references Tenant)
CREATE TABLE Tenant_Phone (
    SSN         CHAR(9)      NOT NULL,
    PhoneNumber VARCHAR(20)  NOT NULL,
    PRIMARY KEY (SSN, PhoneNumber),
    FOREIGN KEY (SSN) REFERENCES Tenant(SSN)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Unit
CREATE TABLE Unit (
    UnitID      INT          NOT NULL AUTO_INCREMENT,
    SquareFeet  INT          NOT NULL,
    Street      VARCHAR(100) NOT NULL,
    City        VARCHAR(100) NOT NULL,
    State       CHAR(2)      NOT NULL,
    Zipcode     VARCHAR(10)  NOT NULL,
    PRIMARY KEY (UnitID)
);

-- Lease (references Unit)
CREATE TABLE Lease (
    LeaseID         INT           NOT NULL AUTO_INCREMENT,
    Term            VARCHAR(50)   NOT NULL,
    SecurityDeposit DECIMAL(10,2) NOT NULL,
    LeaseType       VARCHAR(50)   NOT NULL,
    ActiveStatus    VARCHAR(20)   NOT NULL,
    UnitID          INT           NOT NULL,
    PRIMARY KEY (LeaseID),
    FOREIGN KEY (UnitID) REFERENCES Unit(UnitID)
);

-- InvoicePayment
CREATE TABLE InvoicePayment (
    InvoiceNumber      INT           NOT NULL AUTO_INCREMENT,
    InvoiceDate        DATE          NOT NULL,
    DueDate            DATE          NOT NULL,
    Amount             DECIMAL(10,2) NOT NULL,
    InvoiceDescription VARCHAR(255)  NOT NULL,
    PaidStatus         VARCHAR(20)   NOT NULL,
    PRIMARY KEY (InvoiceNumber)
);

-- ServiceRequest (references Lease)
CREATE TABLE ServiceRequest (
    LeaseID            INT           NOT NULL,
    RequestID          INT           NOT NULL,
    RequestStatus      VARCHAR(20)   NOT NULL,
    RequestDate        DATE          NOT NULL,
    RequestDescription VARCHAR(255)  NOT NULL,
    PRIMARY KEY (LeaseID, RequestID),
    FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID)
);

-- Covers (references Lease, Unit)
CREATE TABLE Covers (
    LeaseID INT NOT NULL,
    UnitID  INT NOT NULL,
    PRIMARY KEY (LeaseID),
    FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID),
    FOREIGN KEY (UnitID)  REFERENCES Unit(UnitID)
);

-- Holds (references Lease, Tenant)
CREATE TABLE Holds (
    LeaseID INT     NOT NULL,
    SSN     CHAR(9) NOT NULL,
    PRIMARY KEY (LeaseID),
    FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID),
    FOREIGN KEY (SSN)     REFERENCES Tenant(SSN)
);

-- HasPayment (references InvoicePayment, Lease)
CREATE TABLE HasPayment (
    InvoiceNumber INT NOT NULL,
    LeaseID       INT NOT NULL,
    PRIMARY KEY (InvoiceNumber),
    FOREIGN KEY (InvoiceNumber) REFERENCES InvoicePayment(InvoiceNumber),
    FOREIGN KEY (LeaseID)       REFERENCES Lease(LeaseID)
);
