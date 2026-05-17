import { useState } from "react";
import { loginDemoAccount, DEMO_ACCOUNTS } from "../services/demoAuth";

export default function Login() {
  const [email, setEmail] = useState("beauty@demo.com");
  const [password, setPassword] = useState("demo123");
  const [error, setError] = useState("");

  function handleLogin(e) {
    e.preventDefault();

    try {
      loginDemoAccount(email, password);
      window.location.href = "/connect-shop";
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="min-h-screen bg-[#070b18] text-white flex items-center justify-center p-8">
      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="border border-white/10 rounded-3xl p-8 bg-[#0a1020]">
          <p className="text-sky-400 text-xs font-bold tracking-[0.25em] uppercase">
            BlueprintAI Demo Login
          </p>

          <h1 className="text-5xl font-black mt-4">Sign in</h1>

          <p className="text-slate-400 mt-4">
            Use a fake account to simulate how different TikTok Shop owners would see separate shop data.
          </p>

          <form onSubmit={handleLogin} className="mt-8 space-y-5">
            <label className="block">
              <span className="text-sm text-slate-300">Email</span>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-2 w-full rounded-xl bg-white/10 border border-white/10 px-4 py-3 text-white outline-none focus:border-sky-400"
              />
            </label>

            <label className="block">
              <span className="text-sm text-slate-300">Password</span>
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                className="mt-2 w-full rounded-xl bg-white/10 border border-white/10 px-4 py-3 text-white outline-none focus:border-sky-400"
              />
            </label>

            {error && (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-red-200">
                {error}
              </div>
            )}

            <button className="w-full rounded-xl bg-gradient-to-r from-sky-400 to-blue-500 px-5 py-3 font-bold text-white">
              Sign In
            </button>
          </form>
        </div>

        <div className="border border-white/10 rounded-3xl p-8 bg-[#0d1526]">
          <h2 className="text-2xl font-bold">Demo Accounts</h2>
          <p className="text-slate-400 mt-2">
            Each account has different shop access.
          </p>

          <div className="mt-6 space-y-4">
            {DEMO_ACCOUNTS.map((account) => (
              <button
                key={account.id}
                onClick={() => {
                  setEmail(account.email);
                  setPassword(account.password);
                }}
                className="w-full text-left rounded-2xl border border-white/10 bg-white/[0.03] p-4 hover:border-sky-400/40"
              >
                <p className="font-bold text-white">{account.name}</p>
                <p className="text-sky-300 text-sm mt-1">{account.email}</p>
                <p className="text-slate-500 text-sm mt-1">
                  Password: demo123 · Shops: {account.allowedShopIds.join(", ")}
                </p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
