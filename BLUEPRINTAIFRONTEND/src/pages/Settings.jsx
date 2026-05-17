import { useState } from "react";
import {
  Settings as SettingsIcon,
  Store,
  Video,
  Library,
  Activity,
  CheckCircle2,
  Circle,
  User,
  ChevronDown,
  LogOut,
  Sparkles,
} from "lucide-react";

export default function Settings() {
  const [autoSave, setAutoSave] = useState(true);
  const [emailSummaries, setEmailSummaries] = useState(false);
  const [depth, setDepth] = useState("Standard Analysis");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
    window.location.href = "/login";
  };

  return (
    <main className="min-h-screen bg-[#08111f] px-6 py-10 text-white">
      <div className="mx-auto w-full max-w-6xl">
        <header className="mb-10 flex items-start gap-4">
          <div className="grid h-14 w-14 place-items-center rounded-2xl border border-cyan-400/25 bg-cyan-400/10 shadow-lg">
            <SettingsIcon className="h-6 w-6 text-cyan-300" />
          </div>

          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white">
              Settings
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-400">
              Manage your BlueprintAI workspace, demo shop connection, and video analysis preferences.
            </p>
          </div>
        </header>

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
          <Section icon={Sparkles} title="Workspace Profile" description="Identity and goals for this workspace.">
            <Field label="Workspace Name" value="BlueprintAI" />
            <Field label="Main Platform" value="TikTok Shop" />
            <Field label="Primary Goal" value="Creative Intelligence" />
            <Field label="Account Type" value="MVP Testing" />
          </Section>

          <Section icon={Store} title="Connected Shop" description="The demo shop powering your creative analysis.">
            <div className="rounded-xl border border-slate-700 bg-[#111c2e]/80 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold text-white">GlowLab Beauty</p>
                  <p className="text-xs text-slate-400">Demo TikTok Shop</p>
                </div>
                <Badge type="success">Connected</Badge>
              </div>
            </div>

            <button
              onClick={() => (window.location.href = "/connect-shop")}
              className="mt-4 rounded-xl bg-cyan-400 px-4 py-2 text-sm font-bold text-[#08111f] transition hover:bg-cyan-300"
            >
              Change Demo Shop
            </button>

            <p className="mt-3 text-xs text-slate-500">
              Demo mode only. No real TikTok Shop account is being accessed yet.
            </p>
          </Section>

          <Section icon={Video} title="Video Analysis Preferences" description="Control how videos are processed.">
            <label className="mb-2 block text-xs font-medium text-slate-400">
              Analysis Depth
            </label>

            <div className="relative">
              <select
                value={depth}
                onChange={(e) => setDepth(e.target.value)}
                className="w-full appearance-none rounded-xl border border-slate-700 bg-[#111c2e] px-4 py-3 pr-10 text-sm text-white outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"
              >
                <option>Standard Analysis</option>
                <option>Deep Analysis</option>
                <option>Quick Scan</option>
              </select>

              <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            </div>

            <div className="mt-4 divide-y divide-slate-700/70">
              <ToggleRow
                label="Auto-save analyzed videos"
                description="Save results to the Creative Library automatically."
                checked={autoSave}
                onChange={setAutoSave}
              />
              <ToggleRow
                label="Email summaries"
                description="Get a weekly digest of new insights."
                checked={emailSummaries}
                onChange={setEmailSummaries}
              />
            </div>
          </Section>

          <Section icon={Library} title="Creative Library Defaults" description="Defaults applied to newly analyzed videos.">
            <Field label="Default Product Label" value="Unknown Product" />
            <Field label="Default Creator Label" value="Uploaded Creator" />
            <Field label="Default Source" value="Uploaded Video" />
            <Field label="Default Sort" value="Newest First" />
          </Section>

          <Section icon={Activity} title="App Status" description="Live status of BlueprintAI services.">
            <StatusRow label="Backend" status="Connected" type="success" />
            <StatusRow label="Video Analysis" status="Working" type="success" />
            <StatusRow label="Speech-to-Text" status="Enabled" type="info" />
            <StatusRow label="Creative Library" status="In Progress" type="warn" />
          </Section>

          <Section icon={CheckCircle2} title="MVP Checklist" description="Track progress toward the demo milestone.">
            <ul className="divide-y divide-slate-700/60">
              <ChecklistItem label="Upload videos" done />
              <ChecklistItem label="Generate analysis" done />
              <ChecklistItem label="Clean results page" done />
              <ChecklistItem label="Save to Creative Library" done={false} />
              <ChecklistItem label="View saved creative details" done={false} />
              <ChecklistItem label="Connect TikTok Shop data" done={false} />
            </ul>
          </Section>

          <Section icon={User} title="Account" description="Signed in to BlueprintAI.">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="grid h-10 w-10 place-items-center rounded-full border border-slate-700 bg-cyan-400/10 text-sm font-bold text-cyan-300">
                  Y
                </div>

                <div>
                  <p className="text-sm font-medium text-white">you@blueprintai.app</p>
                  <p className="text-xs text-slate-400">Owner · MVP Testing</p>
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-2 rounded-xl border border-slate-700 bg-[#111c2e] px-4 py-2 text-sm font-medium text-white transition hover:border-cyan-400/60 hover:bg-[#14233a]"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            </div>
          </Section>
        </div>

        <footer className="mt-10 text-center text-xs text-slate-500">
          BlueprintAI · MVP build
        </footer>
      </div>
    </main>
  );
}

