import { useState } from "react";

function AddTenant() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [ssn, setSsn] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:5000/tenants", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          email,
          ssn,
        }),
      });

      const text = await res.text(); // read server response for debugging
      console.log("POST /tenants ->", res.status, text);

      if (!res.ok) {
        alert(`Error saving tenant: ${res.status} ${text}`);
        return;
      }

      // If backend returns JSON, you could do:
      // const data = JSON.parse(text);
      // console.log("Tenant saved:", data);

      setName("");
      setEmail("");
      setSsn("");
      alert("Tenant saved!");
    } catch (err) {
      console.error("Network error:", err);
      alert(`Error saving tenant (network): ${err.message}`);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Add New Tenant</h1>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 w-80 bg-white p-6 rounded-lg shadow-md"
      >
        <input
          className="border border-gray-300 p-3 w-full rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Tenant Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          className="border border-gray-300 p-3 w-full rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="border border-gray-300 p-3 w-full rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="SSN"
          value={ssn}
          onChange={(e) => setSsn(e.target.value)}
        />

        <button
          type="submit"
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded font-medium transition duration-200 w-full"
        >
          Save Tenant
        </button>
      </form>
    </div>
  );
}

export default AddTenant;
