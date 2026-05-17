export function SidebarProvider({ children }) {
  return <div className="min-h-screen">{children}</div>;
}

export function Sidebar({ children, className = "" }) {
  return <aside className={`border-r bg-white ${className}`}>{children}</aside>;
}

export function SidebarHeader({ children, className = "" }) {
  return <div className={`p-4 border-b ${className}`}>{children}</div>;
}

export function SidebarContent({ children, className = "" }) {
  return <div className={`p-4 space-y-2 ${className}`}>{children}</div>;
}

export function SidebarInset({ children, className = "" }) {
  return <main className={`flex-1 p-6 ${className}`}>{children}</main>;
}

export function SidebarTrigger({ children = "Menu", className = "", ...props }) {
  return (
    <button className={`border rounded-xl px-3 py-2 ${className}`} {...props}>
      {children}
    </button>
  );
}
