import { useEffect, useState } from "react";
import { Check, Sparkles, Store } from "lucide-react";
import { getCurrentDemoUser, setUserSelectedShop, userCanAccessShop } from "../services/demoAuth";
import { logActivity } from "../services/activityLog";

const API_BASE = "http://127.0.0.1:8000";

export default function ConnectShop() {
  const [shops, setShops] = useState([]);
  const [selectedShopId, setSelectedShopId] = useState(localStorage.getItem("selectedShopId") || "1");
  const [loading, setLoading] = useState(true);
  const user = getCurrentDemoUser();

  useEffect(() => {
    async function loadShops() {
      try {
        const res = await fetch(`${API_BASE}/demo/shops`);
        const data = await res.json();

        const list = Array.isArray(data) ? data : data.shops || [];
        const filtered = list.filter((shop) => userCanAccessShop(shop.id || shop.shop_id));

        setShops(filtered);
      } catch {
        setShops([
          { id: 1, shop_name: "GlowLab Beauty", category: "Beauty & Personal Care", region: "US", creatives: 17, creators: 4 },
          { id: 2, shop_name: "FitPulse Gear", category: "Fitness Accessories", region: "US", creatives: 17, creators: 4 },
          { id: 3, shop_name: "HomeEase Finds", category: "Home & Kitchen", region: "US", creatives: 17, creators: 4 },
          { id: 4, shop_name: "StyleNest Apparel", category: "Fashion", region: "US", creatives: 15, creators: 4 },
          { id: 5, shop_name: "TechTok Gadgets", category: "Consumer Electronics", region: "US", creatives: 14, creators: 4 },
        ].filter((shop) => userCanAccessShop(shop.id)));
      } finally {
        setLoading(false);
      }
    }

    loadShops();
  }, []);

  function connectShop(shopId) {
    setUserSelectedShop(shopId);
    setSelectedShopId(String(shopId));

    const shopToLog = shops.find(
      (shop) => String(shop.id || shop.shop_id) === String(shopId)
    );

    logActivity(
      "shop_connected",
      "Shop connected",
      `Connected ${shopToLog?.shop_name || shopToLog?.name || "a demo shop"} to this workspace.`,
      {
        shop_id: shopId,
        shop_name: shopToLog?.shop_name || shopToLog?.name,
      }
    );
  }

  function continueToDashboard() {
    window.location.href = "/dashboard";
  }

  return (
    <section className="min-h-screen bg-[#070b18] text-white p-8">
      <div className="max-w-7xl mx-auto">
        <div className="border border-white/10 rounded-3xl p-8 bg-[#0a1020]">
          <div className="flex items-start gap-5">
            <div className="w-14 h-14 rounded-2xl bg-sky-500/15 text-sky-300 flex items-center justify-center">
              <Sparkles size={26} />
            </div>

            <div>
              <h1 className="text-4xl font-black">Connect Shop</h1>
              <p className="text-slate-400 mt-2">
                Choose one demo TikTok Shop dataset to power BlueprintAI.
              </p>

              {user && (
                <p className="text-sky-300 mt-3">
                  Signed in as {user.name} · {user.email}
                </p>
              )}
            </div>
          </div>

          {loading ? (
            <div className="mt-10 text-slate-400">Loading shops...</div>
          ) : (
            <div className="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-6">
              {shops.map((shop) => {
                const id = shop.id || shop.shop_id;
                const name = shop.shop_name || shop.name;
                const connected = String(selectedShopId) === String(id);

                return (
                  <div
                    key={id}
                    className={`rounded-3xl border p-6 bg-[#0d1526] ${
                      connected ? "border-sky-400/60" : "border-white/10"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h2 className="text-2xl font-bold">{name}</h2>
                        <p className="text-slate-400 mt-2">
                          {shop.category || "TikTok Shop"} · {shop.region || "US"}
                        </p>
                      </div>

                      {connected && (
                        <div className="w-10 h-10 rounded-full bg-emerald-500/15 text-emerald-300 flex items-center justify-center">
                          <Check size={20} />
                        </div>
                      )}
                    </div>

                    <div className="grid grid-cols-2 gap-4 mt-6">
                      <div className="rounded-xl border border-white/10 p-4">
                        <p className="text-slate-500">Creatives</p>
                        <p className="text-xl font-bold">{shop.creatives || shop.total_creatives || 17}</p>
                      </div>

                      <div className="rounded-xl border border-white/10 p-4">
                        <p className="text-slate-500">Creators</p>
                        <p className="text-xl font-bold">{shop.creators || shop.total_creators || 4}</p>
                      </div>
                    </div>

                    <button
                      onClick={() => connectShop(id)}
                      className="mt-6 w-full rounded-xl bg-sky-500 hover:bg-sky-400 px-5 py-3 font-bold text-white"
                    >
                      {connected ? "Connected" : `Connect ${name}`}
                    </button>
                  </div>
                );
              })}
            </div>
          )}

          <button
            onClick={continueToDashboard}
            className="mt-8 rounded-xl bg-gradient-to-r from-sky-400 to-blue-500 px-6 py-3 font-bold text-white"
          >
            Continue to Dashboard
          </button>
        </div>
      </div>
    </section>
  );
}
