import { Outlet } from "react-router-dom";
import AppSidebar from "./AppSidebar";

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="flex min-h-screen">
        <aside className="w-72 shrink-0 border-r border-slate-800">
          <AppSidebar />
        </aside>

        <main className="flex-1 bg-[radial-gradient(circle_at_top_left,#0f2742_0%,#020617_38%,#020617_100%)]">
          <div className="mx-auto max-w-7xl p-6 md:p-10">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
