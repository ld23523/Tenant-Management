function PaymentPlans() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Payment Plans</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-xl font-semibold mb-4">Request Payment Plan</h2>
        <form className="space-y-4 max-w-md">
          <select className="w-full p-3 border border-gray-300 rounded">
            <option>Select Tenant</option>
            <option>John Doe (Unit A1)</option>
            <option>Sara Smith (Unit B2)</option>
          </select>
          <input type="number" placeholder="Total Amount" className="w-full p-3 border border-gray-300 rounded" />
          <input type="number" placeholder="Number of Installments" className="w-full p-3 border border-gray-300 rounded" />
          <button type="submit" className="bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700">
            Submit Request
          </button>
        </form>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Active Payment Plans</h2>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
            <div>
              <p className="font-semibold">John Doe - Unit A1</p>
              <p className="text-sm text-gray-600">$500 ÷ 5 payments</p>
            </div>
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">Active</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PaymentPlans;