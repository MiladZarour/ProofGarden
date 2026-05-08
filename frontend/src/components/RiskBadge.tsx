interface RiskBadgeProps {
  score: number;
  label: string;
}

const styles: Record<string, string> = {
  Low: "border-emerald-400/40 bg-emerald-400/12 text-emerald-200",
  Medium: "border-yellow-400/40 bg-yellow-400/12 text-yellow-100",
  High: "border-orange-400/40 bg-orange-400/12 text-orange-100",
  Critical: "border-red-400/40 bg-red-400/12 text-red-100",
};

export default function RiskBadge({ score, label }: RiskBadgeProps) {
  return (
    <span className={`inline-flex items-center gap-2 rounded-md border px-2.5 py-1 text-xs font-semibold ${styles[label] ?? styles.Low}`}>
      <span>{label}</span>
      <span className="text-slate-300">{score}/100</span>
    </span>
  );
}

