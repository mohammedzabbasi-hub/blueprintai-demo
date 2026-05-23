import { Link } from "react-router-dom";

export default function EmptyWorkspaceState({
  title = "No data yet",
  description = "This new shop does not have data yet. Upload a creative or connect your TikTok Shop to begin.",
  primaryText = "Upload Creative",
  primaryLink = "/upload",
  secondaryText = "Connect Shop",
  secondaryLink = "/connect-shop",
}) {
  return (
    <div className="rounded-3xl border border-cyan-900 bg-[#0b1220] p-10">
      <p className="text-cyan-400 font-black tracking-[0.25em] uppercase">
        New Workspace
      </p>

      <h2 className="text-4xl font-black mt-4">{title}</h2>

      <p className="text-slate-400 mt-4 text-lg max-w-3xl">
        {description}
      </p>

      <div className="flex flex-wrap gap-4 mt-8">
        <Link
          to={primaryLink}
          className="rounded-xl bg-cyan-500 px-6 py-3 font-black text-white"
        >
          {primaryText}
        </Link>

        <Link
          to={secondaryLink}
          className="rounded-xl border border-slate-700 px-6 py-3 font-black text-slate-200"
        >
          {secondaryText}
        </Link>
      </div>
    </div>
  );
}
