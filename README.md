# ProofGarden

**Logo placeholder:** ProofGarden wordmark and leaf mark  
**Badges placeholder:** build status, license, contributors, first good issue

**Grow proof, not rumors.**

ProofGarden is an open-source evidence workspace for verifying screenshots, images, documents, suspicious posts, scam messages, emails, and online claims. It is not a simple "AI fake detector." It helps users collect evidence, analyze transparent signals, write structured notes, and export careful verification reports.

## What It Does

- Create investigation records for claims, posts, screenshots, messages, and documents.
- Upload PNG, JPG, JPEG, WEBP, PDF, TXT, and placeholder EML evidence files.
- Store file metadata locally in SQLite with a local uploads folder.
- Add structured evidence notes with type, confidence, source, and explanation.
- Run non-AI analysis modules for image metadata and suspicious text patterns.
- Calculate an explainable risk score with visible score reasons.
- Generate Markdown reports for sharing, review, or archival.

## Why It Exists

Online verification work is often scattered across screenshots, browser tabs, chat threads, notes, and assumptions. ProofGarden gives that work a structured home. The goal is to make uncertainty visible, keep evidence organized, and help contributors build transparent analysis modules that support careful human judgment.

## Screenshots

Placeholder screenshots:

- Dashboard investigation list
- Investigation detail workspace
- Markdown report preview

## MVP Features

- React, Vite, TypeScript, and TailwindCSS frontend
- FastAPI backend with SQLAlchemy and Pydantic
- SQLite database
- Local file uploads in `backend/uploads/`
- Investigation CRUD API
- Evidence upload and listing API
- Evidence note API
- Image metadata checker
- Text pattern checker
- Transparent risk scoring
- Markdown report endpoint
- Backend pytest suite
- Frontend Vitest setup
- GitHub Actions CI

## Example Use Cases

- Check whether a delivery SMS contains known scam pressure patterns.
- Preserve a screenshot and document what is known, unknown, and externally verified.
- Compare a public claim against a source URL and investigator notes.
- Export a Markdown report for a newsroom, moderation team, security team, or community fact-checking group.

## Quick Start: Backend

### Windows PowerShell

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will run at `http://localhost:8000`.

### Linux / macOS

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will run at `http://localhost:8000`.

## Quick Start: Frontend

### Windows PowerShell

```powershell
cd frontend
npm install
npm run dev
```

### Linux / macOS

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

If your backend runs somewhere else, create `frontend/.env.local`:

```text
VITE_API_URL=http://localhost:8000
```

## Tests

### Backend

```bash
pytest
```

### Frontend

```bash
cd frontend
npm run test -- --run
npm run build
```

### Docker

Run the full test suite in containers:

```bash
docker compose -f docker-compose.test.yml run --rm backend-tests
docker compose -f docker-compose.test.yml run --rm frontend-tests
```

Run one side at a time:

```bash
docker compose -f docker-compose.test.yml run --rm backend-tests
docker compose -f docker-compose.test.yml run --rm frontend-tests
```

Clean Docker test volumes when you want a fresh dependency install:

```bash
docker compose -f docker-compose.test.yml down --volumes
```

There is also a manual `Docker Tests` GitHub Action for running the same Compose checks in GitHub when needed.

## API Overview

- `GET /api/health`
- `GET /api/investigations`
- `POST /api/investigations`
- `GET /api/investigations/{id}`
- `PUT /api/investigations/{id}`
- `DELETE /api/investigations/{id}`
- `POST /api/investigations/{id}/upload`
- `GET /api/investigations/{id}/evidence`
- `POST /api/investigations/{id}/notes`
- `GET /api/investigations/{id}/notes`
- `DELETE /api/notes/{note_id}`
- `POST /api/investigations/{id}/analyze`
- `GET /api/investigations/{id}/report.md`

## Roadmap

- Email header analyzer
- PDF tampering checks
- OCR for screenshots and scanned documents
- Reverse image search integrations
- Browser extension for capture workflows
- Source reputation modules
- Scam pattern database
- Timeline builder
- Plugin API for community analysis modules
- Multilingual report templates

## Contributing

ProofGarden is designed to be contributor-friendly. Start with [CONTRIBUTING.md](CONTRIBUTING.md), read the [architecture notes](docs/architecture.md), and open an issue before large changes. Analysis modules should be transparent, cautious, and testable.

## Safety Disclaimer

ProofGarden does not prove absolute truth. It organizes evidence and surfaces transparent signals for human review. Do not use it for harassment, doxxing, defamation, or publishing private personal data. Reports should use careful language such as "likely", "unverified", and "needs more evidence."
