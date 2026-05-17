import { useEffect, useMemo, useState } from "react";
import TopBar from "../components/dashboard/TopBar";
import StatCards from "../components/dashboard/StatCards";
import PerformanceChart from "../components/dashboard/PerformanceChart";
import TopCreatives from "../components/dashboard/TopCreatives";
import PatternInsights from "../components/dashboard/PatternInsights";
import NextActions from "../components/dashboard/NextActions";

import { getEngineAnalysis } from "../services/engineApi";

function getSelectedShopId() {
  return (
    localStorage.getItem("selectedShopId") ||
    localStorage.getItem("shop_id") ||
    localStorage.getItem("demoShopId") ||
    "1"
  );
}

function itemMatchesSearch(item, query) {
  if (!query) return true;
  if (item === null || item === undefined) return false;

  if (typeof item === "string" || typeof item === "number") {
    return String(item).toLowerCase().includes(query);
  }

  if (Array.isArray(item)) {
    return item.some((entry) => itemMatchesSearch(entry, query));
  }

  if (typeof item === "object") {
    return Object.values(item).some((value) => itemMatchesSearch(value, query));
  }

  return false;
}

function filterDashboardData(data, search) {
  const query = search.trim().toLowerCase();

  if (!query || !data) return data;

  const clone = structuredClone(data);

  function filterArrays(obj) {
    if (!obj || typeof obj !== "object") return obj;

    Object.keys(obj).forEach((key) => {
      const value = obj[key];

      if (Array.isArray(value)) {
        obj[key] = value.filter((item) => itemMatchesSearch(item, query));
      } else if (value && typeof value === "object") {
        filterArrays(value);
      }
    });

    return obj;
  }

  return filterArrays(clone);
}

export default function Dashboard() {
  const [dateRange, setDateRange] = useState("30d");
  const [search, setSearch] = useState("");
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const shopId = getSelectedShopId();

  const filteredDashboardData = useMemo(() => {
    return filterDashboardData(dashboardData, search);
  }, [dashboardData, search]);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const engineData = await getEngineAnalysis(shopId);

        const data = {
          ...engineData,
          shop: {
            id: engineData.shop_id,
            shop_name: engineData.shop_name,
            name: engineData.shop_name,
          },
          totals: engineData.totals || {},
          patterns: engineData.patterns || {},
          recommendations: engineData.strategy?.recommendations || [],
          next_actions: engineData.strategy?.recommendations || [],
          top_creatives: engineData.scored_creatives || [],
          leaderboard: engineData.scored_creatives || [],
          issues: engineData.issues || [],
          strategy: engineData.strategy || {},
        };

        setDashboardData(data);
      } catch (err) {
        console.error("Dashboard load error:", err);
        setError("Could not load dashboard data. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [shopId]);

  return (
    <div className="min-h-screen bg-[#0a0f1e] text-white px-6 py-6">
      <div className="max-w-[1400px] mx-auto space-y-6">
        <TopBar
          dateRange={dateRange}
          onDateRangeChange={setDateRange}
          search={search}
          onSearchChange={setSearch}
        />

        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">
            {dashboardData?.shop?.shop_name || dashboardData?.shop?.name || "BluePrintAI"} Dashboard
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            TikTok Shop creative intelligence, performance patterns, and next actions for this connected shop.
          </p>
        </div>

        {loading && (
          <div className="bg-[#0d1526] border border-white/5 rounded-xl p-5 text-sm text-slate-400">
            Loading dashboard data...
          </div>
        )}

        {error && (
          <div className="bg-rose-500/10 border border-rose-500/20 rounded-xl p-5 text-sm text-rose-300">
            {error}
          </div>
        )}

        {!loading && !error && (
          <>
            <StatCards data={dashboardData} />

            {search.trim() && (
              <div className="bg-sky-500/10 border border-sky-500/20 rounded-xl p-4 text-sm text-sky-200">
                Showing dashboard matches for "{search}".
              </div>
            )}

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              <div className="xl:col-span-2">
                <PerformanceChart dateRange={dateRange} data={dashboardData} />
              </div>

              <div>
                <PatternInsights data={filteredDashboardData} />
              </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              <div className="xl:col-span-2">
                <TopCreatives data={filteredDashboardData} />
              </div>

              <div>
                <NextActions data={filteredDashboardData} />
              </div>
            </div>

            
          </>
        )}
      </div>
    </div>
  );
}
