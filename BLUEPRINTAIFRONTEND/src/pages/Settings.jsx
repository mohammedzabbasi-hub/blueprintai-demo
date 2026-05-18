import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getSelectedShopId, getStoredShopName, setSelectedShop } from "../lib/shopSession";
import { userCanAccessShop } from "../services/demoAuth";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const FALLBACK_SHOPS = [
  { id: "1", shop_name: "GlowLab Beauty", category: "Beauty & Personal Care", region: "US", creatives: 17, creators: 4 },
  { id: "2", shop_name: "FitPulse Gear", category: "Fitness Accessories", region: "US", creatives: 17, creators: 4 },
  { id: "3", shop_name: "HomeEase Finds", category: "Home & Kitchen", region: "US", creatives: 17, creators: 4 },
  { id: "4", shop_name: "StyleNest Apparel", category: "Fashion", region: "US", creatives: 15, creators: 4 },
  { id: "5", shop_name: "TechTok Gadgets", category: "Consumer Electronics", region: "US", creatives: 14, creators: 4 },
];

function normalizeShop(shop, index) {
  const rawId = shop.id || shop.shop_id || shop.shopId || String(index + 1);
  const numericId = String(rawId).includes("demo_shop_")
    ? String(Number(String(rawId).replace("demo_shop_", "")))
    : String(rawId);

  return {
    ...shop,
    id: numericId,
    shop_name: shop.shop_name || shop.name || `Shop ${numericId}`,
    category: shop.category || shop.industry || "TikTok Shop",
    region: shop.region || "US",
    creatives: shop.creatives_count || shop.total_creatives || shop.creatives || shop.summary?.total_creatives || 0,
    creators: shop.creators_count || shop.total_creators || shop.creators || shop.summary?.total_creators || 0,
  };
}

