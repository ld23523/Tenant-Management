from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pass",   # your password
    "database": "tenant_management",
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- existing /tenants routes here ----------------
# GET /tenants
@app.route("/tenants", methods=["GET"])
def get_tenants():
    search = request.args.get("search", "").lower().strip()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Name AS name, Email AS email, SSN AS ssn FROM Tenant")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if search:
        rows = [
            r for r in rows
            if search in r["name"].lower()
            or search in r["email"].lower()
            or search in r["ssn"]
        ]

    return jsonify(rows)

# POST /tenants
@app.route("/tenants", methods=["POST"])
def add_tenant():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    ssn = data.get("ssn")

    if not name or not email or not ssn:
        return jsonify({"error": "name, email, and ssn are required"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Tenant (SSN, Email, Name) VALUES (%s, %s, %s)",
            (ssn, email, name),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Tenant created"}), 201
    except Exception as e:
        print("DB error (POST /tenants):", e)
        return jsonify({"error": str(e)}), 500

# PUT /tenants/<ssn>
@app.route("/tenants/<ssn>", methods=["PUT"])
def update_tenant(ssn):
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Tenant SET Email = %s, Name = %s WHERE SSN = %s",
            (email, name, ssn),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Tenant updated"}), 200
    except Exception as e:
        print("DB error (PUT /tenants):", e)
        return jsonify({"error": str(e)}), 500

# DELETE /tenants/<ssn>
@app.route("/tenants/<ssn>", methods=["DELETE"])
def delete_tenant(ssn):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Tenant WHERE SSN = %s", (ssn,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Tenant deleted"}), 200
    except Exception as e:
        print("DB error (DELETE /tenants):", e)
        return jsonify({"error": str(e)}), 500

