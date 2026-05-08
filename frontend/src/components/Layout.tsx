import { Leaf, Plus } from "lucide-react";
import { Link, NavLink } from "react-router-dom";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen text-slate-100">
      <header className="border-b border-garden-line/80 bg-garden-ink/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex min-w-0 items-center gap-3">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-garden-cyan/40 bg-garden-panelSoft text-garden-cyan">
              <Leaf size={22} aria-hidden="true" />
            </span>
            <span className="min-w-0">
              <span className="block text-lg font-semibold tracking-normal text-white">ProofGarden</span>
              <span className="block truncate text-xs text-slate-400">Grow proof, not rumors.</span>
            </span>
          </Link>
          <nav className="flex items-center gap-2">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `rounded-md px-3 py-2 text-sm font-medium transition ${
                  isActive ? "bg-garden-panelSoft text-white" : "text-slate-300 hover:bg-garden-panelSoft hover:text-white"
                }`
              }
            >
              Dashboard
            </NavLink>
            <Link
              to="/new"
              className="inline-flex items-center gap-2 rounded-md bg-garden-cyan px-3 py-2 text-sm font-semibold text-garden-ink transition hover:bg-cyan-300"
            >
              <Plus size={16} aria-hidden="true" />
              New Investigation
            </Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
    </div>
  );
}
