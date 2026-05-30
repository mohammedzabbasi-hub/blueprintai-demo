import { useEffect, useState } from "react";
import { API_BASE, getSelectedShopId, getAccountLabel } from "../lib/accountContext";

const tables = ["products", "orders", "creators", "creatives", "metrics"];

function getAuthHeaders() {
  const token =
    localStorage.getItem("token") ||
    localStorage.getItem("access_token") ||
    localStorage.getItem("authToken");

  return token ? { Authorization: `Bearer ${token}` } : {};
}

export default function DataImport() {
  const shopId = getSelectedShopId();
  const account = getAccountLabel();

  const [tableName, setTableName] = useState("products");
  const [csvFile, setCsvFile] = useState(null);
  const [jsonFile, setJsonFile] = useState(null);
  const [summary, setSummary] = useState({});
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadSummary() {
    const res = await fetch(`${API_BASE}/data-import/summary?shop_id=${shopId}`, {
      headers: getAuthHeaders(),
    });
    const data = await res.json();
    setSummary(data.summary || {});
  }

  useEffect(() => {
    loadSummary().catch(console.error);
  }, [shopId]);

  async function uploadCsv() {
    if (!csvFile) {
      setMessage("Choose a CSV file first.");
      return;
    }

    setLoading(true);
    setMessage("");

    const form = new FormData();
    form.append("shop_id", shopId);
    form.append("table_name", tableName);
    form.append("file", csvFile);

    const res = await fetch(`${API_BASE}/data-import/csv`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: form,
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "CSV import failed.");
    } else {
      setMessage(`Imported ${data.inserted} rows into ${data.table}.`);
      await loadSummary();
    }

    setLoading(false);
  }

  async function uploadJson() {
    if (!jsonFile) {
      setMessage("Choose a JSON file first.");
      return;
    }

    setLoading(true);
    setMessage("");

    const form = new FormData();
    form.append("shop_id", shopId);
    form.append("file", jsonFile);

    const res = await fetch(`${API_BASE}/data-import/json`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: form,
    });

    const data = await res.json();

    if (!res.ok) {
      setMessage(data.detail || "JSON import failed.");
    } else {
      const insertedRaw =
        data.inserted_total ??
        data.inserted ??
        data.total_inserted ??
        data.inserted_rows ??
        0;

      const skippedRaw =
        data.skipped_total ??
        data.skipped_duplicates ??
        data.duplicates_skipped ??
        data.skipped_rows ??
        0;

      const sumValue = (value) => {
        if (typeof value === "number") return value;
        if (value && typeof value === "object") {
          return Object.values(value).reduce((sum, item) => sum + Number(item || 0), 0);
        }
        return Number(value || 0);
      };

      const inserted = sumValue(insertedRaw);
      const skipped = sumValue(skippedRaw);

      setMessage(
        `JSON import complete. Imported ${inserted} new rows. Skipped ${skipped} duplicate rows.`
      );
      await loadSummary();
    }

    setLoading(false);
  }

  async function clearData() {
    if (!confirm("Clear imported data for this shop?")) return;

    setLoading(true);

    const res = await fetch(`${API_BASE}/data-import/clear?shop_id=${shopId}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });

    const data = await res.json();
    setMessage(data.success ? "Shop import data cleared." : "Could not clear data.");
    await loadSummary();

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-10">
      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10 mb-8">
        <div className="flex items-center gap-3">
          <p className="text-cyan-400 uppercase tracking-[0.25em] font-black">
            Data Setup
          </p>
          <span className="rounded-full border border-yellow-500/40 bg-yellow-500/10 px-4 py-1 text-xs font-black uppercase tracking-widest text-yellow-200">
            Temporary MVP Only
          </span>
        </div>
        <h1 className="text-6xl font-black mt-4">Import Shop Data</h1>
        <p className="text-slate-400 mt-5 text-xl">
          Temporary MVP tool: upload TikTok Shop CSV/JSON downloads into this workspace until real TikTok Shop OAuth is connected.
        </p>
        <p className="text-slate-500 mt-3">
          Current shop: {account.shopName} · Shop ID: {shopId}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-8">
          <h2 className="text-3xl font-black">Upload CSV</h2>
          <p className="text-slate-400 mt-3">
            Choose which table this CSV should fill.
          </p>

          <select
            value={tableName}
            onChange={(e) => setTableName(e.target.value)}
            className="w-full mt-6 rounded-xl bg-slate-900 border border-slate-700 px-5 py-4 text-white"
          >
            {tables.map((table) => (
              <option key={table} value={table}>
                {table}
              </option>
            ))}
          </select>

          <input
            type="file"
            accept=".csv"
            onChange={(e) => setCsvFile(e.target.files?.[0] || null)}
            className="w-full mt-6 rounded-xl bg-slate-900 border border-slate-700 px-5 py-4"
          />

          <button
            onClick={uploadCsv}
            disabled={loading}
            className="mt-6 rounded-xl bg-cyan-500 px-6 py-3 font-black disabled:opacity-50"
          >
            Upload CSV
          </button>
        </div>

        <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-8">
          <h2 className="text-3xl font-black">Upload JSON Bundle</h2>
          <p className="text-slate-400 mt-3">
            JSON can include products, orders, creators, creatives, and metrics arrays.
          </p>

          <input
            type="file"
            accept=".json"
            onChange={(e) => setJsonFile(e.target.files?.[0] || null)}
            className="w-full mt-6 rounded-xl bg-slate-900 border border-slate-700 px-5 py-4"
          />

          <button
            onClick={uploadJson}
            disabled={loading}
            className="mt-6 rounded-xl bg-cyan-500 px-6 py-3 font-black disabled:opacity-50"
          >
            Upload JSON
          </button>
        </div>
      </div>

      {message && (
        <div className="rounded-2xl border border-cyan-900 bg-cyan-950/30 p-5 mt-8 text-cyan-100 font-bold">
          {message}
        </div>
      )}

      <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-8 mt-8">
        <div className="flex justify-between items-center gap-4">
          <h2 className="text-3xl font-black">Current Imported Data</h2>
          <button
            onClick={clearData}
            className="rounded-xl border border-red-500/40 px-5 py-3 font-bold text-red-200"
          >
            Clear Shop Data
          </button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-5 mt-8">
          {tables.map((table) => (
            <div key={table} className="rounded-2xl bg-slate-950/40 border border-slate-800 p-5">
              <p className="text-slate-400 font-bold">{table}</p>
              <p className="text-4xl font-black mt-3">{summary[table] || 0}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