function Section({ icon: Icon, title, description, children }) {
  return (
    <section className="rounded-3xl border border-slate-700/70 bg-[#0b1322]/95 p-6 shadow-2xl shadow-black/20">
      <header className="mb-5 flex items-start gap-3">
        <div className="grid h-10 w-10 place-items-center rounded-xl border border-cyan-400/25 bg-cyan-400/10 text-cyan-300">
          <Icon className="h-5 w-5" />
        </div>

        <div>
          <h2 className="text-base font-semibold tracking-tight text-white">
            {title}
          </h2>
          {description && <p className="mt-1 text-xs text-slate-400">{description}</p>}
        </div>
      </header>

      {children}
    </section>
  );
}

function Field({ label, value }) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-slate-700/60 py-3 last:border-0">
      <span className="text-sm text-slate-400">{label}</span>
      <span className="text-sm font-medium text-white">{value}</span>
    </div>
  );
}

function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={`relative inline-flex h-6 w-11 items-center rounded-full border transition-colors ${
        checked ? "border-cyan-400/50 bg-cyan-400" : "border-slate-600 bg-slate-700"
      }`}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
          checked ? "translate-x-6" : "translate-x-1"
        }`}
      />
    </button>
  );
}

function ToggleRow({ label, description, checked, onChange }) {
  return (
    <div className="flex items-center justify-between gap-4 py-4">
      <div>
        <p className="text-sm font-medium text-white">{label}</p>
        {description && <p className="text-xs text-slate-400">{description}</p>}
      </div>

      <Toggle checked={checked} onChange={onChange} />
    </div>
  );
}

function StatusRow({ label, status, type }) {
  return (
    <div className="flex items-center justify-between border-b border-slate-700/60 py-3 last:border-0">
      <span className="text-sm text-white">{label}</span>
      <Badge type={type}>{status}</Badge>
    </div>
  );
}

function Badge({ children, type = "success" }) {
  const styles = {
    success: "bg-emerald-400/15 text-emerald-300 border-emerald-400/30",
    info: "bg-cyan-400/15 text-cyan-300 border-cyan-400/30",
    warn: "bg-yellow-400/15 text-yellow-300 border-yellow-400/30",
  };

  return (
    <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${styles[type]}`}>
      {children}
    </span>
  );
}

function ChecklistItem({ label, done }) {
  return (
    <li className="flex items-center gap-3 py-3">
      {done ? (
        <CheckCircle2 className="h-4 w-4 text-cyan-300" />
      ) : (
        <Circle className="h-4 w-4 text-slate-500" />
      )}

      <span className={`text-sm ${done ? "text-white" : "text-slate-400"}`}>
        {label}
      </span>
    </li>
  );
}
