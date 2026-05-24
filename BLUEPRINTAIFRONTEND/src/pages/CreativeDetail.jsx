import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { API_BASE, getSelectedShopId } from "../lib/accountContext";

function getAuthHeaders() {
  const token =
    localStorage.getItem("token") ||
    localStorage.getItem("access_token") ||
    localStorage.getItem("authToken");

  return token ? { Authorization: `Bearer ${token}` } : {};
}

function formatMetric(value) {
  const number = Number(value || 0);
  return Number.isFinite(number) ? number.toLocaleString() : value || 0;
}

export default function CreativeDetail() {
  const { id } = useParams();
  const shopId = getSelectedShopId();
  const [creative, setCreative] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCreative() {
      setLoading(true);
      setError("");

      const res = await fetch(
        `${API_BASE}/personalized/creatives/${encodeURIComponent(id)}?shop_id=${encodeURIComponent(shopId)}`,
        { headers: getAuthHeaders() }
      );

      if (!res.ok) {
        throw new Error("Creative not found");
      }

      const data = await res.json();
      setCreative(data);
    }

    loadCreative()
      .catch((err) => {
        console.error(err);
        setCreative(null);
        setError("Creative not found");
      })
      .finally(() => setLoading(false));
  }, [id, shopId]);

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold">Loading creative...</h1>
      </div>
    );
  }

  if (!creative || error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold">Creative not found</h1>
        <Link to="/creative-library" className="text-blue-600 hover:underline">
          Back to Creative Library
        </Link>
      </div>
    );
  }

  const videoUrl = creative.video_url || creative.videoUrl || "";
  const hook = creative.hook_type || creative.hook || "No hook tag";
  const creatorType = creative.creator_type || creative.creatorType || "No creator tag";
  const humor = creative.humor_style || creative.humor || "No humor tag";
  const delivery = creative.delivery_style || creative.delivery || "No delivery tag";
  const insight =
    creative.insight ||
    creative.ai_summary ||
    creative.transcript_summary ||
    "No insight available.";

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="mx-auto max-w-5xl">
        <Link to="/creative-library" className="mb-6 inline-block text-blue-600 hover:underline">
          ← Back to Creative Library
        </Link>

        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h1 className="text-4xl font-bold text-slate-900">{creative.title || "Untitled Creative"}</h1>
          <p className="mt-2 text-slate-600">
            {creative.product || "Product"} · {creative.creator || "Creator"}
          </p>

          <video
            src={videoUrl}
            controls
            className="mt-6 max-h-[600px] w-full rounded-xl border bg-black object-contain"
          />

          <div className="mt-6 flex flex-wrap gap-2">
            <span className="rounded-full border px-3 py-1 text-sm">{hook}</span>
            <span className="rounded-full border px-3 py-1 text-sm">{creatorType}</span>
            <span className="rounded-full border px-3 py-1 text-sm">{humor}</span>
            <span className="rounded-full border px-3 py-1 text-sm">{delivery}</span>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3 md:grid-cols-6">
            <Metric label="Score" value={formatMetric(creative.score)} />
            <Metric label="Views" value={formatMetric(creative.views)} />
            <Metric label="Likes" value={formatMetric(creative.likes)} />
            <Metric label="Shares" value={formatMetric(creative.shares)} />
            <Metric label="Clicks" value={formatMetric(creative.clicks)} />
            <Metric label="Orders" value={formatMetric(creative.orders)} />
          </div>

          <div className="mt-6 rounded-xl border bg-slate-50 p-5">
            <h2 className="text-xl font-bold text-slate-900">Creative Insight</h2>
            <p className="mt-2 text-slate-700">{insight}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-xl border bg-white p-3">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="text-lg font-semibold text-slate-900">{value}</p>
    </div>
  );
}
