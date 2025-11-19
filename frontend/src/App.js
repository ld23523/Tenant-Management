import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Tenants from "./pages/Tenants";
import AddTenant from "./pages/AddTenant";
import Maintenance from "./pages/Maintenance";
import PaymentPlans from "./pages/PaymentPlans";
import LateFees from "./pages/LateFees";

function App() {
  return (
    <Router>
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 p-6 bg-gradient-to-br from-blue-50 to-indigo-100">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/tenants" element={<Tenants />} />
            <Route path="/tenants/add" element={<AddTenant />} />
            <Route path="/payment-plans" element={<PaymentPlans />} />
            <Route path="/late-fees" element={<LateFees />} />
            <Route path="/maintenance" element={<Maintenance />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;