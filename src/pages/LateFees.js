function LateFees() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Late Fee Management</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Current Late Fees</h2>
          <div className="space-y-3">
            <div className="flex justify-between p-3 bg-red-50 rounded">
              <span>John Doe - Unit A1</span>
              <span className="font-bold text-red-600">$50</span>
            </div>
            <div className="flex justify-between p-3 bg-red-50 rounded">
              <span>Mike Johnson - Unit C3</span>
              <span className="font-bold text-red-600">$75</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Late Fee Rules</h2>
          <div className="space-y-2 text-sm">
            <p>• $25 late fee after 3-day grace period</p>
            <p>• +$10 per additional day late</p>
            <p>• Maximum late fee: $100</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LateFees;