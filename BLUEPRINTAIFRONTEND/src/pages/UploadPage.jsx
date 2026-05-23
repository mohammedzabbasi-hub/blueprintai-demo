import { API_BASE, getSelectedShopId } from "../lib/accountContext";
import { useState } from "react";
import { logActivity } from "../services/activityLog";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function scoreLabel(score) {
  if (score >= 8) return "Strong";
  if (score >= 5) return "Needs Testing";
  return "Weak";
}

function predictImpact(analysis) {
  const hook = Number(analysis.hook_score || 0);
  const cta = Number(analysis.cta_score || 0);
  const clarity = Number(analysis.clarity_score || 0);
  const avg = (hook + cta + clarity) / 3;

  if (avg >= 7) {
    return {
      level: "High",
      reason: "Strong hook, clear message, and CTA give this creative stronger conversion potential.",
    };
  }

  if (avg >= 4) {
    return {
      level: "Medium",
      reason: "The creative has some usable elements, but weak clarity or CTA may limit TikTok Shop conversions.",
    };
  }

  return {
    level: "Low",
    reason: "Weak CTA, unclear benefit, and low hook strength make this unlikely to convert well without revision.",
  };
}

function getWinningPattern(analysis) {
  const hook = Number(analysis.hook_score || 0);
  const cta = Number(analysis.cta_score || 0);
  const clarity = Number(analysis.clarity_score || 0);

  const missing = [];
  if (hook < 6) missing.push("strong hook");
  if (cta < 6) missing.push("clear CTA");
  if (clarity < 6) missing.push("clear benefit text");

  return {
    matches: hook >= 7 && cta >= 7 && clarity >= 7 ? "Yes" : "No",
    closest: analysis.creator_style || "Product Demo",
    missing: missing.length ? missing.join(", ") : "No major missing pattern detected",
  };
}

function getAdClassification(analysis, metadata) {
  const style = analysis.creator_style || "Product demonstration";
  const duration = Number(metadata.duration_seconds || 0);

  return {
    format: `${style} / short-form ad`,
    style,
    bestUse:
      duration > 60
        ? "Retargeting or product education, not cold traffic"
        : "Cold traffic test or retargeting creative",
  };
}

function rewriteAd(analysis) {
  const summary = `${analysis.summary || ""}`.toLowerCase();

  if (summary.includes("old spice") || summary.includes("deodorant")) {
    return {
      hook: "Most deodorants fade by noon — this one does not.",
      cta: "Tap to shop Old Spice now.",
      angle: "Lead with the product benefit, then show the result clearly.",
    };
  }

  return {
    hook: "Stop scrolling — this fixes the problem you deal with every day.",
    cta: "Tap to shop now.",
    angle: "Open with the pain point, show the product in action, then end with a direct CTA.",
  };
}

function ScoreCard({ label, value }) {
  const score = Number(value || 0);

  return (
    <div className="bg-[#0d1526] border border-white/10 rounded-2xl p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="text-4xl font-bold text-white mt-2">{score}/10</p>
      <p className="text-xs text-sky-300 mt-2">{scoreLabel(score)}</p>
    </div>
  );
}

function SectionCard({ title, subtitle, children, accent = false }) {
  return (
    <div
      className={`bg-[#0d1526] border ${
        accent ? "border-sky-500/25" : "border-white/10"
      } rounded-2xl p-6`}
    >
      <h3 className="text-lg font-bold text-white">{title}</h3>
      {subtitle && <p className="text-sm text-slate-500 mt-1">{subtitle}</p>}
      <div className="mt-4 text-slate-300 leading-relaxed">{children}</div>
    </div>
  );
}

function ListCard({ title, items = [], accent = false }) {
  return (
    <SectionCard title={title} accent={accent}>
      <ul className="space-y-3">
        {items.length ? (
          items.map((item, index) => <li key={index}>• {item}</li>)
        ) : (
          <li>No data available.</li>
        )}
      </ul>
    </SectionCard>
  );
}

