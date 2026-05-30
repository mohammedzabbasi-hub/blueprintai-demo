import { useEffect, useState } from "react";
import EmptyWorkspaceState from "../components/EmptyWorkspaceState";
import { API_BASE, getSelectedShopId } from "../lib/accountContext";

function formatBriefDescription(brief) {
  if (brief.description || brief.content || brief.summary) {
    return brief.description || brief.content || brief.summary;
  }

  if (brief.structure) return brief.structure;

  if (Array.isArray(brief.script)) {
    return brief.script
      .map((scene) => scene.direction || scene.goal)
      .filter(Boolean)
      .join(" ");
  }

  if (brief.hook_type || brief.creator_type || brief.visual_style) {
    return [brief.hook_type, brief.creator_type, brief.visual_style]
      .filter(Boolean)
      .join(" · ");
  }

  return "";
}

export default function AdBriefs() {
  const [briefs, setBriefs] = useState([]);
  const [loading, setLoading] = useState(true);
  const shopId = getSelectedShopId();

  useEffect(() => {
    async function load() {
      const res = await fetch(`${API_BASE}/briefs?shop_id=${shopId}`);
      const data = await res.json();

      setBriefs(Array.isArray(data) ? data : data.briefs || []);
      setLoading(false);
    }

    load().catch((err) => {
      console.error(err);
      setBriefs([]);
      setLoading(false);
    });
  }, [shopId]);

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <p className="text-cyan-400 uppercase tracking-[0.25em] font-black">
          Creative Planning
        </p>
        <h1 className="text-6xl font-black mt-4">Ad Briefs</h1>
        <p className="text-slate-400 mt-5 text-xl">
          Briefs generated from this shop’s real creative patterns.
        </p>
      </div>

      {loading && <p className="text-slate-400">Loading briefs...</p>}

      {!loading && briefs.length === 0 && (
        <EmptyWorkspaceState
          title="No ad briefs yet"
          description="This shop does not have enough creative data to generate personalized ad briefs yet. Upload or analyze creatives first."
          primaryText="Upload Creative"
          primaryLink="/upload"
        />
      )}

      <div className="space-y-6">
        {briefs.map((brief, index) => (
          <div key={brief.id || index} className="rounded-3xl border border-slate-800 bg-[#0b1220] p-7">
            <h2 className="text-3xl font-black">
              {brief.title || brief.brief_title || "Ad Brief"}
            </h2>
            <p className="text-slate-400 mt-4">{formatBriefDescription(brief)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
