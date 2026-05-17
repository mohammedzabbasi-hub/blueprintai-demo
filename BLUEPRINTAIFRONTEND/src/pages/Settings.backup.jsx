import { Settings as SettingsIcon, CheckCircle2, Video, Library, Mail, Palette, ShieldCheck } from "lucide-react";

export default function Settings() {
  return (
    <div className="min-h-screen bg-[#08111f] text-white px-8 py-10">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="flex items-center gap-5 mb-8">
          <div className="h-16 w-16 rounded-2xl bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center">
            <SettingsIcon className="h-8 w-8 text-cyan-300" />
          </div>

          <div>
            <h1 className="text-5xl font-extrabold tracking-tight">
              Settings
            </h1>
            <p className="text-xl text-slate-400 mt-2">
              Manage your BlueprintAI workspace, analysis preferences, and app setup.
            </p>
          </div>
        </div>

        {/* Main Panel */}
        <div className="rounded-3xl border border-slate-700/70 bg-[#0b1322] p-12 shadow-2xl">

          {/* Workspace Profile */}
          <section className="mb-10">
            <div className="mb-8">
              <h2 className="text-3xl font-bold">Workspace Profile</h2>
              <p className="text-slate-400 text-lg mt-2">
                Basic information about your BlueprintAI workspace.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-7">
              <SettingField label="Workspace Name" value="BlueprintAI" />
              <SettingField label="Main Platform" value="TikTok Shop" />
              <SettingField label="Primary Goal" value="Creative intelligence" />
              <SettingField label="Account Type" value="MVP Testing" />
            </div>
          </section>

          {/* Video Analysis Preferences */}
          <SectionCard
            icon={<Video className="h-6 w-6 text-cyan-300" />}
            title="Video Analysis Preferences"
            description="Control how uploaded videos are processed."
          >
            <div className="space-y-6">
              <div>
                <p className="text-slate-500 font-semibold mb-3 text-lg">
                  Analysis Depth
                </p>
                <select className="w-full rounded-2xl bg-[#111c2e] border border-slate-700 px-5 py-4 text-white text-lg outline-none focus:border-cyan-400">
                  <option>Standard Analysis</option>
                  <option>Deep Creative Analysis</option>
                  <option>Fast MVP Analysis</option>
                </select>
              </div>

              <ToggleRow
                title="Auto-save analyzed videos"
                description="Automatically save completed video analyses into the Creative Library."
              />

              <ToggleRow
                title="Email analysis summaries"
                description="Send a short summary after a video analysis is completed."
              />
            </div>
          </SectionCard>

          {/* Creative Library Defaults */}
          <SectionCard
            icon={<Library className="h-6 w-6 text-cyan-300" />}
            title="Creative Library Defaults"
            description="Customize how saved creatives are organized."
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-7">
              <SettingField label="Default Product Label" value="Unknown Product" />
              <SettingField label="Default Creator Label" value="Uploaded Creator" />
              <SettingField label="Default Source" value="Uploaded Video" />
              <SettingField label="Default Sort" value="Newest First" />
            </div>
          </SectionCard>

          {/* Status */}
          <SectionCard
            icon={<ShieldCheck className="h-6 w-6 text-cyan-300" />}
            title="Status"
            description="Current app setup health."
          >
            <div className="space-y-5">
              <StatusRow label="Backend" status="Connected" />
              <StatusRow label="Video Analysis" status="Working" />
              <StatusRow label="Speech-to-Text" status="Enabled" />
              <StatusRow label="Creative Library" status="In Progress" />
            </div>
          </SectionCard>

          {/* Appearance */}
          <SectionCard
            icon={<Palette className="h-6 w-6 text-cyan-300" />}
            title="Appearance"
            description="Basic UI preferences."
          >
            <ToggleRow
              title="Dark Mode"
              description="Visual preference only. Full theme support can be added later."
            />
          </SectionCard>

          {/* MVP Checklist */}
          <section className="mt-10">
            <h2 className="text-3xl font-bold mb-2">MVP Checklist</h2>
            <p className="text-slate-400 text-lg mb-7">
              Recommended next steps.
            </p>

            <div className="space-y-4 text-lg">
              <ChecklistItem checked text="Upload videos" />
              <ChecklistItem checked text="Generate analysis" />
              <ChecklistItem checked text="Clean results page" />
              <ChecklistItem text="Save to Creative Library" />
              <ChecklistItem text="View saved creative details" />
              <ChecklistItem text="Connect TikTok Shop data" />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

function SectionCard({ icon, title, description, children }) {
  return (
    <section className="rounded-3xl border border-slate-700/70 bg-[#08111f] p-8 mb-8">
      <div className="flex items-start gap-4 mb-7">
        <div className="h-12 w-12 rounded-xl bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center">
          {icon}
        </div>

        <div>
          <h2 className="text-3xl font-bold">{title}</h2>
          <p className="text-slate-400 text-lg mt-2">{description}</p>
        </div>
      </div>

      {children}
    </section>
  );
}

function SettingField({ label, value }) {
  return (
    <div>
      <p className="text-slate-500 font-semibold mb-3 text-lg">{label}</p>
      <div className="rounded-2xl bg-[#111c2e] border border-slate-700 px-5 py-4 text-white text-lg font-semibold">
        {value}
      </div>
    </div>
  );
}

function ToggleRow({ title, description }) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-[#0b1322] p-6 flex items-center justify-between gap-6">
      <div>
        <h3 className="text-xl font-bold">{title}</h3>
        <p className="text-slate-400 text-lg mt-2">{description}</p>
      </div>

      <button className="w-16 h-9 rounded-full bg-slate-700 relative shrink-0">
        <span className="absolute left-1 top-1 h-7 w-7 rounded-full bg-slate-300" />
      </button>
    </div>
  );
}

function StatusRow({ label, status }) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-[#0b1322] px-6 py-5 flex items-center justify-between">
      <span className="text-slate-400 text-lg font-semibold">{label}</span>
      <span className="rounded-full bg-cyan-400 text-[#08111f] px-5 py-2 text-sm font-extrabold">
        {status}
      </span>
    </div>
  );
}

function ChecklistItem({ checked = false, text }) {
  return (
    <div className="flex items-center gap-3">
      {checked ? (
        <CheckCircle2 className="h-6 w-6 text-green-400" />
      ) : (
        <div className="h-6 w-6 rounded-md border border-slate-500 bg-slate-200" />
      )}
      <span className={checked ? "text-slate-300" : "text-slate-500"}>
        {text}
      </span>
    </div>
  );
}
