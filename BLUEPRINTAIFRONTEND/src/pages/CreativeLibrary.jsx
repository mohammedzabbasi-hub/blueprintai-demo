import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "https://blueprintai-hvgq.onrender.com";

const DEMO_EMAILS = new Set([
  "beauty@demo.com",
  "fitness@demo.com",
  "home@demo.com",
  "agency@demo.com",
]);

function getUser() {
  try {
    return JSON.parse(localStorage.getItem("user") || "{}");
  } catch {
    return {};
  }
}

function getShopId() {
  const user = getUser();
  return (
    user.shop_id ||
    user.shopId ||
    localStorage.getItem("selectedShopId") ||
    localStorage.getItem("shop_id") ||
    1
  );
}

function isDemoAccount() {
  const user = getUser();
  const email = String(user.email || "").toLowerCase();
  return DEMO_EMAILS.has(email) || user.is_demo === true;
}

function numberFormat(value) {
  const num = Number(value || 0);
  return num.toLocaleString();
}

export default function CreativeLibrary() {
  const [creatives, setCreatives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [hookType, setHookType] = useState("all");
  const [creatorType, setCreatorType] = useState("all");

  const demoAccount = isDemoAccount();
  const shopId = getShopId();

  useEffect(() => {
    async function loadCreatives() {
      try {
        setLoading(true);

        if (!demoAccount) {
          setCreatives([]);
          return;
        }

        const res = await fetch(`${API_BASE}/creatives?shop_id=${shopId}`);

        if (!res.ok) {
          setCreatives([]);
          return;
        }

        const data = await res.json();
        setCreatives(Array.isArray(data) ? data : data.creatives || []);
      } catch (err) {
        console.error("Failed to load creatives:", err);
        setCreatives([]);
      } finally {
        setLoading(false);
      }
    }

    loadCreatives();
  }, [demoAccount, shopId]);

  const hookTypes = useMemo(() => {
    const values = creatives.map((c) => c.hook_type || c.hook || "").filter(Boolean);
    return ["all", ...new Set(values)];
  }, [creatives]);

  const creatorTypes = useMemo(() => {
    const values = creatives.map((c) => c.creator_type || c.creator_archetype || "").filter(Boolean);
    return ["all", ...new Set(values)];
  }, [creatives]);

  const filteredCreatives = useMemo(() => {
    return creatives.filter((creative) => {
      const title = `${creative.title || ""} ${creative.product || ""} ${creative.creator || ""}`.toLowerCase();
      const matchesSearch = title.includes(search.toLowerCase());

      const creativeHook = creative.hook_type || creative.hook || "";
      const creativeCreator = creative.creator_type || creative.creator_archetype || "";

      const matchesHook = hookType === "all" || creativeHook === hookType;
      const matchesCreator = creatorType === "all" || creativeCreator === creatorType;

      return matchesSearch && matchesHook && matchesCreator;
    });
  }, [creatives, search, hookType, creatorType]);

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <p className="text-slate-300 uppercase tracking-[0.25em] font-black">
          Creative Intelligence
        </p>
        <h1 className="text-7xl font-black mt-4">Creative Library</h1>
        <p className="text-slate-400 mt-6 text-xl max-w-4xl">
          Compare hooks, creator types, humor, delivery, and performance across your TikTok Shop creatives.
        </p>
      </div>

      {!demoAccount && (
        <div className="rounded-3xl border border-cyan-900 bg-[#0b1220] p-10 mb-8">
          <h2 className="text-3xl font-black">No creatives yet</h2>
          <p className="text-slate-400 mt-4 text-lg">
            This is a newly created shop account, so demo videos are hidden. Upload a TikTok ad or connect shop data to start building your creative library.
          </p>

          <div className="flex gap-4 mt-8">
            <Link
              to="/upload"
              className="rounded-xl bg-cyan-500 px-6 py-3 font-bold text-white"
            >
              Upload Creative
            </Link>

            <Link
              to="/connect-shop"
              className="rounded-xl border border-slate-700 px-6 py-3 font-bold text-slate-200"
            >
              Connect Shop
            </Link>
          </div>
        </div>
      )}

      {demoAccount && (
        <>
          <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-6 mb-8 grid grid-cols-1 md:grid-cols-3 gap-5">
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search creatives..."
              className="rounded-xl bg-slate-900 border border-slate-700 px-5 py-4 text-white"
            />

            <select
              value={hookType}
              onChange={(e) => setHookType(e.target.value)}
              className="rounded-xl bg-slate-900 border border-slate-700 px-5 py-4 text-white"
            >
              {hookTypes.map((item) => (
                <option key={item} value={item}>
                  {item === "all" ? "All hook types" : item}
                </option>
              ))}
            </select>

            <select
              value={creatorType}
              onChange={(e) => setCreatorType(e.target.value)}
              className="rounded-xl bg-slate-900 border border-slate-700 px-5 py-4 text-white"
            >
              {creatorTypes.map((item) => (
                <option key={item} value={item}>
                  {item === "all" ? "All creator types" : item}
                </option>
              ))}
            </select>
          </div>

          {loading && <p className="text-slate-400">Loading creatives...</p>}

          {!loading && filteredCreatives.length === 0 && (
            <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10">
              <h2 className="text-3xl font-black">No creatives found</h2>
              <p className="text-slate-400 mt-3">Try changing your filters.</p>
            </div>
          )}

          <div className="space-y-8">
            {filteredCreatives.map((creative) => (
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
                  <div className="flex justify-between gap-4">
                    <div>
                      <h2 className="text-4xl font-black">
                        {creative.title || "Untitled Creative"}
                      </h2>
                      <p className="text-slate-400 mt-2 text-lg">
                        {creative.product || "Demo Product"} · {creative.creator || creative.promoter_handle || "Creator"}
                      </p>
                    </div>

                    <div className="text-right">
                      <p className="text-slate-400 font-bold">Score</p>
                      <p className="text-cyan-400 text-5xl font-black">
                        {creative.score || creative.creative_score || 8}
                      </p>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-3 mt-6">
                    {[creative.hook_type, creative.creator_type, creative.humor_style, creative.delivery_style]
                      .filter(Boolean)
                      .map((tag) => (
                        <span
                          key={tag}
                          className="rounded-full border border-slate-500 px-4 py-2 font-bold text-slate-200"
                        >
                          {tag}
                        </span>
                      ))}
                  </div>

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

function Metric({ label, value }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/40 p-4">
      <p className="text-slate-400 font-bold">{label}</p>
      <p className="text-white text-2xl font-black mt-2">{numberFormat(value)}</p>
    </div>
  );
}
