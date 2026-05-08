import { CalendarDays, FileText } from "lucide-react";
import { Link } from "react-router-dom";

import type { Investigation } from "../types";
import RiskBadge from "./RiskBadge";

interface InvestigationCardProps {
  investigation: Investigation;
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(new Date(value));
}

export default function InvestigationCard({ investigation }: InvestigationCardProps) {
  return (
    <Link
      to={`/investigations/${investigation.id}`}
      className="panel block p-5 transition hover:-translate-y-0.5 hover:border-garden-cyan/70"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-garden-cyan">{investigation.category}</p>
          <h2 className="mt-2 line-clamp-2 text-lg font-semibold text-white">{investigation.title}</h2>
        </div>
        <RiskBadge score={investigation.risk_score} label={investigation.risk_label} />
      </div>
      <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-300">{investigation.claim}</p>
      <div className="mt-5 flex flex-wrap items-center gap-3 text-xs text-slate-400">
        <span className="rounded-md border border-garden-line bg-garden-panelSoft px-2 py-1">{investigation.status}</span>
        <span className="inline-flex items-center gap-1.5">
          <CalendarDays size={14} aria-hidden="true" />
          {formatDate(investigation.created_at)}
        </span>
        <span className="inline-flex items-center gap-1.5">
          <FileText size={14} aria-hidden="true" />
          {investigation.evidence_items.length} evidence
        </span>
      </div>
    </Link>
  );
}