function VideoAdBreakdown({ result, file }) {
  const payload = result?.result || {};
  const analysis = payload?.analysis || {};
  const metadata = payload?.metadata || {};
  const transcript = payload?.transcript || {};
  const ocrText = payload?.ocr_text || [];

  const hookScore = Number(analysis.hook_score || 0);
  const ctaScore = Number(analysis.cta_score || 0);
  const clarityScore = Number(analysis.clarity_score || 0);

  const impact = predictImpact(analysis);
  const pattern = getWinningPattern(analysis);
  const classification = getAdClassification(analysis, metadata);
  const rewrite = rewriteAd(analysis);

  const detectedText = ocrText
    .map((item) => item.text)
    .filter(Boolean)
    .slice(0, 5)
    .join(" | ");

  function saveToCreativeLibrary() {
    const saved = JSON.parse(localStorage.getItem("creativeLibrary") || "[]");

    const newCreative = {
      id: Date.now(),
      filename: result?.filename || file?.name || "Uploaded Creative",
      saved_at: new Date().toISOString(),
      hook_score: hookScore,
      cta_score: ctaScore,
      clarity_score: clarityScore,
      impact: impact.level,
      summary: analysis.summary,
      strengths: analysis.strengths || [],
      weaknesses: analysis.weaknesses || [],
      recommendations: analysis.recommendations || [],
      full_result: result,
    };

    localStorage.setItem("creativeLibrary", JSON.stringify([newCreative, ...saved]));
    logActivity(
      "creative_saved",
      "Creative saved to library",
      analysis.summary || "A video analysis was saved to the creative library.",
      {
        filename: result?.filename || file?.name,
        hook_score: hookScore,
        cta_score: ctaScore,
        clarity_score: clarityScore,
      }
    );

    logActivity(
      "creative_saved",
      "Creative saved to library",
      analysis.summary || "A video analysis was saved to the creative library.",
      {
        filename: result?.filename || file?.name,
        hook_score: hookScore,
        cta_score: ctaScore,
        clarity_score: clarityScore,
      }
    );

    alert("Saved to Creative Library.");
  }

  function generateBlueprint() {
    const blueprint = {
      id: Date.now(),
      title: `Blueprint from ${result?.filename || file?.name || "Video Analysis"}`,
      created_at: new Date().toISOString(),
      main_goal: "Improve creative performance and TikTok Shop conversion potential.",
      diagnosis: analysis.summary,
      recommended_tests: [
        rewrite.hook,
        rewrite.cta,
        "Add clearer product-benefit text on screen.",
        "Test a creator voiceover version.",
      ],
      source_analysis: result,
    };

    localStorage.setItem("latestVideoBlueprint", JSON.stringify(blueprint));
    logActivity(
      "blueprint_generated",
      "Blueprint generated from video analysis",
      analysis.summary || "A blueprint was generated from a video analysis.",
      {
        filename: result?.filename || file?.name,
        recommended_tests: blueprint.recommended_tests,
      }
    );

    logActivity(
      "blueprint_generated",
      "Blueprint generated from video analysis",
      analysis.summary || "A blueprint was generated from a video analysis.",
      {
        filename: result?.filename || file?.name,
        recommended_tests: blueprint.recommended_tests,
      }
    );

    alert("Blueprint generated from this analysis.");
  }

  function downloadReport() {
    const report = {
      filename: result?.filename || file?.name,
      generated_at: new Date().toISOString(),
      performance_prediction: impact,
      winning_pattern_match: pattern,
      ad_classification: classification,
      rewrite_this_ad: rewrite,
      analysis,
      metadata,
      transcript,
      detected_text: detectedText,
      full_result: result,
    };

    const blob = new Blob([JSON.stringify(report, null, 2)], {
      type: "application/json",
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "blueprintai-video-analysis-report.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="mt-10 space-y-6">
      <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
        <div>
          <p className="text-sky-400 text-xs font-bold tracking-[0.25em] uppercase">
            Creative Intelligence Report
          </p>
          <h2 className="text-3xl font-black text-white mt-2">Video Ad Breakdown</h2>
          <p className="text-slate-400 mt-2">
            Hook, messaging, visual clarity, CTA strength, format, predicted impact, and next-test recommendations.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={saveToCreativeLibrary}
            className="px-4 py-2 rounded-xl bg-white/10 border border-white/10 text-white font-semibold hover:bg-white/15"
          >
            Save to Creative Library
          </button>

          <button
            onClick={generateBlueprint}
            className="px-4 py-2 rounded-xl bg-sky-500/20 border border-sky-500/30 text-sky-200 font-semibold hover:bg-sky-500/30"
          >
            Generate Blueprint
          </button>

          <button
            onClick={downloadReport}
            className="px-4 py-2 rounded-xl bg-blue-500 text-white font-semibold hover:bg-blue-400"
          >
            Download Report
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ScoreCard label="Hook Score" value={hookScore} />
        <ScoreCard label="CTA Score" value={ctaScore} />
        <ScoreCard label="Clarity Score" value={clarityScore} />
      </div>

      <SectionCard title="Executive Summary">
        <p>{analysis.summary || "No summary available."}</p>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <SectionCard title="Performance Prediction" subtitle="Predicted TikTok Shop impact" accent>
          <p className="text-3xl font-black text-white">{impact.level}</p>
          <p className="mt-3">{impact.reason}</p>
        </SectionCard>

        <SectionCard title="Winning Pattern Match" subtitle="How close this ad is to a winning creative">
          <p><strong>Matches Winning Pattern:</strong> {pattern.matches}</p>
          <p className="mt-2"><strong>Closest Pattern:</strong> {pattern.closest}</p>
          <p className="mt-2"><strong>Missing:</strong> {pattern.missing}</p>
        </SectionCard>

        <SectionCard title="Ad Type / Format Classification" subtitle="Creative format and best use">
          <p><strong>Format:</strong> {classification.format}</p>
          <p className="mt-2"><strong>Style:</strong> {classification.style}</p>
          <p className="mt-2"><strong>Best Use:</strong> {classification.bestUse}</p>
        </SectionCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <SectionCard title="Hook Analysis" subtitle="First 3 seconds and scroll-stopping power">
          <p>
            The opening hook scored <strong>{hookScore}/10</strong>.{" "}
            {hookScore >= 7
              ? "The opening is strong enough to earn attention."
              : "A stronger first 3 seconds should quickly show the problem, result, or product payoff."}
          </p>
        </SectionCard>

        <SectionCard title="Messaging Angle" subtitle="Main selling angle detected">
          <p>
            Detected creator style: <strong>{analysis.creator_style || "Not clearly detected"}</strong>.
          </p>
          <p className="mt-2">
            The core benefit should be made clearer earlier, especially for viewers watching without sound.
          </p>
        </SectionCard>

        <SectionCard title="Visual Elements" subtitle="Branding, text, product focus">
          <p>
            Detected text:{" "}
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
              : "The ad should clearly tell the viewer what to do next."}
          </p>
        </SectionCard>
      </div>

      <SectionCard title="Rewrite This Ad" subtitle="Suggested creative variation to test next" accent>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Better Hook</p>
            <p className="text-white font-semibold mt-2">“{rewrite.hook}”</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Better CTA</p>
            <p className="text-white font-semibold mt-2">“{rewrite.cta}”</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Better Angle</p>
            <p className="text-white font-semibold mt-2">{rewrite.angle}</p>
          </div>
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <ListCard title="Strengths" items={analysis.strengths || []} />
        <ListCard title="Weaknesses" items={analysis.weaknesses || []} />
        <ListCard title="Recommendations" items={analysis.recommendations || []} accent />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <SectionCard title="Ad Format">
          <p>Duration: {metadata.duration_seconds ? `${metadata.duration_seconds.toFixed(1)} seconds` : "Unknown"}</p>
          <p>Size: {metadata.width || "?"} × {metadata.height || "?"}</p>
          <p>FPS: {metadata.fps || "Unknown"}</p>
        </SectionCard>

        <SectionCard title="Transcript Review">
          <p>{transcript.full_text || "No clear transcript detected."}</p>
        </SectionCard>

        <SectionCard title="Next Test Plan" accent>
          <ul className="space-y-3">
            <li>• Test a stronger first 3-second hook.</li>
            <li>• Add clearer product-benefit text on screen.</li>
            <li>• Add a direct CTA near the end.</li>
            <li>• Test a creator voiceover version.</li>
          </ul>
        </SectionCard>
      </div>
    </section>
  );
}


async function saveCreativeToShop(analysisResult) {
  const shopId = getSelectedShopId();

  try {
    await fetch(`${API_BASE}/personalized/creatives`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        shop_id: shopId,
        title: analysisResult?.title || analysisResult?.filename || "Uploaded Creative",
        product: analysisResult?.product || "Uploaded Product",
        creator: "Uploaded by user",
        video_url: analysisResult?.video_url || analysisResult?.videoUrl || "",
        thumbnail: analysisResult?.thumbnail || "",
        insight: analysisResult?.insight || analysisResult?.summary || "",
        transcript: analysisResult?.transcript || "",
        transcript_summary: analysisResult?.transcript_summary || analysisResult?.summary || "",
        hook_type: analysisResult?.hook_type || analysisResult?.hook || "",
        creator_type: analysisResult?.creator_type || "",
        humor_style: analysisResult?.humor_style || "",
        delivery_style: analysisResult?.delivery_style || "",
        score: analysisResult?.score || analysisResult?.creative_score || 0,
      }),
    });
  } catch (err) {
    console.warn("Could not save creative to shop:", err);
  }
}

