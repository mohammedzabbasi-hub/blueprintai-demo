import { CheckCircle2 } from "lucide-react";

export default function BlueprintStepCard({ step, index, onClick }) {
  return (
    <button
      className={`blueprint-step-card ${step.is_completed ? "completed" : ""}`}
      style={{ animationDelay: `${index * 140}ms` }}
      onClick={() => onClick(step)}
    >
      <div className="blueprint-step-number">
        {step.is_completed ? <CheckCircle2 size={20} /> : step.step_number}
      </div>

      <div className="blueprint-step-mini-content">
        <span>{step.related_feature || "BlueprintAI"}</span>
        <h3>{step.title}</h3>
      </div>
    </button>
  );
}
