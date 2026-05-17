import BriefField from "./BriefField";

export default function BriefResultCard({ brief }) {
  if (!brief) return null;

  return (
    <div className="border rounded-2xl p-6 space-y-5">
      <div>
        <div className="text-sm text-gray-500">Title</div>
        <div className="text-2xl font-bold">{brief.brief_title || "Generated Brief"}</div>
      </div>

      <BriefField label="Hook" value={brief.hook} />
      <BriefField label="Creator Type" value={brief.creator_type} />
      <BriefField label="Tone" value={brief.tone} />
      <BriefField label="Structure" value={brief.structure} />
      <BriefField label="CTA" value={brief.cta} />
      <BriefField label="Reasoning" value={brief.reasoning} />
      <BriefField label="Target Audience" value={brief.target_audience} />
      <BriefField label="Primary Angle" value={brief.primary_angle} />
      <BriefField label="Secondary Angle" value={brief.secondary_angle} />
      <BriefField label="Script" value={brief.script} />
      <BriefField label="Shot List" value={brief.shot_list} />
      <BriefField label="Do's" value={brief.dos} />
      <BriefField label="Don'ts" value={brief.donts} />
      <BriefField label="References" value={brief.references} />
    </div>
  );
}
