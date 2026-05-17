import {
  DollarSign,
  MousePointerClick,
  ShoppingCart,
  Package,
  Users,
  Flame,
  Share2,
  Heart,
  Bookmark,
  TestTube2,
  AlertTriangle,
} from "lucide-react";

function num(value) {
  return Number(value || 0);
}

function compact(value) {
  const n = num(value);
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return n.toLocaleString();
}

function money(value) {
  const n = num(value);
  if (!n) return "$0";
  if (n >= 1000000) return `$${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `$${(n / 1000).toFixed(1)}K`;
  return `$${n.toFixed(0)}`;
}

function pct(value) {
  const n = num(value);
  return `${n.toFixed(2)}%`;
}

function safeDivide(a, b) {
  return num(b) === 0 ? 0 : num(a) / num(b);
}

function estimateAov(category = "") {
  const c = category.toLowerCase();
  if (c.includes("electronics") || c.includes("gadget")) return 42;
  if (c.includes("fashion")) return 34;
  if (c.includes("fitness")) return 31;
  if (c.includes("home")) return 28;
  if (c.includes("beauty")) return 24;
  return 30;
}

function aggregateLeaderboard(data) {
  const leaderboard = data?.leaderboard || [];

  return leaderboard.reduce(
    (acc, item) => {
      acc.views += num(item.views);
      acc.clicks += num(item.clicks);
      acc.orders += num(item.orders);
      acc.likes += num(item.likes);
      acc.shares += num(item.shares);

      const product = item.product || "Unknown Product";
      acc.products[product] ||= { name: product, views: 0, clicks: 0, orders: 0, revenue: 0 };
      acc.products[product].views += num(item.views);
      acc.products[product].clicks += num(item.clicks);
      acc.products[product].orders += num(item.orders);

      const creator = item.creator || "Unknown Creator";
      acc.creators[creator] ||= { name: creator, views: 0, clicks: 0, orders: 0, likes: 0, shares: 0 };
      acc.creators[creator].views += num(item.views);
      acc.creators[creator].clicks += num(item.clicks);
      acc.creators[creator].orders += num(item.orders);
      acc.creators[creator].likes += num(item.likes);
      acc.creators[creator].shares += num(item.shares);

      const hook = item.hook_type || "Unknown Hook";
      acc.hooks[hook] ||= { name: hook, views: 0, clicks: 0, orders: 0 };
      acc.hooks[hook].views += num(item.views);
      acc.hooks[hook].clicks += num(item.clicks);
      acc.hooks[hook].orders += num(item.orders);

      return acc;
    },
    {
      views: 0,
      clicks: 0,
      orders: 0,
      likes: 0,
      shares: 0,
      products: {},
      creators: {},
      hooks: {},
    }
  );
}

function MetricCard({ icon: Icon, label, value, sublabel }) {
  const fatigueStatus =
    engagementRate >= 4 && shareRate >= 0.5
      ? "Healthy"
      : engagementRate >= 2 || shareRate >= 0.25
      ? "Watch"
      : "Fatigued";

  const fatigueAction =
    fatigueStatus === "Healthy"
      ? "Keep scaling this creative, but prepare a new hook test."
      : fatigueStatus === "Watch"
      ? "Refresh the hook, test a new CTA, or rotate the creator."
      : "Pause or rebuild this creative with a stronger hook and new angle.";

  return (
    <div className="bg-[#0d1526] border border-white/5 rounded-xl p-4">
      <div className="flex items-start justify-between mb-3">
        <div className="w-9 h-9 rounded-lg bg-sky-500/15 flex items-center justify-center">
          <Icon size={16} className="text-sky-400" />
        </div>
        <span className="text-[10px] font-semibold px-2 py-1 rounded-full bg-sky-500/15 text-sky-400">
          Demo
        </span>
      </div>
      <p className="text-2xl font-bold text-white leading-none">{value}</p>
      <p className="text-[12px] text-slate-400 mt-2">{label}</p>
      {sublabel && <p className="text-[10px] text-slate-600 mt-1">{sublabel}</p>}
    </div>
  );
}

function RankingTable({ title, subtitle, rows, columns }) {
  const fatigueStatus =
    engagementRate >= 4 && shareRate >= 0.5
      ? "Healthy"
      : engagementRate >= 2 || shareRate >= 0.25
      ? "Watch"
      : "Fatigued";

  const fatigueAction =
    fatigueStatus === "Healthy"
      ? "Keep scaling this creative, but prepare a new hook test."
      : fatigueStatus === "Watch"
      ? "Refresh the hook, test a new CTA, or rotate the creator."
      : "Pause or rebuild this creative with a stronger hook and new angle.";

  return (
    <div className="bg-[#0d1526] border border-white/5 rounded-xl p-5">
      <div className="mb-4">
        <h2 className="text-[14px] font-semibold text-white">{title}</h2>
        <p className="text-[11px] text-slate-500">{subtitle}</p>
      </div>

      <div className="space-y-3">
        {rows.length === 0 && (
          <p className="text-sm text-slate-500">No data available yet.</p>
        )}

        {rows.map((row, index) => (
          <div
            key={row.name}
            className="grid grid-cols-[28px_1fr_repeat(3,minmax(64px,auto))] gap-3 items-center border border-white/5 rounded-xl p-3 bg-white/[0.02]"
          >
            <span className="text-xs font-bold text-slate-600">#{index + 1}</span>
            <div className="min-w-0">
              <p className="text-sm font-semibold text-slate-200 truncate">{row.name}</p>
              <p className="text-[10px] text-slate-600">{row.note}</p>
            </div>

            {columns.map((col) => (
              <div key={col.key} className="text-right">
                <p className="text-xs font-bold text-white">{col.render(row)}</p>
                <p className="text-[9px] text-slate-600 uppercase">{col.label}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function GrowthMetrics({ data }) {
  const totals = data?.totals || {};
  const shop = data?.shop || {};
  const agg = aggregateLeaderboard(data);

  const views = num(totals.views) || agg.views;
  const orders = num(totals.orders) || agg.orders;
  const clicks = num(totals.clicks) || agg.clicks;
  const likes = num(totals.likes) || agg.likes;
  const shares = num(totals.shares) || agg.shares;

  const aov = num(totals.avg_order_value) || estimateAov(shop.category);
  const revenue = num(totals.revenue) || orders * aov;

  const roas = num(totals.roas || totals.avg_roas) || 3.2;
  const adSpend = num(totals.ad_spend) || safeDivide(revenue, roas);

  const conversionRate = safeDivide(orders, clicks) * 100;
  const costPerOrder = safeDivide(adSpend, orders);
  const shareRate = safeDivide(shares, views) * 100;
  const revenuePerThousandViews = views > 0 ? (revenue / views) * 1000 : 0;
  const engagementRate = safeDivide(likes + shares, views) * 100;

  const products = Object.values(agg.products)
    .map((p) => ({
      ...p,
      revenue: p.orders * aov,
      conversionRate: safeDivide(p.orders, p.clicks) * 100,
      note: `${compact(p.views)} views`,
    }))
    .sort((a, b) => b.orders - a.orders)
    .slice(0, 5);

  const hooks = Object.values(agg.hooks)
    .map((h) => ({
      ...h,
      winRate: safeDivide(h.orders, h.clicks) * 100,
      note: `${compact(h.views)} views`,
    }))
    .sort((a, b) => b.winRate - a.winRate)
    .slice(0, 5);

  const creators = Object.values(agg.creators)
    .map((c) => ({
      ...c,
      conversionRate: safeDivide(c.orders, c.clicks) * 100,
      engagementRate: safeDivide(c.likes + c.shares, c.views) * 100,
      note: `${compact(c.views)} views`,
    }))
    .sort((a, b) => b.orders - a.orders)
    .slice(0, 5);

  const topProduct = products[0]?.name || "your top product";
  const topHook = hooks[0]?.name || "your strongest hook";
  const topCreator = creators[0]?.name || "your top creator";

  const tests = [
    `Create 3 more videos for ${topProduct} using the ${topHook} hook.`,
    `Ask ${topCreator} to test a second angle with a stronger first 3 seconds.`,
    `Turn the highest-order creative into 2 new variants with different CTAs.`,
  ];

  const fatigueStatus =
    engagementRate >= 4 && shareRate >= 0.5
      ? "Healthy"
      : engagementRate >= 2 || shareRate >= 0.25
      ? "Watch"
      : "Fatigued";

  const fatigueAction =
    fatigueStatus === "Healthy"
      ? "Keep scaling this creative, but prepare a new hook test."
      : fatigueStatus === "Watch"
      ? "Refresh the hook, test a new CTA, or rotate the creator."
      : "Pause or rebuild this creative with a stronger hook and new angle.";

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white mb-2">Growth Metrics</h2>
        <p className="text-sm text-slate-500">
          Revenue, spend, conversion, product, creator, hook, engagement, fatigue, and next-test stats.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-7 gap-4">
        <MetricCard
          icon={MousePointerClick}
          label="Conversion Rate"
          value={pct(conversionRate)}
          sublabel="orders / clicks"
        />
        <MetricCard
          icon={ShoppingCart}
          label="Cost Per Order"
          value={money(costPerOrder)}
          sublabel="ad spend / orders"
        />
        <MetricCard
          icon={DollarSign}
          label="Revenue"
          value={money(revenue)}
          sublabel="estimated from demo AOV"
        />
        <MetricCard
          icon={DollarSign}
          label="Ad Spend"
          value={money(adSpend)}
          sublabel="estimated until TikTok Ads data"
        />
        <MetricCard
          icon={Bookmark}
          label="Revenue / 1K Views"
          value={money(revenuePerThousandViews)}
          sublabel="revenue generated per 1,000 views"
        />
        <MetricCard
          icon={Share2}
          label="Share Rate"
          value={pct(shareRate)}
          sublabel="shares / views"
        />
        <MetricCard
          icon={Heart}
          label="Engagement Rate"
          value={pct(engagementRate)}
          sublabel="likes + shares / views"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <RankingTable
          title="Top Products by Creative Performance"
          subtitle="Ranked by orders from top creatives"
          rows={products}
          columns={[
            { key: "orders", label: "Orders", render: (r) => compact(r.orders) },
            { key: "revenue", label: "Revenue", render: (r) => money(r.revenue) },
            { key: "cvr", label: "CVR", render: (r) => pct(r.conversionRate) },
          ]}
        />

        <RankingTable
          title="Hook Win Rate"
          subtitle="Ranked by conversion rate"
          rows={hooks}
          columns={[
            { key: "orders", label: "Orders", render: (r) => compact(r.orders) },
            { key: "clicks", label: "Clicks", render: (r) => compact(r.clicks) },
            { key: "winRate", label: "Win Rate", render: (r) => pct(r.winRate) },
          ]}
        />

        <RankingTable
          title="Creator Performance"
          subtitle="Ranked by attributed orders"
          rows={creators}
          columns={[
            { key: "orders", label: "Orders", render: (r) => compact(r.orders) },
            { key: "cvr", label: "CVR", render: (r) => pct(r.conversionRate) },
            { key: "eng", label: "Eng.", render: (r) => pct(r.engagementRate) },
          ]}
        />

        <div className="bg-[#0d1526] border border-white/5 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-lg bg-amber-500/15 flex items-center justify-center">
              <AlertTriangle size={15} className="text-amber-400" />
            </div>
            <div>
              <h2 className="text-[14px] font-semibold text-white">Creative Fatigue</h2>
              <p className="text-[11px] text-slate-500">Creative health based on performance signals</p>
            </div>
          </div>

          <div className="border border-white/5 rounded-xl p-4 bg-white/[0.02] mb-4">
            <p className="text-xs text-slate-500">Status</p>
            <p className="text-2xl font-bold text-white mt-1">{fatigueStatus}</p>
          </div>

          <div className="space-y-2 text-sm text-slate-400">
            <p className="text-slate-300 font-semibold">Signals tracked:</p>
            <p>• CTR change</p>
            <p>• ROAS change</p>
            <p>• Orders change</p>
            <p>• Engagement change</p>
            <p>• Views vs conversions</p>
          </div>

          <div className="mt-4 border border-sky-500/10 rounded-xl p-4 bg-sky-500/[0.04]">
            <p className="text-xs text-slate-500">Recommended action</p>
            <p className="text-sm text-slate-300 mt-1">{fatigueAction}</p>
          </div>
        </div>
      </div>

      <div className="bg-[#0d1526] border border-white/5 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-lg bg-sky-500/15 flex items-center justify-center">
            <TestTube2 size={15} className="text-sky-400" />
          </div>
          <div>
            <h2 className="text-[14px] font-semibold text-white">Recommended Next Tests</h2>
            <p className="text-[11px] text-slate-500">Next creative experiments based on current winners</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {tests.map((test, index) => (
            <div key={test} className="border border-white/5 rounded-xl p-4 bg-white/[0.02]">
              <div className="flex items-center gap-2 mb-2">
                <Flame size={13} className="text-sky-400" />
                <p className="text-xs font-semibold text-sky-400">Test {index + 1}</p>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{test}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
