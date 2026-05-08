# Architecture

ProofGarden is split into a FastAPI backend and a React frontend.

## Backend

- `app/main.py` creates the FastAPI app, CORS rules, routers, startup database initialization, and static upload serving.
- `app/database.py` configures SQLAlchemy and SQLite.
- `app/models.py` defines investigations, evidence items, and evidence notes.
- `app/schemas.py` defines Pydantic validation and response models.
- `app/crud.py` keeps persistence operations separate from route handlers.
- `app/analysis/` contains transparent, non-AI analysis modules.
- `app/utils/report_markdown.py` generates Markdown reports.

## Frontend

- `src/App.tsx` defines the route tree.
- `src/api/client.ts` wraps HTTP calls to the backend.
- `src/pages/` contains dashboard, creation, and detail views.
- `src/components/` contains reusable UI pieces for evidence, reports, cards, and badges.

## Data Model

An investigation has many evidence items and many evidence notes. Analysis findings and risk score reasons are stored as JSON so reports can reproduce the reasoning visible at the time analysis was run.

## Uploads

Files are stored locally in `backend/uploads/`. Metadata and hashes are stored in SQLite. Uploaded files are not exposed through a public object store in the MVP.

## Analysis Flow

1. Investigator creates an investigation.
2. Investigator uploads evidence and adds notes.
3. Backend runs text and image metadata checks.
4. Risk score is calculated from source availability, findings, and notes.
5. Findings and score reasons are stored on the investigation.
6. Report endpoint renders a Markdown snapshot.

