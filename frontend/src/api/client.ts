import type { AnalyzeResponse, EvidenceItem, EvidenceNote, Investigation, InvestigationCreate, NoteCreate } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Request failed with ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const api = {
  listInvestigations: () => request<Investigation[]>("/api/investigations"),
  createInvestigation: (payload: InvestigationCreate) =>
    request<Investigation>("/api/investigations", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getInvestigation: (id: number) => request<Investigation>(`/api/investigations/${id}`),
  updateInvestigation: (id: number, payload: Partial<InvestigationCreate>) =>
    request<Investigation>(`/api/investigations/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  uploadEvidence: async (id: number, file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${API_BASE}/api/investigations/${id}/upload`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error(await response.text());
    }
    return response.json() as Promise<EvidenceItem>;
  },
  listEvidence: (id: number) => request<EvidenceItem[]>(`/api/investigations/${id}/evidence`),
  createNote: (id: number, payload: NoteCreate) =>
    request<EvidenceNote>(`/api/investigations/${id}/notes`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listNotes: (id: number) => request<EvidenceNote[]>(`/api/investigations/${id}/notes`),
  deleteNote: (id: number) =>
    request<void>(`/api/notes/${id}`, {
      method: "DELETE",
    }),
  analyze: (id: number) =>
    request<AnalyzeResponse>(`/api/investigations/${id}/analyze`, {
      method: "POST",
    }),
  getReport: async (id: number) => {
    const response = await fetch(`${API_BASE}/api/investigations/${id}/report.md`);
    if (!response.ok) {
      throw new Error(await response.text());
    }
    return response.text();
  },
};

