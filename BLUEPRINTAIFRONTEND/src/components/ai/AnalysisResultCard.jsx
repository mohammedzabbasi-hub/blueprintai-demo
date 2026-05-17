import AnalysisSignalGrid from "./AnalysisSignalGrid";
import StrengthWeaknessList from "./StrengthWeaknessList";

function TextBlock({ title, value }) {
  return (
    <div>
      <div className="text-sm text-gray-500">{title}</div>
      <div className="mt-1">{value || "—"}</div>
    </div>
  );
}

export default function AnalysisResultCard({ result }) {
  if (!result) return null;

  return (
    <div className="border rounded-2xl p-6 space-y-5">
      <div>
        <h2 className="text-xl font-semibold">Analysis Result</h2>
        <p className="text-sm text-gray-600 mt-1">AI-generated creative breakdown</p>
      </div>

      <AnalysisSignalGrid signals={result.signals || {}} />

      <TextBlock title="Transcript Summary" value={result.transcript_summary} />
      <TextBlock title="Performance Hypothesis" value={result.performance_hypothesis} />

      <StrengthWeaknessList title="Strengths" items={result.strengths || []} />
      <StrengthWeaknessList title="Weaknesses" items={result.weaknesses || []} />
    </div>
  );
}
