export default function BriefForm({
  productName,
  setProductName,
  brandName,
  setBrandName,
  onSubmit,
  loading,
  error,
}) {
  return (
    <form onSubmit={onSubmit} className="border rounded-2xl p-5 space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          className="border rounded-xl px-3 py-2"
          placeholder="Product name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          required
        />
        <input
          className="border rounded-xl px-3 py-2"
          placeholder="Brand name"
          value={brandName}
          onChange={(e) => setBrandName(e.target.value)}
        />
      </div>

      <button
        type="submit"
        className="px-4 py-2 rounded-xl bg-black text-white"
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Brief"}
      </button>

      {error && <div className="text-sm text-red-600">{error}</div>}
    </form>
  );
}
