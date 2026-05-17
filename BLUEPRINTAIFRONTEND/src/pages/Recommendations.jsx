import React, { useEffect, useMemo, useState } from "react";
import "./Recommendations.css";
import { getEngineRecommendations, getGeminiStrategy } from "../services/engineApi";

const fallbackRecommendations = [
  {
    id: 1,
    title: "Make more creatives using 3-second demo hooks",
    type: "Hooks",
    priority: "High",
    product: "All products",
    confidence: 75,
    why: "3-second demo hooks are currently one of the strongest creative patterns for this shop.",
    action: "Create more short demo-first videos that show the product in use within the first 3 seconds.",
    evidence: "Creatives using this pattern are outperforming other hook styles across the shop.",
  },
  {
    id: 2,
    title: "Scale voiceover tutorial style videos",
    type: "Creative Format",
    priority: "High",
    product: "All products",
    confidence: 75,
    why: "Voiceover tutorial creatives are converting better than other formats.",
    action: "Produce more tutorial-style videos with clear voiceover explanations and product demonstrations.",
    evidence: "Voiceover tutorial creatives are showing stronger conversion patterns than other formats.",
  },
  {
    id: 3,
    title: "Prioritize sample collaboration creators",
    type: "Creator Strategy",
    priority: "High",
    product: "All products",
    confidence: 92,
    why: "Sample collaboration creators are producing stronger shop performance.",
    action: "Recruit or assign more sample collaboration creators for the next testing cycle.",
    evidence: "Sample collaboration creatives generated strong order volume and conversion performance.",
  },
  {
    id: 4,
    title: "Improve click-through with clearer CTAs",
    type: "CTA",
    priority: "Medium",
    product: "Smart Water Bottle",
    confidence: 82,
    why: "Some creatives get views but do not generate enough clicks.",
    action: "Use direct CTA language like “Tap the product card” or “Shop the bundle before the deal ends.”",
    evidence: "The product has below-average click-through compared with the shop benchmark.",
  },
];

function getShopId() {
  const params = new URLSearchParams(window.location.search);
  return (
    params.get("shop_id") ||
    localStorage.getItem("selectedShopId") ||
    localStorage.getItem("demoShopId") ||
    localStorage.getItem("shop_id") ||
    "2"
  );
}

