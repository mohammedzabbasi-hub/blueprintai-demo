function MiniMetric({ label, value }) {
  return (
    <div className="border rounded-xl p-2">
      <div className="text-gray-500 text-xs">{label}</div>
      <div className="font-medium">{Number(value || 0).toLocaleString()}</div>
    </div>
  );
}

export default function CreativeMetricsRow({ creative }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4 text-sm">
      <MiniMetric label="Views" value={creative.views} />
      <MiniMetric label="Likes" value={creative.likes} />
      <MiniMetric label="Shares" value={creative.shares} />
      <MiniMetric label="Clicks" value={creative.clicks} />
      <MiniMetric label="Orders" value={creative.orders} />
    </div>
  );
}
