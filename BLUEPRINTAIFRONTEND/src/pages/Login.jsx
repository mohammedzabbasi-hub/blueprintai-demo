import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const demoAccounts = [
  {
    name: "GlowLab Beauty Team",
    email: "beauty@demo.com",
    shops: "1",
  },
  {
    name: "FitPulse Gear Team",
    email: "fitness@demo.com",
    shops: "2",
  },
  {
    name: "HomeEase Finds Team",
    email: "home@demo.com",
    shops: "3",
  },
  {
    name: "BlueprintAI Agency Demo",
    email: "agency@demo.com",
    shops: "1, 2, 3, 4, 5",
  },
];

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("beauty@demo.com");
  const [password, setPassword] = useState("demo123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e) {
    e?.preventDefault();

    try {
      setLoading(true);
      setError("");

      const res = await fetch(`${API_BASE}/auth/app-login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.detail || "Login failed.");
      }

      localStorage.setItem("token", data.token);
      localStorage.setItem("access_token", data.token);
      localStorage.setItem("authToken", data.token);

      localStorage.setItem("user", JSON.stringify(data.user));
      localStorage.setItem("selectedShop", JSON.stringify(data.shop));

      if (data.shop?.id) {
        localStorage.setItem("selectedShopId", String(data.shop.id));
        localStorage.setItem("shop_id", String(data.shop.id));
      }

      localStorage.setItem("onboardingComplete", "true");

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      if (err instanceof TypeError && err.message === "Failed to fetch") {
        setError(`Could not reach the backend at ${API_BASE}. Start the FastAPI server or set VITE_API_BASE_URL.`);
      } else {
        setError(err.message || "Invalid email or password.");
      }
    } finally {
      setLoading(false);
    }
  }

  function fillDemo(account) {
    setEmail(account.email);
    setPassword("demo123");
    setError("");
  }

  return (
    <div className="min-h-screen bg-[#070b16] text-white px-8 py-12">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10">
          <p className="text-cyan-400 tracking-[0.3em] uppercase font-black">
            BlueprintAI Login
          </p>

          <h1 className="text-6xl font-black mt-6">Sign in</h1>

          <p className="text-slate-400 mt-6 text-xl">
            Sign in with a demo account or an account created during onboarding.
          </p>
          <p className="mt-4 text-sm leading-6 text-slate-500">
            Current MVP supports demo accounts, onboarding-created workspaces,
            manual import, and creative upload/analysis. TikTok Shop OAuth is
            not live yet.
          </p>

          <form onSubmit={handleLogin} className="mt-12">
            <label className="block text-slate-300 font-bold mb-3">Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-xl border border-slate-800 bg-slate-900 px-5 py-4 text-white text-lg"
              placeholder="you@example.com"
            />

            <label className="block text-slate-300 font-bold mb-3 mt-8">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl border border-slate-800 bg-slate-900 px-5 py-4 text-white text-lg"
              placeholder="Password"
            />

            {error && <p className="text-red-300 mt-5">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-8 rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 px-6 py-4 font-black text-white text-lg disabled:opacity-50"
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>
        </div>

        <div className="rounded-3xl border border-slate-800 bg-[#0b1220] p-10">
          <h2 className="text-4xl font-black">Demo Accounts</h2>
          <p className="text-slate-400 mt-4 text-xl">
            Each account has different shop access.
          </p>

          <div className="space-y-5 mt-10">
            {demoAccounts.map((account) => (
              <button
                key={account.email}
                onClick={() => fillDemo(account)}
                className="w-full text-left rounded-2xl border border-slate-800 bg-slate-950/30 p-6 hover:border-cyan-500 transition"
              >
                <h3 className="text-2xl font-black">{account.name}</h3>
                <p className="text-cyan-300 font-bold mt-2">{account.email}</p>
                <p className="text-slate-400 font-bold mt-2">
                  Password: demo123 · Shops: {account.shops}
                </p>
              </button>
            ))}
          </div>

          <div className="mt-8 rounded-2xl border border-cyan-900 bg-cyan-950/20 p-6">
            <h3 className="text-xl font-black">New user?</h3>
            <p className="text-slate-400 mt-2">
              Create a real shop workspace through onboarding, then come back and log in using that email and password.
            </p>
            <button
              onClick={() => navigate("/onboarding")}
              className="mt-5 rounded-xl border border-cyan-400 px-5 py-3 font-bold text-cyan-200"
            >
              Create Account →
            </button>
          </div>
        </div>
      </div>

      <div className="mx-auto mt-8 flex max-w-7xl flex-wrap justify-center gap-5 text-sm font-bold text-slate-500">
        <Link to="/privacy" className="hover:text-cyan-200">Privacy</Link>
        <Link to="/terms" className="hover:text-cyan-200">Terms</Link>
        <Link to="/support" className="hover:text-cyan-200">Support</Link>
      </div>
    </div>
  );
}
