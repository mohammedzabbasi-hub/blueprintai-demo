import { useEffect, useState } from "react";
import EmptyWorkspaceState from "../components/EmptyWorkspaceState";
import { API_BASE, getSelectedShopId, isDemoAccount } from "../lib/accountContext";

export default function RevenueBlueprint() {
  const [blueprint, setBlueprint] = useState(null);
  const [shopState, setShopState] = useState(null);
  const [loading, setLoading] = useState(true);
  const demo = isDemoAccount();
  const shopId = getSelectedShopId();

  useEffect(() => {
    async function load() {
      const stateRes = await fetch(`${API_BASE}/personalized/shop-state?shop_id=${shopId}`);
      const state = await stateRes.json();
      setShopState(state);

      const res = await fetch(`${API_BASE}/blueprint/${shopId}/latest`);
      if (res.ok) {
        const data = await res.json();
        setBlueprint(data);
      }

      setLoading(false);
    }

    load().catch((err) => {
      console.error(err);
      setLoading(false);
    });
  }, [shopId]);

  async function generateBlueprint() {
    const res = await fetch(`${API_BASE}/blueprint/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shop_id: shopId }),
    });

    const data = await res.json();
    setBlueprint(data);
  }

  const newEmptyAccount = !demo && !shopState?.has_data && !blueprint;

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <p className="text-cyan-400 uppercase tracking-[0.25em] font-black">
          AI Growth Plan
        </p>
        <h1 className="text-6xl font-black mt-4">Revenue Blueprint</h1>
        <p className="text-slate-400 mt-5 text-xl">
          A shop-specific plan based on this account’s data.
        </p>
      </div>

      {loading && <p className="text-slate-400">Loading blueprint...</p>}

      {!loading && newEmptyAccount && (
        <EmptyWorkspaceState
          title="No blueprint yet"
          description="This new shop does not have enough data for a strong revenue blueprint yet. Upload creatives or connect shop data first."
          primaryText="Upload Creative"
          primaryLink="/upload"
        />
      )}

      {!loading && !newEmptyAccount && !blueprint && (
        <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10">
          <h2 className="text-3xl font-black">Generate your first blueprint</h2>
          <p className="text-slate-400 mt-4">
            This will create a shop-specific growth plan.
          </p>
          <button
            onClick={generateBlueprint}
            className="mt-7 rounded-xl bg-cyan-500 px-6 py-3 font-black text-white"
          >
            Generate Blueprint
          </button>
        </div>
      )}

      {!loading && blueprint && (
        <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10">
          <h2 className="text-4xl font-black">
            {blueprint.title || "AI Growth Blueprint"}
          </h2>
          <p className="text-slate-400 mt-5 text-lg">
            {blueprint.summary || blueprint.diagnosis || "Your blueprint is ready."}
          </p>

          <button
            onClick={generateBlueprint}
            className="mt-7 rounded-xl bg-cyan-500 px-6 py-3 font-black text-white"
          >
            Generate New Blueprint
          </button>

          <div className="space-y-5 mt-8">
            {(blueprint.steps || []).map((step, index) => (
              <div key={step.id || index} className="rounded-2xl border border-slate-800 bg-slate-950/40 p-6">
                <p className="text-cyan-300 font-black">Step {step.step_number || index + 1}</p>
                <h3 className="text-2xl font-black mt-2">{step.title}</h3>
                <p className="text-slate-400 mt-3">{step.description || step.action}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
