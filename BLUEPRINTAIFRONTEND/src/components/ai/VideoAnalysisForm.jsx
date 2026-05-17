export default function VideoAnalysisForm({
  url,
  setUrl,
  brandName,
  setBrandName,
  productName,
  setProductName,
  onSubmit,
  loading,
  error,
}) {
  return (
    <form onSubmit={onSubmit} className="border rounded-2xl p-5 space-y-4">
      <input
        className="w-full border rounded-xl px-3 py-2"
        placeholder="TikTok video URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        required
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          className="border rounded-xl px-3 py-2"
          placeholder="Brand name"
          value={brandName}
          onChange={(e) => setBrandName(e.target.value)}
        />
        <input
          className="border rounded-xl px-3 py-2"
          placeholder="Product name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
      </div>

      <button
        type="submit"
        className="px-4 py-2 rounded-xl bg-black text-white"
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Video"}
      </button>

      {error && <div className="text-sm text-red-600">{error}</div>}
    </form>
  );
}
