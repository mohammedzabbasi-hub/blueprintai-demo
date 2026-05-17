import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

export default function CreativeLibrary() {
  const [creatives, setCreatives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [hookType, setHookType] = useState("");
  const [creatorType, setCreatorType] = useState("");

  useEffect(() => {
    const run = async () => {
      try {
        setLoading(true);
        const res = await fetch("/creatives", {
          headers: { "Content-Type": "application/json" },
        });

        if (!res.ok) throw new Error("Failed to load creatives");
        const json = await res.json();
        setCreatives(json);
      } catch (err) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    run();
  }, []);

  const filtered = useMemo(() => {
    return creatives.filter((item) => {
      const matchesSearch =
        !search ||
        item.title?.toLowerCase().includes(search.toLowerCase()) ||
        item.product?.toLowerCase().includes(search.toLowerCase()) ||
        item.creator?.toLowerCase().includes(search.toLowerCase());

      const matchesHook = !hookType || item.hook_type === hookType;
      const matchesCreator = !creatorType || item.creator_type === creatorType;

      return matchesSearch && matchesHook && matchesCreator;
    });
  }, [creatives, search, hookType, creatorType]);

  const hookOptions = [...new Set(creatives.map((c) => c.hook_type).filter(Boolean))];
  const creatorOptions = [...new Set(creatives.map((c) => c.creator_type).filter(Boolean))];

  return (
    <div className="min-h-screen bg-white p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Creative Library</h1>
          <p className="text-sm text-gray-600 mt-1">
            Compare hooks, creator types, humor, delivery, and performance
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <input
            className="border rounded-xl px-3 py-2"
            placeholder="Search creatives..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <select
            className="border rounded-xl px-3 py-2"
            value={hookType}
            onChange={(e) => setHookType(e.target.value)}
          >
            <option value="">All hook types</option>
            {hookOptions.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>

          <select
            className="border rounded-xl px-3 py-2"
            value={creatorType}
            onChange={(e) => setCreatorType(e.target.value)}
          >
            <option value="">All creator types</option>
            {creatorOptions.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>

          <Link
            to="/upload"
            className="border rounded-xl px-3 py-2 flex items-center justify-center"
          >
            Analyze New Video
          </Link>
        </div>

        {loading && <div className="text-sm text-gray-600">Loading creatives...</div>}
        {error && <div className="text-sm text-red-600">{error}</div>}

        {!loading && !error && (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
            {filtered.map((creative) => (
              <Link
                key={creative.id}
                to={`/creatives/${creative.id}`}
                className="border rounded-2xl p-5 block"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h2 className="font-semibold text-lg">{creative.title}</h2>
                    <div className="text-sm text-gray-600 mt-1">
                      {creative.product} · {creative.creator}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-500">Score</div>
                    <div className="font-bold">{creative.score ?? "—"}</div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mt-4 text-xs">
                  <Tag>{creative.hook_type || "No hook tag"}</Tag>
                  <Tag>{creative.creator_type || "No creator tag"}</Tag>
                  <Tag>{creative.humor_style || "No humor tag"}</Tag>
                  <Tag>{creative.delivery_style || "No delivery tag"}</Tag>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4 text-sm">
                  <MiniMetric label="Views" value={creative.views || 0} />
                  <MiniMetric label="Likes" value={creative.likes || 0} />
                  <MiniMetric label="Shares" value={creative.shares || 0} />
                  <MiniMetric label="Clicks" value={creative.clicks || 0} />
                  <MiniMetric label="Orders" value={creative.orders || 0} />
                </div>

                <div className="mt-4 text-sm text-gray-700">
                  {creative.transcript_summary || creative.insight || "No summary yet."}
                </div>
              </Link>
            ))}

            {filtered.length === 0 && (
              <div className="text-sm text-gray-600">No creatives match your filters.</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function Tag({ children }) {
  return <span className="border rounded-full px-2 py-1">{children}</span>;
}

function MiniMetric({ label, value }) {
  return (
    <div className="border rounded-xl p-2">
      <div className="text-gray-500 text-xs">{label}</div>
      <div className="font-medium">{Number(value).toLocaleString()}</div>
    </div>
  );
}