import { X, CheckCircle2, Circle } from "lucide-react";
import { useState } from "react";
import BlueprintStepCard from "./BlueprintStepCard";
import { completeBlueprintStep } from "../services/blueprintApi";

export default function BlueprintTimeline({ steps = [], onStepUpdated }) {
  const [selectedStep, setSelectedStep] = useState(null);

  async function handleToggle(step) {
    try {
      const updated = await completeBlueprintStep(step.id, !step.is_completed);
      onStepUpdated?.(updated);
      setSelectedStep(updated);
    } catch (error) {
      console.error(error);
    }
  }

  const nodeClassNames = [
    "node-1",
    "node-2",
    "node-3",
    "node-4",
    "node-5",
    "node-6",
  ];

  return (
    <div className="blueprint-flow-wrap">
      <div className="blueprint-flow-title">
        <span>AI Revenue Blueprint Path</span>
        <p>Click each step to view the full action plan.</p>
      </div>

      <div className="blueprint-flow-board">
        <svg
          className="blueprint-svg-lines"
          viewBox="0 0 1200 900"
          preserveAspectRatio="none"
        >
          <defs>
            <marker
              id="blueprintArrow"
              markerWidth="12"
              markerHeight="12"
              refX="10"
              refY="6"
              orient="auto"
              markerUnits="strokeWidth"
            >
              <path d="M0,0 L12,6 L0,12 Z" fill="#22d3ee" />
            </marker>
          </defs>

          {/* 1 bottom-left anchor → 2 top-right anchor */}
          <path d="M520 210 C430 255, 335 295, 250 345" />

          {/* 2 right-center anchor → 3 left-center anchor */}
          <path d="M275 430 C455 430, 745 430, 925 430" />

          {/* 3 bottom-left anchor → 4 top-right anchor */}
          <path d="M925 525 C720 600, 470 595, 250 650" />

          {/* 4 right-center anchor → 5 left-center anchor */}
          <path d="M275 735 C455 735, 745 735, 925 735" />

          {/* 5 bottom-left anchor → 6 top-right anchor */}
          <path d="M925 830 C760 875, 635 870, 535 845" />
        </svg>

        {steps.map((step, index) => (
          <div
            key={step.id || step.step_number}
            className={`blueprint-flow-node ${nodeClassNames[index] || ""}`}
          >
            <BlueprintStepCard
              step={step}
              index={index}
              onClick={setSelectedStep}
            />
          </div>
        ))}
      </div>

      {selectedStep && (
        <div className="blueprint-modal-backdrop" onClick={() => setSelectedStep(null)}>
          <div className="blueprint-modal" onClick={(e) => e.stopPropagation()}>
            <button className="blueprint-modal-close" onClick={() => setSelectedStep(null)}>
              <X size={20} />
            </button>

            <div className="blueprint-modal-top">
              <div className="blueprint-step-number large">
                {selectedStep.is_completed ? <CheckCircle2 size={24} /> : selectedStep.step_number}
              </div>

              <div>
                <span className="blueprint-step-feature">
                  {selectedStep.related_feature || "BlueprintAI"}
                </span>
                <h2>{selectedStep.title}</h2>
              </div>
            </div>

            <p className="blueprint-modal-description">{selectedStep.description}</p>

            <div className="blueprint-modal-action">
              <p className="blueprint-eyebrow">Action</p>
              <span>{selectedStep.action}</span>
            </div>

            {selectedStep.expected_result && (
              <div className="blueprint-modal-result">
                <p className="blueprint-eyebrow">Expected Result</p>
                <span>{selectedStep.expected_result}</span>
              </div>
            )}

            <button
              className="blueprint-complete-button"
              onClick={() => handleToggle(selectedStep)}
            >
              {selectedStep.is_completed ? (
                <>
                  <CheckCircle2 size={17} />
                  Completed
                </>
              ) : (
                <>
                  <Circle size={17} />
                  Mark Complete
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
