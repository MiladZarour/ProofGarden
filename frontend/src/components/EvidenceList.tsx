import { File, Fingerprint } from "lucide-react";

import type { EvidenceItem } from "../types";

interface EvidenceListProps {
  items: EvidenceItem[];
}

function formatBytes(bytes: number) {
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}

export default function EvidenceList({ items }: EvidenceListProps) {
  if (items.length === 0) {
    return <div className="rounded-md border border-dashed border-garden-line p-6 text-sm text-slate-400">No evidence uploaded yet.</div>;
  }

  return (
    <div className="space-y-3">
      {items.map((item) => {
        const width = item.metadata_json.width as number | undefined;
        const height = item.metadata_json.height as number | undefined;
        return (
          <div key={item.id} className="rounded-md border border-garden-line bg-garden-panelSoft/70 p-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex min-w-0 gap-3">
                <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-garden-ink text-garden-cyan">
                  <File size={18} aria-hidden="true" />
                </span>
                <div className="min-w-0">
                  <p className="truncate font-medium text-white">{item.file_name}</p>
                  <p className="mt-1 text-xs text-slate-400">
                    {item.content_type} · {formatBytes(item.file_size)}
                    {width && height ? ` · ${width}x${height}` : ""}
                  </p>
                </div>
              </div>
              <span className="rounded-md border border-garden-line px-2 py-1 text-xs text-slate-300">
                {new Date(item.uploaded_at).toLocaleDateString()}
              </span>
            </div>
            <p className="mt-3 flex min-w-0 items-center gap-2 text-xs text-slate-500">
              <Fingerprint size={14} aria-hidden="true" />
              <span className="truncate">{item.sha256}</span>
            </p>
          </div>
        );
      })}
    </div>
  );
}

