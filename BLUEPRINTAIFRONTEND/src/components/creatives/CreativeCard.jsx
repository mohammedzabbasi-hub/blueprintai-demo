import { Link } from "react-router-dom";
import CreativeMetricsRow from "./CreativeMetricsRow";

function Tag({ children }) {
  return <span className="border rounded-full px-2 py-1">{children}</span>;
}

export default function CreativeCard({ creative }) {
  return (
    <Link
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

      <CreativeMetricsRow creative={creative} />

      <div className="mt-4 text-sm text-gray-700">
        {creative.transcript_summary || creative.insight || "No summary yet."}
      </div>
    </Link>
  );
}
