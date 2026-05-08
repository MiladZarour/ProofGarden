import { ArrowLeft, PlayCircle, Save, Trash2 } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { api } from "../api/client";
import EvidenceList from "../components/EvidenceList";
import ReportPreview from "../components/ReportPreview";
import RiskBadge from "../components/RiskBadge";
import UploadBox from "../components/UploadBox";
import { noteTypes, statuses, type Confidence, type EvidenceNote, type Investigation, type InvestigationStatus, type NoteType } from "../types";

const confidences: Confidence[] = ["Low", "Medium", "High"];

export default function InvestigationDetail() {
  const { id } = useParams();
  const investigationId = Number(id);
  const [investigation, setInvestigation] = useState<Investigation | null>(null);
  const [report, setReport] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [noteTitle, setNoteTitle] = useState("");
  const [noteType, setNoteType] = useState<NoteType>("Text clue");
  const [confidence, setConfidence] = useState<Confidence>("Medium");
  const [explanation, setExplanation] = useState("");
  const [source, setSource] = useState("");

  async function loadInvestigation() {
    if (!Number.isFinite(investigationId)) return;
    setIsLoading(true);
    setError(null);
    try {
      const [loaded, markdown] = await Promise.all([api.getInvestigation(investigationId), api.getReport(investigationId)]);
      setInvestigation(loaded);
      setReport(markdown);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load investigation");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadInvestigation();
  }, [investigationId]);

  async function refreshReport(nextInvestigation?: Investigation) {
    const [loaded, markdown] = await Promise.all([Promise.resolve(nextInvestigation ?? api.getInvestigation(investigationId)), api.getReport(investigationId)]);
    setInvestigation(loaded);
    setReport(markdown);
  }

  async function handleUpload(file: File) {
    await api.uploadEvidence(investigationId, file);
    await refreshReport();
  }

  async function handleAnalyze() {
    setIsAnalyzing(true);
    setError(null);
    try {
      const response = await api.analyze(investigationId);
      await refreshReport(response.investigation);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  }

  async function handleStatusChange(status: InvestigationStatus) {
    const updated = await api.updateInvestigation(investigationId, { status });
    await refreshReport(updated);
  }

  async function handleNoteSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    try {
      await api.createNote(investigationId, {
        title: noteTitle,
        type: noteType,
        confidence,
        explanation,
        source: source.trim() || null,
      });
      setNoteTitle("");
      setExplanation("");
      setSource("");
      await refreshReport();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not add note");
    }
  }

  async function deleteNote(note: EvidenceNote) {
    await api.deleteNote(note.id);
    await refreshReport();
  }

  if (isLoading) {
    return <div className="panel p-8 text-sm text-slate-300">Loading investigation...</div>;
  }

  if (!investigation) {
    return <div className="rounded-md border border-red-400/30 bg-red-400/10 p-4 text-sm text-red-100">{error ?? "Investigation not found"}</div>;
  }

  return (
    <div className="space-y-6">
      <Link to="/" className="inline-flex items-center gap-2 text-sm text-slate-300 transition hover:text-white">
        <ArrowLeft size={16} aria-hidden="true" />
        Dashboard
      </Link>

      <section className="panel p-6">
        <div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-start">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-wide text-garden-cyan">{investigation.category}</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-normal text-white">{investigation.title}</h1>
            <p className="mt-4 text-base leading-7 text-slate-200">{investigation.claim}</p>
            {investigation.description ? <p className="mt-3 text-sm leading-6 text-slate-400">{investigation.description}</p> : null}
            {investigation.source_url ? (
              <a className="mt-4 inline-block text-sm text-garden-cyan hover:text-cyan-200" href={investigation.source_url} target="_blank" rel="noreferrer">
                {investigation.source_url}
              </a>
            ) : null}
          </div>
          <div className="flex shrink-0 flex-col gap-3 rounded-lg border border-garden-line bg-garden-panelSoft p-4">
            <RiskBadge score={investigation.risk_score} label={investigation.risk_label} />
            <label className="block space-y-2">
              <span className="field-label">Status</span>
              <select
                className="field-input min-w-56"
                value={investigation.status}
                onChange={(event) => void handleStatusChange(event.target.value as InvestigationStatus)}
              >
                {statuses.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </label>
            <button
              type="button"
              onClick={() => void handleAnalyze()}
              disabled={isAnalyzing}
              className="inline-flex items-center justify-center gap-2 rounded-md bg-garden-cyan px-4 py-2 text-sm font-semibold text-garden-ink transition hover:bg-cyan-300 disabled:opacity-60"
            >
              <PlayCircle size={17} aria-hidden="true" />
              {isAnalyzing ? "Analyzing..." : "Run Analysis"}
            </button>
          </div>
        </div>
      </section>

      {error ? <div className="rounded-md border border-red-400/30 bg-red-400/10 p-4 text-sm text-red-100">{error}</div> : null}

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_24rem]">
        <div className="space-y-6">
          <section className="panel p-5">
            <h2 className="text-base font-semibold text-white">Evidence</h2>
            <div className="mt-4">
              <UploadBox onUpload={handleUpload} />
            </div>
            <div className="mt-4">
              <EvidenceList items={investigation.evidence_items} />
            </div>
          </section>

          <section className="panel p-5">
            <h2 className="text-base font-semibold text-white">Analysis Findings</h2>
            <div className="mt-4 space-y-3">
              {investigation.analysis_findings.length === 0 ? (
                <div className="rounded-md border border-dashed border-garden-line p-5 text-sm text-slate-400">No findings recorded yet.</div>
              ) : (
                investigation.analysis_findings.map((finding, index) => (
                  <div key={`${finding.module}-${index}`} className="rounded-md border border-garden-line bg-garden-panelSoft/70 p-4">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <h3 className="font-medium text-white">{finding.title}</h3>
                      <span className="rounded-md border border-garden-line px-2 py-1 text-xs text-slate-300">
                        {finding.severity} · {finding.score_delta >= 0 ? "+" : ""}
                        {finding.score_delta}
                      </span>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-slate-400">{finding.explanation}</p>
                  </div>
                ))
              )}
            </div>
          </section>

          {report ? <ReportPreview markdown={report} filename={`proofgarden-investigation-${investigation.id}.md`} /> : null}
        </div>

        <aside className="space-y-6">
          <section className="panel p-5">
            <h2 className="text-base font-semibold text-white">Evidence Notes</h2>
            <form onSubmit={(event) => void handleNoteSubmit(event)} className="mt-4 space-y-4">
              <label className="block space-y-2">
                <span className="field-label">Title</span>
                <input className="field-input" value={noteTitle} onChange={(event) => setNoteTitle(event.target.value)} required />
              </label>
              <label className="block space-y-2">
                <span className="field-label">Type</span>
                <select className="field-input" value={noteType} onChange={(event) => setNoteType(event.target.value as NoteType)}>
                  {noteTypes.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block space-y-2">
                <span className="field-label">Confidence</span>
                <select className="field-input" value={confidence} onChange={(event) => setConfidence(event.target.value as Confidence)}>
                  {confidences.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block space-y-2">
                <span className="field-label">Explanation</span>
                <textarea className="field-input min-h-28 resize-y" value={explanation} onChange={(event) => setExplanation(event.target.value)} required />
              </label>
              <label className="block space-y-2">
                <span className="field-label">Source</span>
                <input className="field-input" value={source} onChange={(event) => setSource(event.target.value)} />
              </label>
              <button
                type="submit"
                className="inline-flex w-full items-center justify-center gap-2 rounded-md bg-garden-cyan px-4 py-2 text-sm font-semibold text-garden-ink transition hover:bg-cyan-300"
              >
                <Save size={16} aria-hidden="true" />
                Add Note
              </button>
            </form>
          </section>

          <section className="space-y-3">
            {investigation.notes.length === 0 ? (
              <div className="rounded-md border border-dashed border-garden-line p-5 text-sm text-slate-400">No evidence notes yet.</div>
            ) : (
              investigation.notes.map((note) => (
                <div key={note.id} className="rounded-lg border border-garden-line bg-garden-panel p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-medium text-white">{note.title}</h3>
                      <p className="mt-1 text-xs text-slate-400">
                        {note.type} · {note.confidence}
                      </p>
                    </div>
                    <button type="button" className="icon-button h-8 w-8" onClick={() => void deleteNote(note)} title="Delete evidence note">
                      <Trash2 size={15} aria-hidden="true" />
                    </button>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-slate-300">{note.explanation}</p>
                  {note.source ? <p className="mt-2 text-xs text-slate-500">{note.source}</p> : null}
                </div>
              ))
            )}
          </section>
        </aside>
      </div>
    </div>
  );
}

