import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div className="w-64 h-screen bg-indigo-800 text-white flex flex-col p-6 space-y-4">
      <h2 className="text-2xl font-bold text-white">Tenant Manager</h2>

      <Link to="/" className="hover:bg-indigo-700 p-2 rounded transition duration-200">Dashboard</Link>
      <Link to="/tenants" className="hover:bg-indigo-700 p-2 rounded transition duration-200">Tenants</Link>
      <Link to="/tenants/add" className="hover:bg-indigo-700 p-2 rounded transition duration-200">Add Tenant</Link>
      <Link to="/payment-plans" className="hover:bg-indigo-700 p-2 rounded transition duration-200">Payment Plans</Link>
      <Link to="/late-fees" className="hover:bg-indigo-700 p-2 rounded transition duration-200">Late Fees</Link>
      <Link to="/maintenance" className="hover:bg-indigo-700 p-2 rounded transition duration-200">Maintenance</Link>
    </div>
  );
}

export default Sidebar;