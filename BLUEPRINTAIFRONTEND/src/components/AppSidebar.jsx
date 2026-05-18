import { Link, useLocation, useNavigate } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/creative-library", label: "Creative Library" },
  { to: "/upload", label: "Video Analysis" },
  { to: "/ad-briefs", label: "Ad Briefs" },
  { to: "/recommendations", label: "Recommendations" },
  { to: "/revenue-blueprint", label: "Blueprint Creation" },
  { to: "/creators", label: "Creators" },
  { to: "/activity-log", label: "Activity Log" },
  { to: "/settings", label: "Settings" },
];

export default function AppSidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");

    navigate("/login");
  }

  return (
    <div className="h-full bg-slate-950 text-white flex flex-col">
      <div className="px-6 py-6 border-b border-slate-800">
        <Link to="/dashboard" className="text-2xl font-bold tracking-tight">
          BlueprintAI
        </Link>
        <p className="text-sm text-white mt-1">
          Creative intelligence for TikTok Shop
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {links.map((link) => {
          const active =
            location.pathname === link.to ||
            location.pathname.startsWith(`${link.to}/`);

          return (
            <Link
              key={link.to}
              to={link.to}
              className={`block rounded-xl px-4 py-3 text-sm transition ${
                active
                  ? "bg-slate-800 text-white font-semibold"
                  : "text-white hover:bg-slate-900 hover:text-white"
              }`}
            >
              {link.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button
          onClick={handleLogout}
          className="w-full rounded-xl px-4 py-3 text-sm text-left text-red-300 hover:bg-red-950 hover:text-red-100 transition"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
