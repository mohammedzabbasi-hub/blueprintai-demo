import { useEffect, useState } from "react";
import EmptyWorkspaceState from "../components/EmptyWorkspaceState";
import { API_BASE, getAccountLabel, getSelectedShopId, isDemoAccount } from "../lib/accountContext";

function StatCard({ label, value }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-7">
      <p className="text-slate-400 font-bold">{label}</p>
      <p className="text-5xl font-black mt-4">{value}</p>
    </div>
  );
}

export default function Index() {
  const [data, setData] = useState(null);
  const demo = isDemoAccount();
  const shopId = getSelectedShopId();
  const account = getAccountLabel();

  useEffect(() => {
    async function loadDashboard() {
      const endpoint = demo
        ? `${API_BASE}/analytics/dashboard?shop_id=${shopId}`
        : `${API_BASE}/personalized/dashboard?shop_id=${shopId}`;

      const res = await fetch(endpoint);
      const json = await res.json();
      setData(json);
    }

    loadDashboard().catch((err) => {
      console.error(err);
      setData({ has_data: false, counts: {} });
    });
  }, [demo, shopId]);

  const counts = data?.counts || data || {};
  const hasData = demo || data?.has_data;

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <p className="text-cyan-400 font-black tracking-[0.25em] uppercase">
          {account.shopName}
        </p>
        <h1 className="text-6xl font-black mt-4">Dashboard</h1>
        <p className="text-slate-400 mt-4 text-xl">
          {demo ? "Demo shop intelligence overview." : "Your personalized shop workspace."}
        </p>
      </div>

      {!hasData && (
        <EmptyWorkspaceState
          title="Your dashboard is empty"
          description="This new account has no creative, order, recommendation, or analysis data yet. Upload your first TikTok ad or connect shop data to start filling the dashboard."
        />
      )}

      {hasData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <StatCard label="Creatives" value={counts.creatives || counts.total_creatives || 0} />
          <StatCard label="Recommendations" value={counts.recommendations || 0} />
          <StatCard label="Briefs" value={counts.briefs || 0} />
          <StatCard label="Activity" value={counts.activity || 0} />
        </div>
      )}
    </div>
  );
}
