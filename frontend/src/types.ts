export type Category =
  | "Screenshot"
  | "Image"
  | "Email"
  | "Social media post"
  | "Document"
  | "Scam message"
  | "Delivery/customer support claim"
  | "Public claim"
  | "Other";

export type InvestigationStatus =
  | "Unverified"
  | "Likely real"
  | "Likely edited"
  | "Likely AI-generated"
  | "Likely scam"
  | "Needs more evidence"
  | "Debunked";

export type NoteType =
  | "Metadata clue"
  | "Text clue"
  | "Source mismatch"
  | "Timestamp mismatch"
  | "Known scam pattern"
  | "Visual inconsistency"
  | "User testimony"
  | "External reference"
  | "Other";

export type Confidence = "Low" | "Medium" | "High";

export interface AnalysisFinding {
  module: string;
  title: string;
  severity: string;
  explanation: string;
  evidence_id?: number | null;
  score_delta: number;
  details: Record<string, unknown>;
}

export interface EvidenceItem {
  id: number;
  investigation_id: number;
  file_name: string;
  stored_name: string;
  content_type: string;
  file_size: number;
  sha256: string;
  metadata_json: Record<string, unknown>;
  analysis_findings: AnalysisFinding[];
  uploaded_at: string;
}

export interface EvidenceNote {
  id: number;
  investigation_id: number;
  title: string;
  type: NoteType | string;
  confidence: Confidence | string;
  explanation: string;
  source?: string | null;
  created_at: string;
}

export interface Investigation {
  id: number;
  title: string;
  claim: string;
  category: Category | string;
  source_url?: string | null;
  description?: string | null;
  status: InvestigationStatus | string;
  risk_score: number;
  risk_label: string;
  risk_reasons: Array<Record<string, unknown>>;
  analysis_findings: AnalysisFinding[];
  created_at: string;
  updated_at: string;
  evidence_items: EvidenceItem[];
  notes: EvidenceNote[];
}

export interface InvestigationCreate {
  title: string;
  claim: string;
  category: Category;
  source_url?: string | null;
  description?: string | null;
  status: InvestigationStatus;
}

export interface NoteCreate {
  title: string;
  type: NoteType;
  confidence: Confidence;
  explanation: string;
  source?: string | null;
}

export interface AnalyzeResponse {
  investigation: Investigation;
  findings: AnalysisFinding[];
  risk: {
    score: number;
    label: string;
    reasons: Array<Record<string, unknown>>;
  };
}

export const categories: Category[] = [
  "Screenshot",
  "Image",
  "Email",
  "Social media post",
  "Document",
  "Scam message",
  "Delivery/customer support claim",
  "Public claim",
  "Other",
];

export const statuses: InvestigationStatus[] = [
  "Unverified",
  "Likely real",
  "Likely edited",
  "Likely AI-generated",
  "Likely scam",
  "Needs more evidence",
  "Debunked",
];

export const noteTypes: NoteType[] = [
  "Metadata clue",
  "Text clue",
  "Source mismatch",
  "Timestamp mismatch",
  "Known scam pattern",
  "Visual inconsistency",
  "User testimony",
  "External reference",
  "Other",
];