export default function VideoAnalysis() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [warning, setWarning] = useState("");
  const [loading, setLoading] = useState(false);

  function handleFileChange(e) {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    setResult(null);
    setError("");
    setWarning("");

    if (!selectedFile) return;

    const sizeMb = selectedFile.size / (1024 * 1024);

    if (sizeMb > 100) {
      setWarning("Large video detected. For fastest analysis, use TikTok-style clips under 60 seconds or under 100MB.");
    } else if (sizeMb > 50) {
      setWarning("For best results, upload a short TikTok-style creative under 60 seconds.");
    }
  }

  async function handleAnalyze() {
    if (!file) {
      setError("Choose a video file first.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/video-analysis/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.detail || "Video analysis failed.");
      }

      setResult(data);
      await saveCreativeToShop(data);

      logActivity(
        "video_analysis",
        "Video analysis created",
        data?.result?.analysis?.summary || "A new video creative was analyzed.",
        {
          filename: data?.filename,
          hook_score: data?.result?.analysis?.hook_score,
          cta_score: data?.result?.analysis?.cta_score,
          clarity_score: data?.result?.analysis?.clarity_score,
        }
      );

      logActivity(
        "video_analysis",
        "Video analysis created",
        data?.result?.analysis?.summary || "A new video creative was analyzed.",
        {
          filename: data?.filename,
          hook_score: data?.result?.analysis?.hook_score,
          cta_score: data?.result?.analysis?.cta_score,
          clarity_score: data?.result?.analysis?.clarity_score,
        }
      );
    } catch (err) {
      setError(err.message || "Video analysis failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="min-h-screen bg-[#070b18] text-white p-8">
      <div className="border border-white/10 rounded-3xl p-8 bg-[#0a1020]">
        <p className="text-sky-400 text-xs font-bold tracking-[0.25em] uppercase">
          Creative Intelligence
        </p>

        <h1 className="text-6xl font-black mt-4">Video Analysis</h1>

        <p className="text-slate-300 text-lg mt-4 max-w-4xl">
          Upload a TikTok-style video and BlueprintAI will break down the hook, clarity, CTA, transcript, pacing, and creative structure.
        </p>

        <div className="mt-10 border border-white/10 rounded-2xl p-6">
          <h2 className="text-2xl font-bold">Upload your creative</h2>
          <p className="text-slate-400 mt-2">
            Choose a TikTok ad, product demo, UGC clip, or creator video.
          </p>

          <div className="mt-6 border border-dashed border-white/20 rounded-2xl p-6 flex items-center justify-between gap-4">
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="text-slate-300"
            />
            <p className="text-slate-400 text-sm">{file?.name || "No file selected"}</p>
          </div>

          {warning && (
            <div className="mt-4 border border-amber-500/30 bg-amber-500/10 rounded-xl p-4 text-amber-200">
              {warning}
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="mt-6 px-6 py-3 rounded-xl bg-gradient-to-r from-sky-400 to-blue-500 text-white font-bold disabled:opacity-60"
          >
            {loading ? "Analyzing video..." : "Analyze Video"}
          </button>

          {loading && (
            <div className="mt-6 border border-sky-500/20 bg-sky-500/10 rounded-xl p-5">
              <p className="text-sky-200 font-semibold">Analyzing your creative...</p>
              <p className="text-slate-400 mt-2">
                Extracting frames, reading on-screen text, checking transcript, scoring hook, CTA, and clarity.
              </p>
            </div>
          )}

          {error && (
            <div className="mt-6 border border-red-500/30 bg-red-500/10 rounded-xl p-4 text-red-200">
              {error}
            </div>
          )}
        </div>

        {result && <VideoAdBreakdown result={result} file={file} />}
      </div>
    </section>
  );
}
