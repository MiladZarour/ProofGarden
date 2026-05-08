import { ArrowLeft, Save } from "lucide-react";
import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { api } from "../api/client";
import { categories, statuses, type Category, type InvestigationStatus } from "../types";

export default function NewInvestigation() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [claim, setClaim] = useState("");
  const [category, setCategory] = useState<Category>("Scam message");
  const [sourceUrl, setSourceUrl] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<InvestigationStatus>("Unverified");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      const created = await api.createInvestigation({
        title,
        claim,
        category,
        source_url: sourceUrl.trim() || null,
        description: description.trim() || null,
        status,
      });
      navigate(`/investigations/${created.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create investigation");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <Link to="/" className="inline-flex items-center gap-2 text-sm text-slate-300 transition hover:text-white">
        <ArrowLeft size={16} aria-hidden="true" />
        Dashboard
      </Link>
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-garden-cyan">New record</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-normal text-white">Create Investigation</h1>
      </div>

      <form onSubmit={(event) => void handleSubmit(event)} className="panel space-y-5 p-6">
        {error ? <div className="rounded-md border border-red-400/30 bg-red-400/10 p-3 text-sm text-red-100">{error}</div> : null}

        <label className="block space-y-2">
          <span className="field-label">Title</span>
          <input className="field-input" value={title} onChange={(event) => setTitle(event.target.value)} required />
        </label>

        <label className="block space-y-2">
          <span className="field-label">Claim Being Checked</span>
          <textarea className="field-input min-h-28 resize-y" value={claim} onChange={(event) => setClaim(event.target.value)} required />
        </label>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block space-y-2">
            <span className="field-label">Category</span>
            <select className="field-input" value={category} onChange={(event) => setCategory(event.target.value as Category)}>
              {categories.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>

          <label className="block space-y-2">
            <span className="field-label">Status</span>
            <select className="field-input" value={status} onChange={(event) => setStatus(event.target.value as InvestigationStatus)}>
              {statuses.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label className="block space-y-2">
          <span className="field-label">Source URL</span>
          <input className="field-input" value={sourceUrl} onChange={(event) => setSourceUrl(event.target.value)} type="url" />
        </label>

        <label className="block space-y-2">
          <span className="field-label">Description / Context</span>
          <textarea className="field-input min-h-32 resize-y" value={description} onChange={(event) => setDescription(event.target.value)} />
        </label>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="inline-flex items-center gap-2 rounded-md bg-garden-cyan px-4 py-2 text-sm font-semibold text-garden-ink transition hover:bg-cyan-300 disabled:opacity-60"
          >
            <Save size={16} aria-hidden="true" />
            {isSubmitting ? "Creating..." : "Create"}
          </button>
        </div>
      </form>
    </div>
  );
}

