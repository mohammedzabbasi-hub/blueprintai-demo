import { Target, TrendingUp } from "lucide-react";

export default function BlueprintDiagnosisCard({ blueprint }) {
  if (!blueprint) return null;

  return (
    <div className="blueprint-diagnosis-card">
      <div className="blueprint-card-icon">
        <Target size={22} />
      </div>

      <div>
        <p className="blueprint-eyebrow">Current Diagnosis</p>
        <h2>{blueprint.main_goal || "AI Growth Goal"}</h2>
        <p className="blueprint-muted">{blueprint.diagnosis}</p>

        <div className="blueprint-mini-impact">
          <TrendingUp size={17} />
          <span>{blueprint.estimated_impact}</span>
        </div>
      </div>
    </div>
  );
}