function normalizeRecommendation(item, index) {
  return {
    id: item.id || `${index}-${item.title || item.recommendation || "recommendation"}`,
    title:
      item.title ||
      item.recommendation ||
      item.name ||
      item.headline ||
      "Untitled recommendation",
    type:
      item.type ||
      item.category ||
      item.recommendation_type ||
      item.segment ||
      "Recommendation",
    priority: item.priority || item.urgency || "Medium",
    product:
      item.product ||
      item.product_name ||
      item.productName ||
      item.target_product ||
      "All products",
    confidence: item.confidence || item.confidence_score || item.score || null,
    why:
      item.why ||
      item.why_this_matters ||
      item.why_it_matters ||
      item.finding ||
      item.reason ||
      item.description ||
      "This recommendation is based on current creative performance patterns.",
    action:
      item.action ||
      item.action_step ||
      item.recommended_action ||
      item.next_step ||
      item.next_steps ||
      "Test this recommendation in the next creative cycle.",
    evidence:
      item.evidence ||
      item.proof ||
      item.supporting_data ||
      item.insight ||
      "Performance data suggests this pattern is worth testing further.",
  };
}

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState(fallbackRecommendations);
  const [activeFilter, setActiveFilter] = useState("All");
  const [selectedRecommendation, setSelectedRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);

  const shopId = getShopId();

  useEffect(() => {
    async function loadRecommendations() {
      try {
        let raw = [];

        try {
          const gemini = await getGeminiStrategy(shopId);
          raw = gemini?.result?.gemini_json?.top_3_recommendations || [];
        } catch (geminiError) {
          console.warn("Gemini recommendations unavailable, using coded engine:", geminiError);
        }

        if (!raw.length) {
          const data = await getEngineRecommendations(shopId);
          raw =
            data?.report?.recommendations ||
            data?.recommendations ||
            [];
        }

        if (raw.length > 0) {
          setRecommendations(raw.map(normalizeRecommendation));
        }
      } catch (error) {
        console.warn("Using fallback recommendations:", error);
      } finally {
        setLoading(false);
      }
    }

    loadRecommendations();
  }, [shopId]);

  const filters = useMemo(() => {
    const types = recommendations.map((rec) => rec.type).filter(Boolean);
    return ["All", ...Array.from(new Set(types))];
  }, [recommendations]);

  const filteredRecommendations = useMemo(() => {
    if (activeFilter === "All") return recommendations;
    return recommendations.filter((rec) => rec.type === activeFilter);
  }, [activeFilter, recommendations]);

  const topPriority = recommendations[0];

  return (
    <main className="recommendations-page">
      <section className="recommendations-hero">
        <div>
          <p className="eyebrow">Creative Strategy</p>
          <h1>AI Recommendations</h1>
          <p>
            Focused creative actions based on TikTok Shop performance patterns.
          </p>
        </div>
      </section>

      <section className="recommendations-summary">
        <div className="summary-card">
          <span>Total Recommendations</span>
          <strong>{recommendations.length}</strong>
        </div>
        <div className="summary-card">
          <span>High Priority</span>
          <strong>{recommendations.filter((rec) => rec.priority === "High").length}</strong>
        </div>
        <div className="summary-card">
          <span>Top Opportunity</span>
          <strong>{topPriority?.type || "Creative"}</strong>
        </div>
      </section>

      <section className="recommendations-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Recommendation Queue</p>
            <h2>Current creative actions</h2>
          </div>
          <button className="refresh-button" onClick={() => window.location.reload()}>
            Refresh
          </button>
        </div>

        <div className="recommendation-filters">
          {filters.map((filter) => (
            <button
              key={filter}
              className={activeFilter === filter ? "active" : ""}
              onClick={() => setActiveFilter(filter)}
            >
              {filter}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="empty-state">Loading recommendations...</div>
        ) : (
          <div className="recommendation-grid compact">
            {filteredRecommendations.map((rec) => (
              <article className="recommendation-card simplified" key={rec.id}>
                <div className="card-topline">
                  <span>{rec.type}</span>
                  <span className={`priority-pill ${String(rec.priority).toLowerCase()}`}>
                    {rec.priority}
                  </span>
                </div>

                <h3>{rec.title}</h3>

                <button
                  className="details-link"
                  onClick={() => setSelectedRecommendation(rec)}
                >
                  View details →
                </button>
              </article>
            ))}
          </div>
        )}
      </section>

      {selectedRecommendation && (
        <div className="recommendation-modal-backdrop" onClick={() => setSelectedRecommendation(null)}>
          <section className="recommendation-modal" onClick={(event) => event.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedRecommendation(null)}>
              ×
            </button>

            <p className="eyebrow">{selectedRecommendation.type}</p>
            <h2>{selectedRecommendation.title}</h2>

            <div className="modal-meta-row">
              <span>{selectedRecommendation.priority} priority</span>
              <span>{selectedRecommendation.product}</span>
              {selectedRecommendation.confidence && (
                <span>{selectedRecommendation.confidence}% confidence</span>
              )}
            </div>

            <div className="detail-block">
              <span>Why this matters</span>
              <p>{selectedRecommendation.why}</p>
            </div>

            <div className="detail-block">
              <span>Recommended action</span>
              <p>{selectedRecommendation.action}</p>
            </div>

            <div className="evidence-box">
              <span>Evidence</span>
              <p>{selectedRecommendation.evidence}</p>
            </div>

            <div className="modal-actions">
              <button>Create Ad Brief</button>
              <button className="secondary">View Creatives</button>
            </div>
          </section>
        </div>
      )}
    </main>
  );
}
