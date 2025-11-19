import { Link } from "react-router-dom";

function Tenants() {
  const tenants = [
    { id: 1, name: "John Doe", unit: "A1", phone: "555-1234" },
    { id: 2, name: "Sara Smith", unit: "B2", phone: "555-9876" },
  ];

  const handleDelete = (tenantId) => {
    // This will call backend API: DELETE /api/tenants/${tenantId}
    console.log("Delete tenant with ID:", tenantId);
    alert(`Would delete tenant ${tenantId} - Backend will implement this`);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Tenants</h1>

      <Link
        to="/tenants/add"
        className="bg-blue-600 text-white px-4 py-2 rounded mb-4 inline-block"
      >
        + Add Tenant
      </Link>

      <table className="w-full mt-6 border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Name</th>
            <th className="p-2 border">Unit</th>
            <th className="p-2 border">Phone</th>
            <th className="p-2 border">Actions</th> {/* ← NEW COLUMN */}
          </tr>
        </thead>

        <tbody>
          {tenants.map((t) => (
            <tr key={t.id}>
              <td className="p-2 border">{t.name}</td>
              <td className="p-2 border">{t.unit}</td>
              <td className="p-2 border">{t.phone}</td>
              <td className="p-2 border">
                <button 
                  onClick={() => handleDelete(t.id)}
                  className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Tenants;