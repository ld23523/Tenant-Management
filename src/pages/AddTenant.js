function AddTenant() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Add New Tenant</h1>

      <form className="space-y-4 w-80 bg-white p-6 rounded-lg shadow-md">
        <input className="border border-gray-300 p-3 w-full rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
               placeholder="Tenant Name" />
        <input className="border border-gray-300 p-3 w-full rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
               placeholder="Unit Number" />
        <input className="border border-gray-300 p-3 w-full rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
               placeholder="Phone Number" />

        <button className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded font-medium transition duration-200 w-full">
          Save Tenant
        </button>
      </form>
    </div>
  );
}

export default AddTenant;