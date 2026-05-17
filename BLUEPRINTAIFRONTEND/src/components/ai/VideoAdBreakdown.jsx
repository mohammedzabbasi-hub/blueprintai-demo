function scoreLabel(score) {
  if (score >= 8) return "Strong";
  if (score >= 5) return "Needs Testing";
  return "Weak";
}

function SectionCard({ title, subtitle, children, accent = false }) {
  return (
    <div
      className={`rounded-2xl border p-6 bg-[#0d1526] ${
        accent ? "border-sky-500/25" : "border-white/10"
      }`}
    >
      <h3 className="text-lg font-bold text-white">{title}</h3>
      {subtitle && <p className="text-sm text-slate-500 mt-1">{subtitle}</p>}
      <div className="mt-4 text-slate-300 leading-relaxed">{children}</div>
    </div>
  );
}

function ScoreCard({ label, value }) {
  return (
    <div className="bg-[#0d1526] border border-white/10 rounded-2xl p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="text-4xl font-bold text-white mt-2">{value}/10</p>
      <p className="text-xs text-sky-300 mt-2">{scoreLabel(value)}</p>
    </div>
  );
}

function BulletList({ items = [] }) {
  return (
    <ul className="space-y-3">
      {items.map((item, index) => (
        <li key={index} className="flex gap-2">
          <span className="text-sky-400">•</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

export default function VideoAdBreakdown({ result }) {
  const payload = result?.result || result || {};
  const analysis = payload?.analysis || {};
  const transcript = payload?.transcript || {};
  const metadata = payload?.metadata || {};
  const ocrText = payload?.ocr_text || [];

  const hookScore = analysis.hook_score ?? 0;
  const ctaScore = analysis.cta_score ?? 0;
  const clarityScore = analysis.clarity_score ?? 0;

  const detectedText = ocrText
    .map((item) => item.text)
    .filter(Boolean)
    .slice(0, 5)
    .join(" | ");

  return (
    <section className="analysis-results mt-10 space-y-6">
      <div>
        <p className="text-sky-400 text-xs font-bold tracking-[0.25em] uppercase">
          Creative Intelligence Report
        </p>
        <h2 className="text-3xl font-black text-white mt-2">Video Ad Breakdown</h2>
        <p className="text-slate-400 mt-2">
          Hook, CTA, messaging, visuals, format, and next-test recommendations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ScoreCard label="Hook Score" value={hookScore} />
        <ScoreCard label="CTA Score" value={ctaScore} />
        <ScoreCard label="Clarity Score" value={clarityScore} />
      </div>

      <SectionCard title="Executive Summary" subtitle="Overall creative read">
        <p>{analysis.summary || "No summary available."}</p>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <SectionCard title="Hook Analysis" subtitle="First seconds and scroll-stopping power">
          <p>
            This creative has a hook score of <strong>{hookScore}/10</strong>.{" "}
            {hookScore >= 7
              ? "The opening is strong enough to earn attention."
              : "The opening needs a stronger reason for the viewer to keep watching."}
          </p>
        </SectionCard>

        <SectionCard title="Messaging Angle" subtitle="Main selling angle detected">
          <p>
            Creator style:{" "}
            <strong>{analysis.creator_style || "Not clearly detected"}</strong>.
          </p>
          <p className="mt-2">
            The ad should make the product benefit clearer earlier, especially if the
            viewer has no sound on.
          </p>
        </SectionCard>

        <SectionCard title="Visual Elements" subtitle="Branding, text, product focus">
          <p>
            Detected on-screen text:{" "}
            <span className="text-slate-400">
              {detectedText || "No readable on-screen text detected."}
            </span>
          </p>
          <p className="mt-2">
            Visual clarity score: <strong>{clarityScore}/10</strong>.
          </p>
        </SectionCard>

        <SectionCard title="CTA Effectiveness" subtitle="Conversion prompt strength">
          <p>
            CTA score: <strong>{ctaScore}/10</strong>.{" "}
            {ctaScore >= 7
              ? "The next step is clear."
              : "The ad needs a stronger direct action like “Shop now,” “Try it today,” or “Tap to buy.”"}
          </p>
        </SectionCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <SectionCard title="Strengths">
          <BulletList items={analysis.strengths || []} />
        </SectionCard>

        <SectionCard title="Weaknesses">
          <BulletList items={analysis.weaknesses || []} />
        </SectionCard>

        <SectionCard title="Recommendations" accent>
          <BulletList items={analysis.recommendations || []} />
        </SectionCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <SectionCard title="Ad Format">
          <p>Duration: {metadata.duration_seconds?.toFixed?.(1) || "Unknown"} seconds</p>
          <p>Size: {metadata.width || "?"} × {metadata.height || "?"}</p>
          <p>FPS: {metadata.fps || "Unknown"}</p>
        </SectionCard>

        <SectionCard title="Transcript Review">
          <p>
            {transcript.full_text || "No transcript detected. Add voiceover or captions for stronger clarity."}
          </p>
        </SectionCard>

        <SectionCard title="Next Test Plan" accent>
          <ul className="space-y-3">
            <li>• Test a stronger first 3-second hook.</li>
            <li>• Add clear product-benefit text on screen.</li>
            <li>• Add a direct CTA near the end.</li>
            <li>• Test a creator voiceover version.</li>
          </ul>
        </SectionCard>
      </div>
    </section>
  );
}
