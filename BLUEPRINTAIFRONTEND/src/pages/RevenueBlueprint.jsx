import { useEffect, useState } from "react";
import { RefreshCw, Route, Sparkles } from "lucide-react";
import BlueprintTimeline from "../components/BlueprintTimeline";
import BlueprintDiagnosisCard from "../components/BlueprintDiagnosisCard";
import BlueprintImpactCard from "../components/BlueprintImpactCard";
import { generateBlueprint, getLatestBlueprint } from "../services/blueprintApi";
import "../styles/revenue-blueprint.css";

import { createActivityLog } from "../services/activityLog";
export default function RevenueBlueprint() {
  const [blueprint, setBlueprint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  const selectedShopId =
    localStorage.getItem("selectedShopId") ||
    localStorage.getItem("shop_id") ||
    "1";

  async function loadBlueprint() {
    try {
      setLoading(true);
      setError("");
      const data = await getLatestBlueprint(selectedShopId);
      setBlueprint(data);
    } catch (err) {
      console.error(err);
      setError("Could not load blueprint.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGenerateNewBlueprint() {
    try {
      setGenerating(true);
      setError("");
      const data = await generateBlueprint(selectedShopId);
      setBlueprint(data);

      try {
        await createActivityLog({
          activity_type: "blueprint",
          title: "Blueprint generated",
          description:
            data?.summary ||
            data?.diagnosis ||
            "A new AI Growth Blueprint was generated.",
          shop_id: data?.shop_id || selectedShopId || 1,
          metadata: {
            blueprint_id: data?.id,
            main_goal: data?.main_goal,
            estimated_impact: data?.estimated_impact,
            steps_count: data?.steps?.length || 0,
          },
        });
      } catch (logError) {
        console.warn("Failed to save blueprint activity log:", logError);
      }
    } catch (err) {
      console.error(err);
      setError("Could not generate blueprint.");
    } finally {
      setGenerating(false);
    }
  }

  function handleStepUpdated(updatedStep) {
    setBlueprint((current) => {
      if (!current) return current;

      return {
        ...current,
        steps: current.steps.map((step) =>
          step.id === updatedStep.id ? updatedStep : step
        ),
      };
    });
  }

  useEffect(() => {
    loadBlueprint();
  }, []);

  if (loading) {
    return (
      <div className="revenue-blueprint-page">
        <div className="blueprint-loading">Loading AI Growth Blueprint...</div>
      </div>
    );
  }

  return (
    <div className="revenue-blueprint-page">
      <div className="blueprint-hero">
        <div>
          <div className="blueprint-badge">
            <Sparkles size={16} />
            AI Growth Blueprint
          </div>

          <h1>Revenue Blueprint</h1>
          <p>
            A step-by-step TikTok Shop growth plan built from your dashboard,
            video analysis, creator comparison, ad briefs, and recommendations.
          </p>
        </div>

        <button
          className="blueprint-generate-button"
          onClick={handleGenerateNewBlueprint}
          disabled={generating}
        >
          <RefreshCw size={18} className={generating ? "spin" : ""} />
          {generating ? "Generating..." : "Generate New Blueprint"}
        </button>
      </div>

      {error && <div className="blueprint-error">{error}</div>}

      <div className="blueprint-grid">
        <BlueprintDiagnosisCard blueprint={blueprint} />
        <BlueprintImpactCard blueprint={blueprint} />
      </div>

      <div className="blueprint-summary-card">
        <div className="blueprint-card-icon">
          <Route size={22} />
        </div>

        <div>
          <p className="blueprint-eyebrow">Plan Summary</p>
          <h2>{blueprint?.title || "AI Growth Blueprint"}</h2>
          <p>{blueprint?.summary}</p>
        </div>
      </div>

      <BlueprintTimeline
        steps={blueprint?.steps || []}
        onStepUpdated={handleStepUpdated}
      />
    </div>
  );
}
