import { useEffect, useState } from "react";
import EmptyWorkspaceState from "../components/EmptyWorkspaceState";
import { API_BASE, getSelectedShopId, isDemoAccount } from "../lib/accountContext";

export default function Recommendations() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const demo = isDemoAccount();
  const shopId = getSelectedShopId();

  useEffect(() => {
    async function load() {
      const endpoint = demo
        ? `${API_BASE}/recommendations?shop_id=${shopId}`
        : `${API_BASE}/personalized/recommendations?shop_id=${shopId}`;

      const res = await fetch(endpoint);
      const data = await res.json();

      setItems(Array.isArray(data) ? data : data.recommendations || []);
      setLoading(false);
    }

    load().catch((err) => {
      console.error(err);
      setItems([]);
      setLoading(false);
    });
  }, [demo, shopId]);

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <p className="text-cyan-400 uppercase tracking-[0.25em] font-black">
          Growth Engine
        </p>
        <h1 className="text-6xl font-black mt-4">Recommendations</h1>
        <p className="text-slate-400 mt-5 text-xl">
          Personalized recommendations based on this shop’s creative data.
        </p>
      </div>

      {loading && <p className="text-slate-400">Loading recommendations...</p>}

      {!loading && items.length === 0 && (
        <EmptyWorkspaceState
          title="No recommendations yet"
          description="Recommendations will appear after this shop has uploaded creatives, video analyses, or connected TikTok Shop performance data."
          primaryText="Analyze a Video"
          primaryLink="/upload"
        />
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {items.map((item, index) => (
          <div key={item.id || index} className="rounded-3xl border border-slate-800 bg-[#0b1220] p-7">
            <h2 className="text-2xl font-black">
              {item.title || item.name || item.recommendation || "Recommendation"}
            </h2>
            <p className="text-slate-400 mt-4">
              {item.description || item.details || item.reason || item.action || item.evidence || ""}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
