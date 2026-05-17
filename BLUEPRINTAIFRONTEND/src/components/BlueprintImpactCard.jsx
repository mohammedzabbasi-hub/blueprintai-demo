import { BarChart3, Sparkles, Zap } from "lucide-react";

export default function BlueprintImpactCard({ blueprint }) {
  const totalSteps = blueprint?.steps?.length || 0;
  const completedSteps = blueprint?.steps?.filter((step) => step.is_completed).length || 0;
  const progress = totalSteps ? Math.round((completedSteps / totalSteps) * 100) : 0;

  return (
    <div className="blueprint-impact-card">
      <div className="blueprint-impact-item">
        <div className="blueprint-impact-icon">
          <BarChart3 size={20} />
        </div>
        <div>
          <p>Blueprint Progress</p>
          <h3>{progress}%</h3>
        </div>
      </div>

      <div className="blueprint-impact-item">
        <div className="blueprint-impact-icon">
          <Zap size={20} />
        </div>
        <div>
          <p>Total Steps</p>
          <h3>{totalSteps}</h3>
        </div>
      </div>

      <div className="blueprint-impact-item">
        <div className="blueprint-impact-icon">
          <Sparkles size={20} />
        </div>
        <div>
          <p>Focus</p>
          <h3>{blueprint?.main_goal || "Growth"}</h3>
        </div>
      </div>
    </div>
  );
}
