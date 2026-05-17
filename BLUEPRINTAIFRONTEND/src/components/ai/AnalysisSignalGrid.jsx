function SignalCard({ label, value }) {
  return (
    <div className="border rounded-xl p-3">
      <div className="text-xs text-gray-500">{label}</div>
      <div className="font-medium mt-1">{value || "—"}</div>
    </div>
  );
}

export default function AnalysisSignalGrid({ signals = {} }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      <SignalCard label="Hook Type" value={signals.hook_type} />
      <SignalCard label="Hook Text" value={signals.hook_text} />
      <SignalCard label="Humor Style" value={signals.humor_style} />
      <SignalCard label="Delivery Style" value={signals.delivery_style} />
      <SignalCard label="Creator Style" value={signals.creator_style} />
      <SignalCard label="Promoter Type" value={signals.promoter_type} />
      <SignalCard label="Subject Focus" value={signals.subject_focus} />
      <SignalCard label="Pacing" value={signals.pacing} />
      <SignalCard label="CTA Style" value={signals.cta_style} />
    </div>
  );
}
