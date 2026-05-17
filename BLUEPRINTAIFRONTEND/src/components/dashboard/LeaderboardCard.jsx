import { Link } from "react-router-dom";

export default function LeaderboardCard({ leaderboard = [] }) {
  return (
    <div className="border rounded-2xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Top Performing Creatives</h2>
        <Link to="/creative-library" className="text-sm underline">
          View full library
        </Link>
      </div>

      <div className="space-y-3">
        {leaderboard.length === 0 && (
          <div className="text-sm text-gray-600">No creative performance data yet.</div>
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
                Hook: {item.hook_type || "—"} · Creator: {item.creator_type || "—"}
              </div>
            </div>

            <div className="flex gap-6 text-sm">
              <div>
                <div className="text-gray-500">Engagement</div>
                <div className="font-semibold">{item.engagement_score}</div>
              </div>
              <div>
                <div className="text-gray-500">Conversion</div>
                <div className="font-semibold">{item.conversion_score}</div>
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
  );
}
