import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import EmptyWorkspaceState from "../components/EmptyWorkspaceState";
import { API_BASE, getSelectedShopId, isDemoAccount } from "../lib/accountContext";

function Metric({ label, value }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/40 p-4">
      <p className="text-slate-400 font-bold">{label}</p>
      <p className="text-white text-2xl font-black mt-2">
        {Number(value || 0).toLocaleString()}
      </p>
    </div>
  );
}

export default function CreativeLibrary() {
  const [creatives, setCreatives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const demo = isDemoAccount();
  const shopId = getSelectedShopId();

  useEffect(() => {
    async function loadCreatives() {
      setLoading(true);

      const endpoint = demo
        ? `${API_BASE}/creatives?shop_id=${shopId}`
        : `${API_BASE}/personalized/creatives?shop_id=${shopId}`;

      const res = await fetch(endpoint);
      const data = await res.json();

      setCreatives(Array.isArray(data) ? data : data.creatives || []);
      setLoading(false);
    }

    loadCreatives().catch((err) => {
      console.error(err);
      setCreatives([]);
      setLoading(false);
    });
  }, [demo, shopId]);

  const filtered = useMemo(() => {
    return creatives.filter((creative) => {
      const text = `${creative.title || ""} ${creative.product || ""} ${creative.creator || ""}`.toLowerCase();
      return text.includes(search.toLowerCase());
    });
  }, [creatives, search]);

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <p className="text-cyan-400 uppercase tracking-[0.25em] font-black">
          Creative Intelligence
        </p>
        <h1 className="text-6xl font-black mt-4">Creative Library</h1>
        <p className="text-slate-400 mt-5 text-xl">
          {demo
            ? "Demo creatives are visible for demo accounts."
            : "Only creatives uploaded or saved to this shop will appear here."}
        </p>
      </div>

      {loading && <p className="text-slate-400">Loading creatives...</p>}

      {!loading && filtered.length === 0 && (
        <EmptyWorkspaceState
          title="No creatives yet"
          description="This new shop has no demo videos. Upload your first TikTok ad or connect shop data to begin building your personalized Creative Library."
        />
      )}

      {!loading && filtered.length > 0 && (
        <>
          <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-6 mb-8">
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search creatives..."
              className="w-full rounded-xl bg-slate-900 border border-slate-700 px-5 py-4 text-white"
            />
          </div>

          <div className="space-y-8">
            {filtered.map((creative) => (
              <div
                key={creative.id}
                className="rounded-3xl border border-slate-800 bg-[#0b1220] p-8 grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-8"
              >
                <video
                  src={creative.video_url || creative.videoUrl || ""}
                  poster={creative.thumbnail || creative.thumbnail_url || ""}
                  controls
                  className="w-full rounded-2xl bg-black aspect-video object-cover"
                />

                <div>
                  <h2 className="text-4xl font-black">
                    {creative.title || "Untitled Creative"}
                  </h2>

                  <p className="text-slate-400 mt-2 text-lg">
                    {creative.product || "Product"} · {creative.creator || "Creator"}
                  </p>

                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-7">
                    <Metric label="Views" value={creative.views} />
                    <Metric label="Likes" value={creative.likes} />
                    <Metric label="Shares" value={creative.shares} />
                    <Metric label="Clicks" value={creative.clicks} />
                    <Metric label="Orders" value={creative.orders} />
                  </div>

                  <p className="text-slate-400 mt-7 text-lg">
                    {creative.insight || creative.transcript_summary || "No insight available."}
                  </p>

                  <Link
                    to={`/creatives/${creative.id}`}
                    className="inline-block text-cyan-400 font-black mt-6"
                  >
                    View creative details →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
