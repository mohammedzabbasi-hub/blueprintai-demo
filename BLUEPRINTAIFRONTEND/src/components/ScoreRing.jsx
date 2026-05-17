export function ScoreRing({ value = 0, label = "Score" }) {
  return (
    <div className="border rounded-full w-24 h-24 flex flex-col items-center justify-center">
      <div className="text-lg font-bold">{value}</div>
      <div className="text-xs text-gray-500">{label}</div>
    </div>
  );
}

export default ScoreRing;