# ======================================================
# NEW: GET /tenants/<ssn>/details -> tenant + lease + unit
# ======================================================
@app.route("/tenants/<ssn>/details", methods=["GET"])
def tenant_details(ssn):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            t.SSN,
            t.Name,
            t.Email,
            l.LeaseID,
            l.Term,
            l.SecurityDeposit,
            l.LeaseType,
            l.ActiveStatus,
            u.UnitID,
            u.SquareFeet,
            u.Street,
            u.City,
            u.State,
            u.Zipcode
        FROM Tenant t
        LEFT JOIN Holds h ON t.SSN = h.SSN
        LEFT JOIN Lease l ON h.LeaseID = l.LeaseID
        LEFT JOIN Unit  u ON l.UnitID = u.UnitID
        WHERE t.SSN = %s
        """,
        (ssn,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return jsonify({"error": "Tenant not found"}), 404

    first = rows[0]
    tenant = {
        "ssn": first[0],
        "name": first[1],
        "email": first[2],
        "leases": [],
    }

    for (
        ssn_val,
        name,
        email,
        lease_id,
        term,
        security_deposit,
        lease_type,
        active_status,
        unit_id,
        square_feet,
        street,
        city,
        state,
        zipcode,
    ) in rows:
        if lease_id is None:
            continue

        tenant["leases"].append(
            {
                "leaseId": lease_id,
                "term": term,
                "securityDeposit": float(security_deposit),
                "leaseType": lease_type,
                "status": active_status,
                "unitId": unit_id,
                "squareFeet": square_feet,
                "address": f"{street}, {city}, {state} {zipcode}",
                "street": street,
                "city": city,
                "state": state,
                "zipcode": zipcode,
            }
        )

    return jsonify(tenant), 200
@app.route("/leases/<int:lease_id>", methods=["PUT"])
def update_lease_and_unit(lease_id):
    """
    Expects JSON:
    {
      "term": "...",
      "securityDeposit": 1200.0,
      "leaseType": "Residential",
      "status": "Active",
      "unit": {
        "unitId": 1,
        "squareFeet": 900,
        "street": "123 Peach St",
        "city": "Atlanta",
        "state": "GA",
        "zipcode": "30301"
      }
    }
    """
    data = request.get_json() or {}

    term = data.get("term")
    security_deposit = data.get("securityDeposit")
    lease_type = data.get("leaseType")
    status = data.get("status")
    unit = data.get("unit") or {}

    unit_id = unit.get("unitId")
    square_feet = unit.get("squareFeet")
    street = unit.get("street")
    city = unit.get("city")
    state = unit.get("state")
    zipcode = unit.get("zipcode")

    if not all([term, lease_type, status, unit_id, street, city, state, zipcode]):
        return jsonify({"error": "Missing required lease/unit fields"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Update Lease
        cur.execute(
            """
            UPDATE Lease
            SET Term = %s,
                SecurityDeposit = %s,
                LeaseType = %s,
                ActiveStatus = %s
            WHERE LeaseID = %s
            """,
            (term, security_deposit, lease_type, status, lease_id),
        )

        # Update Unit
        cur.execute(
            """
            UPDATE Unit
            SET SquareFeet = %s,
                Street = %s,
                City = %s,
                State = %s,
                Zipcode = %s
            WHERE UnitID = %s
            """,
            (square_feet, street, city, state, zipcode, unit_id),
        )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Lease and unit updated"}), 200

    except Exception as e:
        print("DB error (PUT /leases):", e)
        return jsonify({"error": str(e)}), 500
@app.route("/leases/<int:lease_id>", methods=["DELETE"])
def delete_lease(lease_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Delete child rows first (due to foreign keys)
        cur.execute("DELETE FROM ServiceRequest WHERE LeaseID = %s", (lease_id,))
        cur.execute("DELETE FROM Covers        WHERE LeaseID = %s", (lease_id,))
        cur.execute("DELETE FROM Holds         WHERE LeaseID = %s", (lease_id,))
        cur.execute("DELETE FROM HasPayment    WHERE LeaseID = %s", (lease_id,))

        # Finally delete the lease itself
        cur.execute("DELETE FROM Lease WHERE LeaseID = %s", (lease_id,))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Lease deleted"}), 200

    except Exception as e:
        print("DB error (DELETE /leases):", e)
        return jsonify({"error": str(e)}), 500
@app.route("/tenants/<ssn>/leases", methods=["POST"])
def create_lease_for_tenant(ssn):
    """
    Expects JSON:
    {
      "term": "12 months",
      "securityDeposit": 1200.0,
      "leaseType": "Residential",
      "status": "Active",
      "squareFeet": 850,
      "street": "123 Peach St",
      "city": "Atlanta",
      "state": "GA",
      "zipcode": "30301"
    }
    """
    data = request.get_json() or {}

    term = data.get("term")
    security_deposit = data.get("securityDeposit")
    lease_type = data.get("leaseType")
    status = data.get("status")
    square_feet = data.get("squareFeet")
    street = data.get("street")
    city = data.get("city")
    state = data.get("state")
    zipcode = data.get("zipcode")

    if not all([term, lease_type, status, square_feet, street, city, state, zipcode]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Make sure tenant exists
        cur.execute("SELECT 1 FROM Tenant WHERE SSN = %s", (ssn,))
        if cur.fetchone() is None:
            cur.close()
            conn.close()
            return jsonify({"error": "Tenant not found"}), 404

        # Create Unit
        cur.execute(
            """
            INSERT INTO Unit (SquareFeet, Street, City, State, Zipcode)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (square_feet, street, city, state, zipcode),
        )
        conn.commit()
        unit_id = cur.lastrowid

        # Create Lease
        cur.execute(
            """
            INSERT INTO Lease (Term, SecurityDeposit, LeaseType, ActiveStatus, UnitID)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (term, security_deposit, lease_type, status, unit_id),
        )
        conn.commit()
        lease_id = cur.lastrowid

        # Link in Holds
        cur.execute(
            "INSERT INTO Holds (LeaseID, SSN) VALUES (%s, %s)",
            (lease_id, ssn),
        )
        conn.commit()

        cur.close()
        conn.close()

        new_lease = {
            "leaseId": lease_id,
            "term": term,
            "securityDeposit": float(security_deposit) if security_deposit is not None else 0.0,
            "leaseType": lease_type,
            "status": status,
            "unitId": unit_id,
            "squareFeet": square_feet,
            "address": f"{street}, {city}, {state} {zipcode}",
            "street": street,
            "city": city,
            "state": state,
            "zipcode": zipcode,
        }

        return jsonify(new_lease), 201

    except Exception as e:
        print("DB error (POST /tenants/<ssn>/leases):", e)
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(debug=True)
