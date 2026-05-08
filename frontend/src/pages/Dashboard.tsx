import { RefreshCw, SearchX } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { api } from "../api/client";
import InvestigationCard from "../components/InvestigationCard";
import type { Investigation } from "../types";

export default function Dashboard() {
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadInvestigations() {
    setIsLoading(true);
    setError(null);
    try {
      setInvestigations(await api.listInvestigations());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load investigations");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadInvestigations();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-garden-cyan">Evidence workspace</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-normal text-white">Investigations</h1>
        </div>
        <button type="button" className="icon-button" onClick={() => void loadInvestigations()} title="Refresh investigations">
          <RefreshCw size={18} aria-hidden="true" />
        </button>
      </div>

      {error ? <div className="rounded-md border border-red-400/30 bg-red-400/10 p-4 text-sm text-red-100">{error}</div> : null}

      {isLoading ? (
        <div className="panel p-8 text-sm text-slate-300">Loading investigations...</div>
      ) : investigations.length === 0 ? (
        <div className="panel flex flex-col items-center px-6 py-16 text-center">
          <SearchX size={42} aria-hidden="true" className="text-garden-cyan" />
          <h2 className="mt-5 text-xl font-semibold text-white">No investigations yet</h2>
          <p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">Create the first record and start collecting evidence.</p>
          <Link
            to="/new"
            className="mt-6 rounded-md bg-garden-cyan px-4 py-2 text-sm font-semibold text-garden-ink transition hover:bg-cyan-300"
          >
            New Investigation
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {investigations.map((investigation) => (
            <InvestigationCard key={investigation.id} investigation={investigation} />
          ))}
        </div>
      )}
    </div>
  );
}

