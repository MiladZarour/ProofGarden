import { Copy, Download } from "lucide-react";
import { useMemo, useState } from "react";

interface ReportPreviewProps {
  markdown: string;
  filename: string;
}

export default function ReportPreview({ markdown, filename }: ReportPreviewProps) {
  const [copied, setCopied] = useState(false);
  const objectUrl = useMemo(() => {
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    return URL.createObjectURL(blob);
  }, [markdown]);

  async function copyReport() {
    await navigator.clipboard.writeText(markdown);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <div className="panel overflow-hidden">
      <div className="flex items-center justify-between gap-3 border-b border-garden-line px-5 py-4">
        <h2 className="text-base font-semibold text-white">Markdown Report</h2>
        <div className="flex items-center gap-2">
          <button type="button" className="icon-button" onClick={() => void copyReport()} title="Copy Markdown report">
            <Copy size={17} aria-hidden="true" />
          </button>
          <a className="icon-button" href={objectUrl} download={filename} title="Download Markdown report">
            <Download size={17} aria-hidden="true" />
          </a>
        </div>
      </div>
      {copied ? <div className="border-b border-garden-line bg-garden-cyan/10 px-5 py-2 text-sm text-cyan-100">Copied to clipboard.</div> : null}
      <pre className="max-h-[34rem] overflow-auto whitespace-pre-wrap p-5 text-sm leading-6 text-slate-300">{markdown}</pre>
    </div>
  );
}

