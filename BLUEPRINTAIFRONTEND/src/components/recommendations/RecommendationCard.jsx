function Info({ label, value }) {
  return (
    <div className="border rounded-xl p-3">
      <div className="text-xs text-gray-500">{label}</div>
      <div className="font-medium mt-1">{value || "—"}</div>
    </div>
  );
}

export default function RecommendationCard({ item }) {
  return (
    <div className="border rounded-2xl p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-xs text-gray-500">{item.category}</div>
          <h2 className="text-xl font-semibold mt-1">{item.name}</h2>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-500">Confidence</div>
          <div className="font-bold">{item.confidence ?? "—"}</div>
        </div>
      </div>

      <div className="mt-3 text-sm text-gray-700">
        {item.reason || "No reason provided."}
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
        <Info label="Type" value={item.rec_type} />
        <Info label="Priority" value={item.priority} />
        <Info label="Product" value={item.product_name} />
      </div>

      {item.action && (
        <div className="mt-4">
          <div className="text-sm text-gray-500">Action</div>
          <div className="mt-1">{item.action}</div>
        </div>
      )}

      {item.evidence && (
        <div className="mt-4">
          <div className="text-sm text-gray-500">Evidence</div>
          <div className="mt-1">{item.evidence}</div>
        </div>
      )}
    </div>
  );
}
