import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

function getConnectedShopId() {
  return (
    localStorage.getItem("connected_shop_id") ||
    localStorage.getItem("selected_shop_id") ||
    localStorage.getItem("shop_id")
  );
}

export default function Recommendations() {
  const [data, setData] = useState(null);
  const [activeCategory, setActiveCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadRecommendations() {
    try {
      setLoading(true);
      setError("");

      const shopId = getConnectedShopId();

      if (!shopId) {
        throw new Error("No shop connected. Connect a demo shop first.");
      }

      const res = await fetch(`/recommendations?shop_id=${shopId}`, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        throw new Error("Failed to load recommendations");
      }

      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRecommendations();
  }, []);

  const recommendations = data?.recommendations || [];
  const summary = data?.summary || {};
  const shop = data?.shop || {};

  const categories = useMemo(() => {
    return ["All", ...new Set(recommendations.map((item) => item.category).filter(Boolean))];
  }, [recommendations]);

  const filteredRecommendations =
    activeCategory === "All"
      ? recommendations
      : recommendations.filter((item) => item.category === activeCategory);

  return (
    <div className="min-h-screen bg-white text-black p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs text-gray-600 mb-3">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              Connected Demo Shop
            </div>

            <h1 className="text-3xl font-bold">
              Recommendations{shop?.name ? ` for ${shop.name}` : ""}
            </h1>

            <p className="text-sm text-gray-600 mt-1">
              AI-style creative actions based on hooks, creators, clicks, orders, and conversion patterns.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={loadRecommendations}
              className="px-4 py-2 rounded-xl border border-gray-300"
            >
              Refresh
            </button>

            <Link
              to="/connect-shop"
              className="px-4 py-2 rounded-xl border border-gray-300"
            >
              Switch Shop
            </Link>
          </div>
        </div>

        {loading && <div className="text-sm text-gray-600">Loading recommendations...</div>}

        {error && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-5 text-red-700">
            <div className="font-semibold">Recommendations failed to load</div>
            <div className="text-sm mt-1">{error}</div>
            <Link to="/connect-shop" className="underline text-sm mt-3 inline-block">
              Connect a shop
            </Link>
          </div>
        )}

        {!loading && !error && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <MetricCard label="Creative Score" value={`${summary.creative_score || 0}/100`} />
              <MetricCard label="CTR" value={`${summary.ctr || 0}%`} />
              <MetricCard label="Conversion Rate" value={`${summary.conversion_rate || 0}%`} />
              <MetricCard label="Expected Lift" value={summary.expected_lift || "—"} />
            </div>

            <div className="rounded-2xl border bg-gray-50 p-5">
              <div className="text-sm text-gray-500">Top priority</div>
              <div className="text-xl font-semibold mt-1">
                {summary.top_priority || "No recommendation yet"}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Best opportunity: {summary.best_opportunity || "Collect more creative data"}
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setActiveCategory(category)}
                  className={`rounded-full border px-4 py-2 text-sm ${
                    activeCategory === category
                      ? "bg-black text-white border-black"
                      : "bg-white text-gray-700 border-gray-300"
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
              {filteredRecommendations.map((item) => (
                <div key={item.id} className="border rounded-2xl p-5 bg-white">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="text-xs text-gray-500">{item.category}</div>
                      <h2 className="text-xl font-semibold mt-1">{item.name}</h2>
                    </div>

                    <div className="text-right">
                      <div className="text-xs text-gray-500">Confidence</div>
                      <div className="font-bold">{item.confidence ?? "—"}%</div>
                    </div>
                  </div>

                  <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                    <Info label="Type" value={item.rec_type} />
                    <Info label="Priority" value={item.priority} />
                    <Info label="Product" value={item.product_name} />
                  </div>

                  <div className="mt-4">
                    <div className="text-sm text-gray-500">Why this matters</div>
                    <div className="mt-1 text-sm text-gray-800">
                      {item.reason || "No reason provided."}
                    </div>
                  </div>

                  {item.action && (
                    <div className="mt-4">
                      <div className="text-sm text-gray-500">Recommended action</div>
                      <div className="mt-1 text-sm text-gray-800">{item.action}</div>
                    </div>
                  )}

                  {item.evidence && (
                    <div className="mt-4 rounded-xl border bg-gray-50 p-4">
                      <div className="text-sm text-gray-500">Evidence</div>
                      <div className="mt-1 text-sm text-gray-800">{item.evidence}</div>
                    </div>
                  )}

                  <div className="mt-5 flex gap-3">
                    <Link
                      to="/ad-briefs"
                      className="px-4 py-2 rounded-xl bg-black text-white text-sm"
                    >
                      Create Ad Brief
                    </Link>

                    <Link
                      to="/creative-library"
                      className="px-4 py-2 rounded-xl border border-gray-300 text-sm"
                    >
                      View Creatives
                    </Link>
                  </div>
                </div>
              ))}

              {filteredRecommendations.length === 0 && (
                <div className="text-sm text-gray-600">
                  No recommendations available yet.
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function MetricCard({ label, value }) {
  return (
    <div className="border rounded-2xl p-4">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-2xl font-bold mt-1">{value}</div>
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div className="border rounded-xl p-3">
      <div className="text-xs text-gray-500">{label}</div>
      <div className="font-medium mt-1">{value || "—"}</div>
    </div>
  );
}
