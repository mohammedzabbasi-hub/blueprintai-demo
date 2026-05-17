import { useState } from "react";
import { logActivity } from "../services/activityLog";
import "../ad-briefs.css";

const API_BASE = "http://127.0.0.1:8000";

export default function AdBriefs() {
  const [productName, setProductName] = useState("");
  const [brandName, setBrandName] = useState("");
  const [brief, setBrief] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function generateBrief(e) {
    e.preventDefault();

    if (!productName.trim()) {
      setError("Enter a product name first.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setBrief(null);

      const res = await fetch(`${API_BASE}/briefs/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_name: productName,
          brand_name: brandName || "BluePrintAI Demo Brand",
        }),
      });

      const json = await res.json();

      if (!res.ok) {
        throw new Error(json?.detail || "Failed to generate brief.");
      }

      setBrief(json);

      logActivity(
        "ad_brief",
        "Ad brief generated",
        `Generated an ad brief for ${productName}.`,
        {
          product_name: productName,
          brand_name: brandName || "BluePrintAI Demo Brand",
          brief: json,
        }
      );

      logActivity(
        "ad_brief",
        "Ad brief generated",
        `Generated an ad brief for ${productName}.`,
        {
          product_name: productName,
          brand_name: brandName || "BluePrintAI Demo Brand",
          brief: json,
        }
      );
    } catch (err) {
      setError(err.message || "Failed to generate brief.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="ad-briefs-page">
      <div className="ad-briefs-shell">
        <div className="ad-briefs-hero">
          <p className="ad-briefs-eyebrow">Creative Strategy</p>
          <h1>Ad Brief Generator</h1>
          <p>
            Generate creative strategy briefs based on TikTok Shop creative patterns.
          </p>
        </div>

        <form onSubmit={generateBrief} className="ad-briefs-form-card">
          <div className="ad-briefs-input-grid">
            <label>
              Product Name
              <input
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="Example: HydraGlow Serum"
              />
            </label>

            <label>
              Brand Name
              <input
                value={brandName}
                onChange={(e) => setBrandName(e.target.value)}
                placeholder="Example: GlowLab Beauty"
              />
            </label>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate Brief"}
          </button>

          {error && <div className="ad-briefs-error">{error}</div>}
        </form>

        {brief && (
          <div className="ad-briefs-result-card">
            <div className="ad-briefs-result-header">
              <p>Generated Brief</p>
              <h2>{brief.title || `${productName} Creative Brief`}</h2>
            </div>

            <div className="ad-briefs-result-grid">
              <div>
                <h3>Main Angle</h3>
                <p>{brief.angle || brief.main_angle || "Highlight the product benefit clearly in the first 3 seconds."}</p>
              </div>

              <div>
                <h3>Target Audience</h3>
                <p>{brief.target_audience || "TikTok Shop viewers interested in practical product solutions."}</p>
              </div>

              <div>
                <h3>Hook</h3>
                <p>{brief.hook || "Stop scrolling — this product solves a problem you deal with every day."}</p>
              </div>

              <div>
                <h3>CTA</h3>
                <p>{brief.cta || "Tap to shop now."}</p>
              </div>
            </div>

            <div className="ad-briefs-result-section">
              <h3>Creative Direction</h3>
              <p>
                {brief.creative_direction ||
                  brief.description ||
                  brief.summary ||
                  "Use a short-form TikTok style video with a clear hook, product demo, benefit text, and direct call to action."}
              </p>
            </div>

            <div className="ad-briefs-result-section">
              <h3>Recommended Shots</h3>
              <ul>
                {(brief.shots || brief.recommended_shots || [
                  "Open with the problem or desired result.",
                  "Show the product clearly in use.",
                  "Add benefit-focused on-screen text.",
                  "End with a strong CTA."
                ]).map((item, index) => (
                  <li key={index}>• {item}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
