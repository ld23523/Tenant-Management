// Tenants.jsx
import { useEffect, useState } from "react";

function Tenants() {
  const [tenants, setTenants] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const [selectedTenant, setSelectedTenant] = useState(null);
  const [details, setDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [errorDetails, setErrorDetails] = useState("");

  // NEW: lease edit / add state
  const [editingLeaseId, setEditingLeaseId] = useState(null);
  const [leaseEditForm, setLeaseEditForm] = useState({
    term: "",
    securityDeposit: "",
    leaseType: "",
    status: "",
    squareFeet: "",
    street: "",
    city: "",
    state: "",
    zipcode: "",
  });

  const [showNewLeaseForm, setShowNewLeaseForm] = useState(false);
  const [newLeaseForm, setNewLeaseForm] = useState({
    term: "",
    securityDeposit: "",
    leaseType: "",
    status: "Active",
    squareFeet: "",
    street: "",
    city: "",
    state: "",
    zipcode: "",
  });

  // Load tenants from backend
  const loadTenants = () => {
    setLoading(true);

    fetch("http://127.0.0.1:5000/tenants")
      .then((res) => res.json())
      .then((data) => {
        setTenants(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching tenants:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadTenants();
  }, []);

  // --- Search / filter on frontend ---
  const filteredTenants = tenants.filter((t) => {
    const term = search.toLowerCase();
    return (
      t.name.toLowerCase().includes(term) ||
      t.email.toLowerCase().includes(term) ||
      t.ssn.includes(term)
    );
  });

  // --- Delete tenant ---
  const handleDelete = async (ssn) => {
    if (!window.confirm("Delete this tenant?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:5000/tenants/${ssn}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        const text = await res.text();
        alert(`Error deleting: ${res.status} ${text}`);
        return;
      }

      setTenants((prev) => prev.filter((t) => t.ssn !== ssn));

      // If the deleted tenant was selected, clear details
      if (selectedTenant && selectedTenant.ssn === ssn) {
        setSelectedTenant(null);
        setDetails(null);
        setErrorDetails("");
        setEditingLeaseId(null);
        setShowNewLeaseForm(false);
      }
    } catch (err) {
      console.error("Delete error:", err);
      alert("Network error deleting tenant");
    }
  };

  // --- Edit tenant (name/email) ---
  const handleEdit = async (tenant) => {
    const newName = window.prompt("New name:", tenant.name);
    if (!newName) return;

    const newEmail = window.prompt("New email:", tenant.email);
    if (!newEmail) return;

    try {
      const res = await fetch(`http://127.0.0.1:5000/tenants/${tenant.ssn}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: newName,
          email: newEmail,
        }),
      });

      const text = await res.text();
      console.log("PUT /tenants ->", res.status, text);

      if (!res.ok) {
        alert(`Error updating tenant: ${res.status} ${text}`);
        return;
      }

      setTenants((prev) =>
        prev.map((t) =>
          t.ssn === tenant.ssn ? { ...t, name: newName, email: newEmail } : t
        )
      );

      // also update details panel if this tenant is selected
      if (selectedTenant && selectedTenant.ssn === tenant.ssn && details) {
        setDetails({ ...details, name: newName, email: newEmail });
        setSelectedTenant({ ...selectedTenant, name: newName, email: newEmail });
      }
    } catch (err) {
      console.error("Update error:", err);
      alert("Network error updating tenant");
    }
  };

  // --- View lease details ---
  const handleViewDetails = async (tenant) => {
    // toggle off if clicking same tenant
    if (selectedTenant && selectedTenant.ssn === tenant.ssn) {
      setSelectedTenant(null);
      setDetails(null);
      setErrorDetails("");
      setEditingLeaseId(null);
      setShowNewLeaseForm(false);
      return;
    }

    setSelectedTenant(tenant);
    setDetails(null);
    setErrorDetails("");
    setEditingLeaseId(null);
    setShowNewLeaseForm(false);
    setLoadingDetails(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/tenants/${tenant.ssn}/details`
      );

      if (!res.ok) {
        const text = await res.text();
        console.error("Details error:", res.status, text);
        setErrorDetails(`Error: ${res.status} ${text}`);
        setLoadingDetails(false);
        return;
      }

      const data = await res.json();
      setDetails(data);
    } catch (err) {
      console.error("Network error:", err);
      setErrorDetails("Network error loading details");
    } finally {
      setLoadingDetails(false);
    }
  };

  // ===== Lease editing helpers =====

  const startEditLease = (lease) => {
    setEditingLeaseId(lease.leaseId);
    setLeaseEditForm({
      term: lease.term || "",
      securityDeposit: lease.securityDeposit?.toString() || "",
      leaseType: lease.leaseType || "",
      status: lease.status || "",
      squareFeet: lease.squareFeet?.toString() || "",
      // these require backend to send street/city/state/zipcode; otherwise they become ""
      street: lease.street || "",
      city: lease.city || "",
      state: lease.state || "",
      zipcode: lease.zipcode || "",
    });
  };

  const handleLeaseEditChange = (field, value) => {
    setLeaseEditForm((prev) => ({ ...prev, [field]: value }));
  };

  const saveLease = async (lease) => {
    try {
      const body = {
        term: leaseEditForm.term,
        securityDeposit: leaseEditForm.securityDeposit
          ? parseFloat(leaseEditForm.securityDeposit)
          : 0,
        leaseType: leaseEditForm.leaseType,
        status: leaseEditForm.status,
        unit: {
          unitId: lease.unitId,
          squareFeet: leaseEditForm.squareFeet
            ? parseInt(leaseEditForm.squareFeet, 10)
            : lease.squareFeet,
          street: leaseEditForm.street,
          city: leaseEditForm.city,
          state: leaseEditForm.state,
          zipcode: leaseEditForm.zipcode,
        },
      };

      const res = await fetch(
        `http://127.0.0.1:5000/leases/${lease.leaseId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const text = await res.text();
      console.log("PUT /leases ->", res.status, text);

      if (!res.ok) {
        alert(`Error updating lease: ${res.status} ${text}`);
        return;
      }

      // update in local state
      setDetails((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          leases: prev.leases.map((l) =>
            l.leaseId === lease.leaseId
              ? {
                  ...l,
                  term: leaseEditForm.term,
                  securityDeposit: body.securityDeposit,
                  leaseType: leaseEditForm.leaseType,
                  status: leaseEditForm.status,
                  squareFeet: body.unit.squareFeet,
                  street: leaseEditForm.street,
                  city: leaseEditForm.city,
                  state: leaseEditForm.state,
                  zipcode: leaseEditForm.zipcode,
                  address: `${leaseEditForm.street}, ${leaseEditForm.city}, ${leaseEditForm.state} ${leaseEditForm.zipcode}`,
                }
              : l
          ),
        };
      });

      setEditingLeaseId(null);
    } catch (err) {
      console.error("Lease update error:", err);
      alert("Network error updating lease");
    }
  };

  const deleteLease = async (leaseId) => {
    if (!window.confirm("Delete this lease?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:5000/leases/${leaseId}`, {
        method: "DELETE",
      });

      const text = await res.text();
      if (!res.ok) {
        alert(`Error deleting lease: ${res.status} ${text}`);
        return;
      }

      setDetails((prev) =>
        prev
          ? { ...prev, leases: prev.leases.filter((l) => l.leaseId !== leaseId) }
          : prev
      );

      if (editingLeaseId === leaseId) {
        setEditingLeaseId(null);
      }
    } catch (err) {
      console.error("Delete lease error:", err);
      alert("Network error deleting lease");
    }
  };

  // ===== New lease helpers =====

  const handleNewLeaseChange = (field, value) => {
    setNewLeaseForm((prev) => ({ ...prev, [field]: value }));
  };

  const saveNewLease = async () => {
    if (!selectedTenant) return;

    try {
      const body = {
        term: newLeaseForm.term,
        securityDeposit: newLeaseForm.securityDeposit
          ? parseFloat(newLeaseForm.securityDeposit)
          : 0,
        leaseType: newLeaseForm.leaseType,
        status: newLeaseForm.status || "Active",
        squareFeet: newLeaseForm.squareFeet
          ? parseInt(newLeaseForm.squareFeet, 10)
          : 0,
        street: newLeaseForm.street,
        city: newLeaseForm.city,
        state: newLeaseForm.state,
        zipcode: newLeaseForm.zipcode,
      };

      const res = await fetch(
        `http://127.0.0.1:5000/tenants/${selectedTenant.ssn}/leases`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const text = await res.text();
      if (!res.ok) {
        console.error("New lease error:", res.status, text);
        alert(`Error creating lease: ${res.status} ${text}`);
        return;
      }

      const newLease = JSON.parse(text);

      setDetails((prev) =>
        prev
          ? { ...prev, leases: [...prev.leases, newLease] }
          : { leases: [newLease] }
      );

      setShowNewLeaseForm(false);
      setNewLeaseForm({
        term: "",
        securityDeposit: "",
        leaseType: "",
        status: "Active",
        squareFeet: "",
        street: "",
        city: "",
        state: "",
        zipcode: "",
      });
    } catch (err) {
      console.error("New lease network error:", err);
      alert("Network error creating lease");
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Tenants</h1>

      {/* Search box */}
      <div className="mb-4 flex items-center gap-2">
        <input
          className="border border-gray-300 p-2 rounded w-64"
          placeholder="Search by name, email, or SSN"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button
          className="border px-3 py-2 rounded bg-gray-100"
          onClick={() => setSearch("")}
        >
          Clear
        </button>
      </div>

      {loading ? (
        <p>Loading tenants...</p>
      ) : filteredTenants.length === 0 ? (
        <p>No tenants found.</p>
      ) : (
        <table className="w-full mt-2 border">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1 text-left">Name</th>
              <th className="border px-2 py-1 text-left">Email</th>
              <th className="border px-2 py-1 text-left">SSN</th>
              <th className="border px-2 py-1 text-left">Actions</th>
            </tr>
          </thead>

          <tbody>
            {filteredTenants.map((t) => (
              <tr key={t.ssn}>
                <td className="border px-2 py-1">{t.name}</td>
                <td className="border px-2 py-1">{t.email}</td>
                <td className="border px-2 py-1">{t.ssn}</td>
                <td className="border px-2 py-1 space-x-3">
                  <button
                    className="text-blue-600 underline"
                    onClick={() => handleEdit(t)}
                  >
                    Edit
                  </button>
                  <button
                    className="text-red-600 underline"
                    onClick={() => handleDelete(t.ssn)}
                  >
                    Delete
                  </button>
                  <button
                    className="text-green-600 underline"
                    onClick={() => handleViewDetails(t)}
                  >
                    {selectedTenant && selectedTenant.ssn === t.ssn
                      ? "Hide Details"
                      : "View Details"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Details panel */}
      {selectedTenant && (
        <div className="mt-6 p-4 border rounded-lg bg-gray-50">
          <h2 className="text-xl font-semibold mb-2">
            Details for {selectedTenant.name} ({selectedTenant.ssn})
          </h2>

          {loadingDetails && <p>Loading lease information...</p>}

          {errorDetails && (
            <p className="text-red-600 mb-2">{errorDetails}</p>
          )}

          {details && (
            <>
              <p className="mb-2">
                <span className="font-medium">Email:</span> {details.email}
              </p>

              {/* Add lease button */}
              <button
                className="mb-3 px-3 py-1 rounded bg-green-600 text-white"
                onClick={() => setShowNewLeaseForm((v) => !v)}
              >
                {showNewLeaseForm ? "Cancel New Lease" : "Add New Lease"}
              </button>

              {/* New lease form */}
              {showNewLeaseForm && (
                <div className="mb-4 p-3 border rounded bg-white space-y-2">
                  <div className="flex gap-2">
                    <input
                      className="border p-1 flex-1"
                      placeholder="Term (e.g., 12 months)"
                      value={newLeaseForm.term}
                      onChange={(e) =>
                        handleNewLeaseChange("term", e.target.value)
                      }
                    />
                    <input
                      className="border p-1 w-32"
                      placeholder="Deposit"
                      value={newLeaseForm.securityDeposit}
                      onChange={(e) =>
                        handleNewLeaseChange(
                          "securityDeposit",
                          e.target.value
                        )
                      }
                    />
                  </div>
                  <div className="flex gap-2">
                    <input
                      className="border p-1 flex-1"
                      placeholder="Lease Type"
                      value={newLeaseForm.leaseType}
                      onChange={(e) =>
                        handleNewLeaseChange(
                          "leaseType",
                          e.target.value
                        )
                      }
                    />
                    <input
                      className="border p-1 w-32"
                      placeholder="Status"
                      value={newLeaseForm.status}
                      onChange={(e) =>
                        handleNewLeaseChange("status", e.target.value)
                      }
                    />
                  </div>
                  <div className="flex gap-2">
                    <input
                      className="border p-1 w-24"
                      placeholder="Sq Ft"
                      value={newLeaseForm.squareFeet}
                      onChange={(e) =>
                        handleNewLeaseChange(
                          "squareFeet",
                          e.target.value
                        )
                      }
                    />
                    <input
                      className="border p-1 flex-1"
                      placeholder="Street"
                      value={newLeaseForm.street}
                      onChange={(e) =>
                        handleNewLeaseChange("street", e.target.value)
                      }
                    />
                  </div>
                  <div className="flex gap-2">
                    <input
                      className="border p-1 flex-1"
                      placeholder="City"
                      value={newLeaseForm.city}
                      onChange={(e) =>
                        handleNewLeaseChange("city", e.target.value)
                      }
                    />
                    <input
                      className="border p-1 w-16"
                      placeholder="State"
                      value={newLeaseForm.state}
                      onChange={(e) =>
                        handleNewLeaseChange("state", e.target.value)
                      }
                    />
                    <input
                      className="border p-1 w-24"
                      placeholder="Zip"
                      value={newLeaseForm.zipcode}
                      onChange={(e) =>
                        handleNewLeaseChange(
                          "zipcode",
                          e.target.value
                        )
                      }
                    />
                  </div>

                  <button
                    className="mt-2 px-3 py-1 rounded bg-blue-600 text-white"
                    onClick={saveNewLease}
                  >
                    Save Lease
                  </button>
                </div>
              )}

              {details.leases.length === 0 ? (
                <p>No leases found for this tenant.</p>
              ) : (
                <div className="space-y-3">
                  {details.leases.map((lease) => {
                    const isEditing = editingLeaseId === lease.leaseId;
                    return (
                      <div
                        key={lease.leaseId}
                        className="p-3 border rounded bg-white shadow-sm space-y-1"
                      >
                        {isEditing ? (
                          <>
                            {/* Editable fields */}
                            <div className="flex gap-2">
                              <input
                                className="border p-1 flex-1"
                                value={leaseEditForm.term}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "term",
                                    e.target.value
                                  )
                                }
                                placeholder="Term"
                              />
                              <input
                                className="border p-1 w-28"
                                value={leaseEditForm.securityDeposit}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "securityDeposit",
                                    e.target.value
                                  )
                                }
                                placeholder="Deposit"
                              />
                            </div>
                            <div className="flex gap-2">
                              <input
                                className="border p-1 flex-1"
                                value={leaseEditForm.leaseType}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "leaseType",
                                    e.target.value
                                  )
                                }
                                placeholder="Lease Type"
                              />
                              <input
                                className="border p-1 w-32"
                                value={leaseEditForm.status}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "status",
                                    e.target.value
                                  )
                                }
                                placeholder="Status"
                              />
                            </div>
                            <div className="flex gap-2">
                              <input
                                className="border p-1 w-20"
                                value={leaseEditForm.squareFeet}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "squareFeet",
                                    e.target.value
                                  )
                                }
                                placeholder="Sq Ft"
                              />
                              <input
                                className="border p-1 flex-1"
                                value={leaseEditForm.street}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "street",
                                    e.target.value
                                  )
                                }
                                placeholder="Street"
                              />
                            </div>
                            <div className="flex gap-2">
                              <input
                                className="border p-1 flex-1"
                                value={leaseEditForm.city}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "city",
                                    e.target.value
                                  )
                                }
                                placeholder="City"
                              />
                              <input
                                className="border p-1 w-16"
                                value={leaseEditForm.state}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "state",
                                    e.target.value
                                  )
                                }
                                placeholder="State"
                              />
                              <input
                                className="border p-1 w-24"
                                value={leaseEditForm.zipcode}
                                onChange={(e) =>
                                  handleLeaseEditChange(
                                    "zipcode",
                                    e.target.value
                                  )
                                }
                                placeholder="Zip"
                              />
                            </div>

                            <div className="mt-2 space-x-2">
                              <button
                                className="px-3 py-1 bg-blue-600 text-white rounded"
                                onClick={() => saveLease(lease)}
                              >
                                Save
                              </button>
                              <button
                                className="px-3 py-1 bg-gray-300 rounded"
                                onClick={() => setEditingLeaseId(null)}
                              >
                                Cancel
                              </button>
                            </div>
                          </>
                        ) : (
                          <>
                            {/* Display mode */}
                            <p>
                              <span className="font-medium">Lease ID:</span>{" "}
                              {lease.leaseId}
                            </p>
                            <p>
                              <span className="font-medium">Term:</span>{" "}
                              {lease.term}
                            </p>
                            <p>
                              <span className="font-medium">Type:</span>{" "}
                              {lease.leaseType}
                            </p>
                            <p>
                              <span className="font-medium">Status:</span>{" "}
                              {lease.status}
                            </p>
                            <p>
                              <span className="font-medium">
                                Security Deposit:
                              </span>{" "}
                              ${lease.securityDeposit.toFixed(2)}
                            </p>
                            <p>
                              <span className="font-medium">Unit:</span>{" "}
                              #{lease.unitId} – {lease.squareFeet} sq ft
                            </p>
                            <p>
                              <span className="font-medium">Address:</span>{" "}
                              {lease.address}
                            </p>

                            <div className="mt-2 space-x-2">
                              <button
                                className="text-blue-600 underline"
                                onClick={() => startEditLease(lease)}
                              >
                                Edit Lease
                              </button>
                              <button
                                className="text-red-600 underline"
                                onClick={() => deleteLease(lease.leaseId)}
                              >
                                Delete Lease
                              </button>
                            </div>
                          </>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default Tenants;
