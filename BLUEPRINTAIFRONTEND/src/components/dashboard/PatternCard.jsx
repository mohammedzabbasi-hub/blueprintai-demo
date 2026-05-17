export default function PatternCard({ title, items = {} }) {
  const rows = Object.entries(items).sort((a, b) => b[1] - a[1]);

  return (
    <div className="border rounded-2xl p-5">
      <h2 className="text-lg font-semibold mb-4">{title}</h2>
      <div className="space-y-2">
        {rows.length === 0 && <div className="text-sm text-gray-600">No data yet.</div>}
        {rows.map(([name, count]) => (
          <div
            key={name}
            className="flex items-center justify-between border rounded-xl px-3 py-2"
          >
            <span>{name}</span>
            <span className="text-sm text-gray-600">{count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
