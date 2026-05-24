import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#f7f7fb] text-white">
      <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-purple-500 text-white shadow-sm">
              ✦
            </div>
            <span className="text-2xl font-semibold tracking-tight">BlueprintAI</span>
          </div>

          <nav className="hidden items-center gap-10 text-lg text-slate-500 md:flex">
            <a href="#features" className="transition hover:text-white">
              Features
            </a>
            <a href="#how-it-works" className="transition hover:text-white">
              How It Works
            </a>
            <Link to="/support" className="transition hover:text-white">
              Support
            </Link>
          </nav>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="text-lg font-medium text-white transition hover:opacity-70"
            >
              Login
            </Link>
            <Link
              to="/onboarding"
              className="rounded-2xl bg-gradient-to-r from-blue-600 to-purple-500 px-6 py-3 text-lg font-semibold text-white shadow-sm transition hover:scale-[1.02]"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="mx-auto flex max-w-7xl flex-col items-center px-6 pb-20 pt-20 text-center md:pt-28">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-6 py-3 text-lg text-blue-600">
            <span>⚡</span>
            <span>AI-Powered Creative Intelligence</span>
          </div>

          <h1 className="max-w-6xl text-5xl font-black leading-[0.95] tracking-tight text-white md:text-7xl lg:text-[92px]">
            Know Which TikTok Creatives
            <br />
            Will Sell{" "}
            <span className="bg-gradient-to-r from-blue-600 to-purple-500 bg-clip-text text-transparent">
              Before You Make the
              <br />
              Next One
            </span>
          </h1>

          <p className="mt-10 max-w-4xl text-2xl leading-relaxed text-slate-500 md:text-[22px]">
            BlueprintAI helps analyze uploaded creatives and manually imported
            shop data, identifies useful hooks and creator styles, and recommends
            next ad angles for MVP testing.
          </p>

          <div className="mt-12 flex flex-col gap-4 sm:flex-row">
            <Link
              to="/onboarding"
              className="rounded-2xl bg-gradient-to-r from-blue-600 to-purple-500 px-12 py-5 text-2xl font-semibold text-white shadow-md transition hover:scale-[1.02]"
            >
              Get Started Free →
            </Link>

            <a
              href="#how-it-works"
              className="rounded-2xl border border-slate-300 bg-white px-12 py-5 text-2xl font-semibold text-white transition-all duration-300 hover:bg-slate-50 hover:scale-105 hover:-translate-y-0.5"
            >
              <span className="text-white font-bold drop-shadow-[0_0_10px_rgba(34,211,238,0.75)]">Book Demo</span>
            </a>
          </div>

          <div className="mt-14 flex flex-wrap items-center justify-center gap-8 text-xl text-slate-500">
            <div className="flex items-center gap-3">
              <span className="text-green-500">✓</span>
              <span>Demo workspaces available</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-green-500">✓</span>
              <span>Manual CSV/JSON import</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-green-500">✓</span>
              <span>TikTok Shop OAuth/API integration planned</span>
            </div>
          </div>
        </section>

        <section id="features" className="mx-auto max-w-7xl px-6 py-16">
          <div className="grid gap-6 md:grid-cols-3">
            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <h3 className="text-2xl font-semibold">Creative Analysis</h3>
              <p className="mt-4 text-lg leading-8 text-slate-500">
                Break down hooks, formats, creator styles, pacing, and visual
                patterns from uploaded creative assets.
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <h3 className="text-2xl font-semibold">Winning Recommendations</h3>
              <p className="mt-4 text-lg leading-8 text-slate-500">
                Get data-backed recommendations for your next creative direction
                based on the shop data you import into the MVP.
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <h3 className="text-2xl font-semibold">Ad Brief Generation</h3>
              <p className="mt-4 text-lg leading-8 text-slate-500">
                Turn performance insights into clear next-step briefs your team
                can use immediately.
              </p>
            </div>
          </div>
        </section>

        <section id="how-it-works" className="mx-auto max-w-7xl px-6 py-16">
          <div className="rounded-[32px] border border-slate-200 bg-white p-10 shadow-sm">
            <h2 className="text-center text-4xl font-bold md:text-5xl">
              How It Works
            </h2>

            <div className="mt-12 grid gap-8 md:grid-cols-3">
              <div>
                <div className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
                  Step 1
                </div>
                <h3 className="text-2xl font-semibold">Upload creatives</h3>
                <p className="mt-3 text-lg leading-8 text-slate-500">
                  Upload creative assets and manually import CSV/JSON shop data
                  into one organized workspace.
                </p>
              </div>

              <div>
                <div className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-purple-600">
                  Step 2
                </div>
                <h3 className="text-2xl font-semibold">Analyze performance</h3>
                <p className="mt-3 text-lg leading-8 text-slate-500">
                  BlueprintAI identifies the hooks, creators, and structures most
                  associated with the performance data you provide.
                </p>
              </div>

              <div>
                <div className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-blue-600">
                  Step 3
                </div>
                <h3 className="text-2xl font-semibold">Launch the next winner</h3>
                <p className="mt-3 text-lg leading-8 text-slate-500">
                  Use recommendations and briefs to plan the next creative. Direct
                  TikTok Shop OAuth/API sync is planned for a later release.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section id="testimonials" className="mx-auto max-w-7xl px-6 py-16 pb-24">
          <div className="grid gap-6 md:grid-cols-3">
            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <p className="text-lg leading-8 text-slate-600">
                “It helped us stop making random creative bets and focus on what
                actually scales.”
              </p>
              <div className="mt-6 text-base font-semibold text-white">
                Ecommerce Brand Operator
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <p className="text-lg leading-8 text-slate-600">
                “The recommendations felt actionable, not generic. Our team turned
                insights into briefs almost immediately.”
              </p>
              <div className="mt-6 text-base font-semibold text-white">
                Creative Strategist
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <p className="text-lg leading-8 text-slate-600">
                “This is the kind of system media buyers and creative teams both
                actually want to use.”
              </p>
              <div className="mt-6 text-base font-semibold text-white">
                Performance Marketing Lead
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-slate-200 bg-white px-6 py-8">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 text-sm text-slate-500 md:flex-row md:items-center md:justify-between">
          <p>BlueprintAI MVP. Manual import/upload today; TikTok Shop OAuth/API integration planned.</p>
          <div className="flex flex-wrap gap-5 font-semibold">
            <Link to="/privacy" className="hover:text-blue-600">Privacy</Link>
            <Link to="/terms" className="hover:text-blue-600">Terms</Link>
            <Link to="/support" className="hover:text-blue-600">Support</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
