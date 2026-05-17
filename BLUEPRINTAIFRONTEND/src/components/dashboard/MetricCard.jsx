export default function MetricCard({ label, value }) {
  return (
    <div className="border rounded-2xl p-4">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-2xl font-bold mt-1">{Number(value || 0).toLocaleString()}</div>
    </div>
  );
}
