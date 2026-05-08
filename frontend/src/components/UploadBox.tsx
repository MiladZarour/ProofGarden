import { UploadCloud } from "lucide-react";
import { useRef, useState } from "react";

interface UploadBoxProps {
  onUpload: (file: File) => Promise<void>;
}

export default function UploadBox({ onUpload }: UploadBoxProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleFile(file: File | undefined) {
    if (!file) return;
    setError(null);
    setIsUploading(true);
    try {
      await onUpload(file);
      if (inputRef.current) inputRef.current.value = "";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className="rounded-lg border border-dashed border-garden-line bg-garden-panelSoft/50 p-5">
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".png,.jpg,.jpeg,.webp,.pdf,.txt,.eml"
        onChange={(event) => void handleFile(event.target.files?.[0])}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={isUploading}
        className="flex w-full items-center justify-center gap-3 rounded-md border border-garden-line bg-garden-panel px-4 py-6 text-sm font-semibold text-slate-100 transition hover:border-garden-cyan disabled:opacity-60"
      >
        <UploadCloud size={22} aria-hidden="true" className="text-garden-cyan" />
        {isUploading ? "Uploading..." : "Upload Evidence"}
      </button>
      {error ? <p className="mt-3 text-sm text-red-300">{error}</p> : null}
    </div>
  );
}

