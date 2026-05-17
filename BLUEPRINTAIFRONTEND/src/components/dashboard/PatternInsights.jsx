import { Sparkles } from "lucide-react";

const patterns = [
  {
    category: "Hook Types",
    items: [
      { label: "Problem / Pain point", pct: 72, color: "bg-sky-500" },
      { label: "Curiosity tease", pct: 61, color: "bg-blue-500" },
      { label: "Transformation reveal", pct: 54, color: "bg-cyan-500" },
    ],
  },
  {
    category: "Creator Styles",
    items: [
      { label: "Authentic UGC", pct: 81, color: "bg-emerald-500" },
      { label: "Tutorial / How-to", pct: 68, color: "bg-teal-500" },
      { label: "Talking head", pct: 45, color: "bg-green-500" },
    ],
  },
  {
    category: "CTA Patterns",
    items: [
      { label: "Urgency + scarcity", pct: 76, color: "bg-amber-500" },
      { label: "Social proof close", pct: 63, color: "bg-orange-500" },
      { label: "Direct price reveal", pct: 58, color: "bg-yellow-500" },
    ],
  },
  {
    category: "Product Angles",
    items: [
      { label: "Results-first demo", pct: 79, color: "bg-rose-500" },
      { label: "Lifestyle fit", pct: 66, color: "bg-pink-500" },
      { label: "Ingredient education", pct: 41, color: "bg-red-500" },
    ],
  },
];

export default function PatternInsights() {
  return (
    <div className="bg-[#0d1526] border border-white/5 rounded-xl p-5 h-full">
      <div className="flex items-center gap-2 mb-5">
        <div className="w-6 h-6 bg-sky-500/15 rounded-md flex items-center justify-center">
          <Sparkles size={12} className="text-sky-400" />
        </div>

        <div>
          <h2 className="text-[14px] font-semibold text-white leading-none">Pattern Insights</h2>
          <p className="text-[10px] text-slate-500 mt-0.5">Win-rate by creative type</p>
        </div>
      </div>

      <div className="space-y-5">
        {patterns.map((group) => (
          <div key={group.category}>
            <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">
              {group.category}
            </p>

            <div className="space-y-2">
              {group.items.map((item) => (
                <div key={item.label}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[11px] font-medium text-slate-300 truncate max-w-[160px]">
                      {item.label}
                    </span>
                    <span className="text-[11px] font-semibold text-white ml-2 flex-shrink-0">
                      {item.pct}%
                    </span>
                  </div>

                  <div className="h-1.5 bg-white/6 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${item.color} opacity-80 transition-all duration-700`}
                      style={{ width: `${item.pct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
