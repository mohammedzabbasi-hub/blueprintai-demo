import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Index() {
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [shopName, setShopName] = useState(
    localStorage.getItem("connected_shop_name") || ""
  );
  const [shopCategory, setShopCategory] = useState(
    localStorage.getItem("connected_shop_category") || ""
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const run = async () => {
      try {
        setLoading(true);
        setError("");

        const shopId = localStorage.getItem("connected_shop_id");
        const savedShopName = localStorage.getItem("connected_shop_name") || "";
        const savedShopCategory =
          localStorage.getItem("connected_shop_category") || "";

        setShopName(savedShopName);
        setShopCategory(savedShopCategory);

        if (!shopId) {
          navigate("/connect-shop");
          return;
        }

        const res = await fetch(`http://127.0.0.1:8000/analytics/dashboard?shop_id=${shopId}`, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!res.ok) {
          throw new Error("Failed to load dashboard analytics");
        }

        const json = await res.json();
        setData(json);
      } catch (err) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    run();
  }, [navigate]);

  const totals = data?.totals || {};
  const leaderboard = data?.leaderboard || [];
  const patterns = data?.patterns || {};

  const displayShopName = shopName || "Connected Shop";

  return (
    <div className="min-h-screen bg-white text-black p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs text-gray-600 mb-3">
              <span className="h-2 w-2 rounded-full bg-green-500" />
              Connected Demo Shop
            </div>

            <h1 className="text-3xl font-bold">
              {displayShopName} Dashboard
            </h1>

            <p className="text-sm text-gray-600 mt-1">
              {shopCategory
                ? `${shopCategory} TikTok Shop creative intelligence overview`
                : "TikTok Shop creative intelligence overview"}
            </p>
          </div>

          <div className="flex gap-3">
            <Link
              to="/upload"
              className="px-4 py-2 rounded-xl bg-black text-white"
            >
              Analyze Video
            </Link>

            <Link
              to="/ad-briefs"
              className="px-4 py-2 rounded-xl border border-gray-300"
            >
              Generate Briefs
            </Link>

            <Link
              to="/connect-shop"
              className="px-4 py-2 rounded-xl border border-gray-300"
            >
              Switch Shop
            </Link>
          </div>
        </div>

        {loading && (
          <div className="text-sm text-gray-600">Loading dashboard...</div>
        )}

        {error && <div className="text-sm text-red-600">{error}</div>}

        {!loading && !error && (
          <>
            <div className="rounded-2xl border bg-gray-50 p-5">
              <div className="text-sm text-gray-500">Currently analyzing</div>
              <div className="text-xl font-semibold mt-1">{displayShopName}</div>
              {shopCategory && (
                <div className="text-sm text-gray-600 mt-1">{shopCategory}</div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-6 gap-4">
              <MetricCard label="Creatives" value={totals.creatives || 0} />
              <MetricCard label="Analyses" value={totals.analyses || 0} />
              <MetricCard label="Briefs" value={totals.briefs || 0} />
              <MetricCard
                label="Recommendations"
                value={totals.recommendations || 0}
              />
              <MetricCard label="Views" value={totals.views || 0} />
              <MetricCard label="Orders" value={totals.orders || 0} />
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <PatternCard title="Top Hook Patterns" items={patterns.hooks || {}} />
              <PatternCard
                title="Top Creator Types"
                items={patterns.creator_types || {}}
              />
              <PatternCard
                title="Top Humor Styles"
                items={patterns.humor_styles || {}}
              />
              <PatternCard
                title="Top Delivery Styles"
                items={patterns.delivery_styles || {}}
              />
            </div>

            <div className="border rounded-2xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold">
                    Top Performing Creatives
                  </h2>
                  <p className="text-sm text-gray-600 mt-1">
                    Best-performing creatives from {displayShopName}.
                  </p>
                </div>

                <Link to="/creative-library" className="text-sm underline">
                  View full library
                </Link>
              </div>

              <div className="space-y-3">
                {leaderboard.length === 0 && (
                  <div className="text-sm text-gray-600">
                    No creative performance data yet.
                  </div>
                )}

                {leaderboard.map((item) => (
                  <div
                    key={item.creative_id}
                    className="border rounded-xl p-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3"
                  >
                    <div>
                      <div className="font-medium">{item.title}</div>
                      <div className="text-sm text-gray-600">{item.product}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        Hook: {item.hook_type || "—"} · Creator:{" "}
                        {item.creator_type || item.creator || "—"}
                      </div>
                    </div>

                    <div className="flex gap-6 text-sm">
                      <div>
                        <div className="text-gray-500">Engagement</div>
                        <div className="font-semibold">
                          {item.engagement_score ?? "—"}
                        </div>
                      </div>

                      <div>
                        <div className="text-gray-500">Conversion</div>
                        <div className="font-semibold">
                          {item.conversion_score ?? "—"}
                        </div>
                      </div>

                      <Link
                        to={`/creatives/${item.creative_id}`}
                        className="underline self-center"
                      >
                        Open
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
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
      <div className="text-2xl font-bold mt-1">
        {Number(value || 0).toLocaleString()}
      </div>
    </div>
  );
}

function PatternCard({ title, items }) {
  const rows = Object.entries(items).sort((a, b) => b[1] - a[1]);

  return (
    <div className="border rounded-2xl p-5">
      <h2 className="text-lg font-semibold mb-4">{title}</h2>

      <div className="space-y-2">
        {rows.length === 0 && (
          <div className="text-sm text-gray-600">No data yet.</div>
        )}

        {rows.map(([name, count]) => (
          <div
            key={name}
            className="flex items-center justify-between border rounded-xl px-3 py-2"
          >
            <span>{name}</span>
            <span className="text-sm text-gray-600">{count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
