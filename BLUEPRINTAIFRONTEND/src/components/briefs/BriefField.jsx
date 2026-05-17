export default function BriefField({ label, value }) {
  return (
    <div>
      <div className="text-sm text-gray-500">{label}</div>
      <div className="mt-1 whitespace-pre-wrap">{value || "—"}</div>
    </div>
  );
}
