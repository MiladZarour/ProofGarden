# ProofGarden Frontend

React, Vite, TypeScript, and TailwindCSS interface for ProofGarden.

## Setup

### Windows PowerShell

```powershell
npm install
npm run dev
```

### Linux / macOS

```bash
npm install
npm run dev
```

The app expects the API at `http://localhost:8000`. To change it:

```text
VITE_API_URL=http://localhost:8000
```

## Scripts

```bash
npm run dev
npm run build
npm run test -- --run
```

## UI Structure

- `pages/Dashboard.tsx`: investigation list and empty state.
- `pages/NewInvestigation.tsx`: investigation creation form.
- `pages/InvestigationDetail.tsx`: evidence, notes, analysis, and report workspace.
- `components/`: reusable cards, upload, badges, and report preview.
