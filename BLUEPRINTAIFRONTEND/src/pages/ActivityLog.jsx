import { useMemo, useState } from "react";
import { clearActivityLog, getActivityLog } from "../services/activityLog";

function formatDate(date) {
  return new Date(date).toLocaleString();
}

function badgeColor(type) {
  if (type.includes("video")) return "bg-sky-500/15 text-sky-300";
  if (type.includes("brief")) return "bg-purple-500/15 text-purple-300";
  if (type.includes("blueprint")) return "bg-emerald-500/15 text-emerald-300";
  if (type.includes("shop")) return "bg-amber-500/15 text-amber-300";
  return "bg-white/10 text-slate-300";
}

export default function ActivityLog() {
  const [logs, setLogs] = useState(getActivityLog());
  const [filter, setFilter] = useState("all");

  const filteredLogs = useMemo(() => {
    if (filter === "all") return logs;
    return logs.filter((log) => log.type === filter);
  }, [logs, filter]);

  const types = ["all", ...new Set(logs.map((log) => log.type))];

  function handleClear() {
    clearActivityLog();
    setLogs([]);
  }

  return (
    <section className="min-h-screen bg-[#070b18] text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="border border-white/10 rounded-3xl p-8 bg-[#0a1020]">
          <p className="text-sky-400 text-xs font-bold tracking-[0.25em] uppercase">
            Workspace History
          </p>

          <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
            <div>
              <h1 className="text-5xl font-black mt-4">Activity Log</h1>
              <p className="text-slate-400 mt-3">
                Track video analyses, ad briefs, blueprint generations, saved creatives, and shop connections.
              </p>
            </div>

            <button
              onClick={handleClear}
              className="rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-3 text-red-200 font-bold"
            >
              Clear Log
            </button>
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          {types.map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`rounded-xl px-4 py-2 font-bold border ${
                filter === type
                  ? "bg-sky-500 text-white border-sky-400"
                  : "bg-white/5 text-slate-300 border-white/10"
              }`}
            >
              {type}
            </button>
          ))}
        </div>

        <div className="mt-6 space-y-4">
          {filteredLogs.length === 0 ? (
            <div className="border border-white/10 rounded-2xl p-8 bg-[#0d1526] text-slate-400">
              No activity has been logged yet.
            </div>
          ) : (
            filteredLogs.map((log) => (
              <div key={log.id} className="border border-white/10 rounded-2xl p-6 bg-[#0d1526]">
                <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                  <div>
                    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-bold ${badgeColor(log.type)}`}>
                      {log.type}
                    </span>

                    <h2 className="text-xl font-bold mt-3">{log.title}</h2>
                    <p className="text-slate-400 mt-2">{log.description}</p>

                    <div className="mt-4 text-sm text-slate-500">
                      <p>User: {log.user_name} · {log.user_email}</p>
                      <p>Shop ID: {log.shop_id}</p>
                    </div>
                  </div>

                  <p className="text-sm text-slate-500">{formatDate(log.created_at)}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  );
}
