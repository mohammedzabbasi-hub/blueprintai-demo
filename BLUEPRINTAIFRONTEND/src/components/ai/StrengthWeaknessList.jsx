export default function StrengthWeaknessList({ title, items = [] }) {
  return (
    <div>
      <div className="text-sm text-gray-500 mb-2">{title}</div>
      <div className="space-y-2">
        {items.length === 0 && <div>—</div>}
        {items.map((item, index) => (
          <div key={`${title}-${index}`} className="border rounded-xl p-3">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