export default function Settings() {
  const navigate = useNavigate();
  const [shops, setShops] = useState([]);
  const [selectedShopId, setSelectedShopId] = useState(getSelectedShopId());
  const [selectedShopName, setSelectedShopName] = useState(getStoredShopName());
  const [shopModalOpen, setShopModalOpen] = useState(false);
  const [loadingShops, setLoadingShops] = useState(false);

  useEffect(() => {
    async function loadShops() {
      setLoadingShops(true);

      try {
        const res = await fetch(`${API_BASE}/demo/shops`);
        if (!res.ok) throw new Error("Failed to load shops");

        const data = await res.json();
        const list = Array.isArray(data) ? data : data.shops || [];
        const normalized = list.map(normalizeShop).filter((shop) => userCanAccessShop(shop.id));

        setShops(normalized.length ? normalized : FALLBACK_SHOPS);
      } catch {
        setShops(FALLBACK_SHOPS);
      } finally {
        setLoadingShops(false);
      }
    }

    loadShops();
  }, []);

  const activeShop = useMemo(() => {
    return shops.find((shop) => String(shop.id) === String(selectedShopId));
  }, [shops, selectedShopId]);

  function handleSelectShop(shop) {
    setSelectedShop(shop);
    setSelectedShopId(String(shop.id));
    setSelectedShopName(shop.shop_name);
    setShopModalOpen(false);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
    localStorage.removeItem("demoUser");
    localStorage.removeItem("isAuthenticated");
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-[#07111f] text-white px-8 py-10">
      <div className="mx-auto max-w-7xl">
        <div className="mb-10 flex items-center gap-5">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-500/30 bg-cyan-500/10 text-3xl text-cyan-300">
            ⚙
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight">Settings</h1>
            <p className="mt-2 text-slate-400">
              Manage your BlueprintAI workspace, active shop, and video analysis preferences.
            </p>
          </div>
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <section className="rounded-3xl border border-slate-800 bg-[#0b1322] p-7">
            <div className="mb-8 flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-500/30 bg-cyan-500/10 text-cyan-300">
                ✨
              </div>
              <div>
                <h2 className="text-2xl font-black">Workspace Profile</h2>
                <p className="text-slate-400">Identity and goals for this workspace.</p>
              </div>
            </div>

            <div className="space-y-5">
              <div className="flex justify-between border-b border-slate-800 pb-4">
                <span className="text-slate-400">Workspace Name</span>
                <span className="font-bold">BlueprintAI</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-4">
                <span className="text-slate-400">Main Platform</span>
                <span className="font-bold">TikTok Shop</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-4">
                <span className="text-slate-400">Primary Goal</span>
                <span className="font-bold">Creative Intelligence</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Account Type</span>
                <span className="font-bold">MVP Testing</span>
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-800 bg-[#0b1322] p-7">
            <div className="mb-8 flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-500/30 bg-cyan-500/10 text-cyan-300">
                🏬
              </div>
              <div>
                <h2 className="text-2xl font-black">Active Shop</h2>
                <p className="text-slate-400">The shop currently powering your account data.</p>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-700 bg-slate-950/40 p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="text-xl font-black">{activeShop?.shop_name || selectedShopName}</h3>
                  <p className="mt-1 text-slate-400">
                    {activeShop?.category || "Demo TikTok Shop"} · {activeShop?.region || "US"}
                  </p>
                </div>
                <span className="rounded-full bg-emerald-500/15 px-4 py-2 text-sm font-black text-emerald-300">
                  Connected
                </span>
              </div>
            </div>

            <button
              onClick={() => setShopModalOpen(true)}
              className="mt-5 rounded-2xl bg-cyan-500 px-6 py-3 font-black text-white transition hover:bg-cyan-400"
            >
              Manage Shops
            </button>

            <p className="mt-4 text-sm text-slate-400">
              One account can manage multiple shops, but BlueprintAI personalizes pages around one active shop at a time.
            </p>
          </section>

          <section className="rounded-3xl border border-slate-800 bg-[#0b1322] p-7">
            <div className="mb-8 flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-500/30 bg-cyan-500/10 text-cyan-300">
                🎥
              </div>
              <div>
                <h2 className="text-2xl font-black">Video Analysis Preferences</h2>
                <p className="text-slate-400">Control how videos are processed.</p>
              </div>
            </div>

            <div className="space-y-6">
              <label className="block">
                <span className="mb-2 block text-slate-400">Analysis Depth</span>
                <select className="w-full rounded-2xl border border-slate-800 bg-slate-900 px-4 py-4 font-bold outline-none">
                  <option>Standard Analysis</option>
                  <option>Deep Creative Breakdown</option>
                  <option>Fast Summary</option>
                </select>
              </label>

              <div className="flex items-center justify-between border-b border-slate-800 pb-5">
                <div>
                  <p className="font-black">Auto-save analyzed videos</p>
                  <p className="text-sm text-slate-400">Save results to the Creative Library automatically.</p>
                </div>
                <div className="h-7 w-14 rounded-full bg-cyan-500 p-1">
                  <div className="ml-auto h-5 w-5 rounded-full bg-slate-950" />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-black">Email summaries</p>
                  <p className="text-sm text-slate-400">Get a weekly digest of new insights.</p>
                </div>
                <div className="h-7 w-14 rounded-full bg-slate-700 p-1">
                  <div className="h-5 w-5 rounded-full bg-slate-950" />
                </div>
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-800 bg-[#0b1322] p-7">
            <div className="mb-8 flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-cyan-500/30 bg-cyan-500/10 text-cyan-300">
                ▥
              </div>
              <div>
                <h2 className="text-2xl font-black">Creative Library Defaults</h2>
                <p className="text-slate-400">Defaults applied to newly analyzed videos.</p>
              </div>
            </div>

            <div className="space-y-5">
              <div className="flex justify-between border-b border-slate-800 pb-4">
                <span className="text-slate-400">Default Product Label</span>
                <span className="font-bold">Unknown Product</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-4">
                <span className="text-slate-400">Default Creator Label</span>
                <span className="font-bold">Uploaded Creator</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-4">
                <span className="text-slate-400">Default Source</span>
                <span className="font-bold">Uploaded Video</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Default Sort</span>
                <span className="font-bold">Newest First</span>
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-800 bg-[#0b1322] p-7 xl:col-span-2">
            <div className="mb-6 flex items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-black">Account</h2>
                <p className="text-slate-400">Signed in to BlueprintAI.</p>
              </div>
              <button
                onClick={handleLogout}
                className="rounded-2xl border border-slate-700 px-6 py-3 font-black text-slate-300 hover:border-red-400 hover:text-red-300"
              >
                Logout
              </button>
            </div>
          </section>
        </div>
      </div>

      {shopModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 backdrop-blur-sm">
          <div className="max-h-[88vh] w-full max-w-5xl overflow-y-auto rounded-[28px] border border-slate-700 bg-[#0b1322] p-7 shadow-2xl">
            <div className="mb-7 flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-bold uppercase tracking-[0.25em] text-cyan-300">Shop Management</p>
                <h2 className="mt-2 text-3xl font-black">Choose Active Shop</h2>
                <p className="mt-2 text-slate-400">
                  Switching shops updates the data shown across Dashboard, Recommendations, Creators, Ad Briefs, and Blueprint Creation.
                </p>
              </div>

              <button
                onClick={() => setShopModalOpen(false)}
                className="rounded-xl border border-slate-700 px-4 py-2 font-black text-slate-300 hover:border-cyan-400"
              >
                ✕
              </button>
            </div>

            {loadingShops ? (
              <div className="rounded-2xl border border-slate-800 p-6 text-slate-300">Loading shops...</div>
            ) : (
              <div className="grid gap-5 md:grid-cols-2">
                {shops.map((shop) => {
                  const isActive = String(shop.id) === String(selectedShopId);

                  return (
                    <button
                      key={shop.id}
                      onClick={() => handleSelectShop(shop)}
                      className={`rounded-3xl border p-5 text-left transition ${
                        isActive
                          ? "border-cyan-400 bg-cyan-950/25"
                          : "border-slate-800 bg-slate-950/40 hover:border-cyan-700"
                      }`}
                    >
                      <div className="mb-5 flex items-start justify-between gap-4">
                        <div>
                          <h3 className="text-2xl font-black">{shop.shop_name}</h3>
                          <p className="mt-1 text-slate-400">
                            {shop.category} · {shop.region}
                          </p>
                        </div>

                        {isActive && (
                          <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-sm font-black text-emerald-300">
                            Active
                          </span>
                        )}
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div className="rounded-2xl border border-slate-800 p-4">
                          <p className="text-sm text-slate-400">Creatives</p>
                          <p className="mt-1 text-xl font-black">{shop.creatives}</p>
                        </div>
                        <div className="rounded-2xl border border-slate-800 p-4">
                          <p className="text-sm text-slate-400">Creators</p>
                          <p className="mt-1 text-xl font-black">{shop.creators}</p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}

            <div className="mt-7 flex flex-wrap gap-4">
              <button
                onClick={() => alert("Real TikTok Shop OAuth connection will be added here later.")}
                className="rounded-2xl bg-cyan-500 px-6 py-3 font-black text-white hover:bg-cyan-400"
              >
                + Connect New Shop
              </button>

              <button
                onClick={() => setShopModalOpen(false)}
                className="rounded-2xl border border-slate-700 px-6 py-3 font-black text-slate-300 hover:border-cyan-400"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
