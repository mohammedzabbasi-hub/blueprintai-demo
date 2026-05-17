import { Flame, Users, TrendingUp, Zap } from "lucide-react";
import { useNavigate } from "react-router-dom";

function getTopProduct(data) {
  const leaderboard = data?.leaderboard || data?.top_creatives || [];
  return leaderboard?.[0]?.product || "your top product";
}

function ActionCard({ icon: Icon, title, description, priority, actionLabel, onClick, color = "sky" }) {
  const colorClasses = {
    rose: "bg-rose-500/15 text-rose-300",
    sky: "bg-sky-500/15 text-sky-300",
    emerald: "bg-emerald-500/15 text-emerald-300",
  };

  const priorityClasses = {
    High: "bg-rose-500/15 text-rose-300",
    Medium: "bg-amber-500/15 text-amber-300",
    Low: "bg-emerald-500/15 text-emerald-300",
  };

  return (
    <div className="border border-white/10 rounded-2xl p-6 bg-[#0d1526]">
      <div className="flex items-start gap-5">
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colorClasses[color]}`}>
          <Icon size={22} />
        </div>

        <div className="flex-1">
          <div className="flex items-start justify-between gap-3">
            <h3 className="text-xl font-bold text-white leading-tight">{title}</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-bold ${priorityClasses[priority]}`}>
              {priority}
            </span>
          </div>

          <p className="mt-3 text-slate-400 leading-relaxed">{description}</p>

          <button
            type="button"
            onClick={onClick}
            className="mt-5 text-sky-300 font-bold hover:text-sky-200 transition-colors"
          >
            {actionLabel} →
          </button>
        </div>
      </div>
    </div>
  );
}

export default function NextActions({ data }) {
  const navigate = useNavigate();
  const topProduct = getTopProduct(data);

  function goGenerateBrief() {
    localStorage.setItem("briefProductName", topProduct);
    localStorage.setItem(
      "briefBrandName",
      data?.shop?.shop_name || data?.shop?.name || "BluePrintAI Demo Brand"
    );
    navigate("/ad-briefs");
  }

  function goFindCreators() {
    localStorage.setItem("creatorSearchFocus", topProduct);
    navigate("/creators");
  }

  function goCreateVariant() {
    const creative = data?.leaderboard?.[0] || data?.top_creatives?.[0] || null;

    localStorage.setItem(
      "variantSourceCreative",
      JSON.stringify({
        product: topProduct,
        title: creative?.title || `Demo TikTok creative for ${topProduct}`,
        hook_type: creative?.hook_type || "shock fact",
        creator_type: creative?.creator_type || "UGC creator",
        recommendation: "Create a new hook, CTA, and product-benefit version from this top creative.",
      })
    );

    navigate("/revenue-blueprint");
  }

  return (
    <div className="bg-[#0d1526] border border-white/10 rounded-2xl p-6">
      <div className="flex items-center gap-4 mb-6">
        <div className="w-12 h-12 bg-sky-500/15 flex items-center justify-center text-sky-300">
          <Zap size={22} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white">Recommended Actions</h2>
          <p className="text-slate-400">Generated from connected shop patterns</p>
        </div>
      </div>

      <div className="space-y-5">
        <ActionCard
          icon={Flame}
          title="Scale shock fact creatives"
          description={`Your connected shop shows shock fact as a leading hook pattern. Create 3 to 5 more variants using this opening angle for ${topProduct}.`}
          priority="High"
          actionLabel="Generate Brief"
          color="rose"
          onClick={goGenerateBrief}
        />

        <ActionCard
          icon={Users}
          title="Recruit more target collaboration creators"
          description="Target collaboration creators are showing up most in this shop's winning creative mix. Prioritize creators with similar delivery style."
          priority="High"
          actionLabel="Find Creators"
          color="sky"
          onClick={goFindCreators}
        />

        <ActionCard
          icon={TrendingUp}
          title="Turn the top creative into variants"
          description={`"${data?.leaderboard?.[0]?.title || `Demo TikTok creative for ${topProduct}`}" is one of your top performers. Test new CTAs, new first 3 seconds, and a product-benefit version.`}
          priority="Medium"
          actionLabel="Create Variant"
          color="emerald"
          onClick={goCreateVariant}
        />
      </div>
    </div>
  );
}
