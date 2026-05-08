# Contributing to ProofGarden

Thanks for helping grow ProofGarden. This project aims to be useful, careful, and welcoming to contributors from engineering, journalism, security, research, and civic tech communities.

## Development Setup

Run the backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

On Windows PowerShell, activate the backend environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Contribution Guidelines

- Keep analysis modules transparent and explainable.
- Avoid claims that an item is definitely fake or real unless the evidence supports it.
- Add tests for backend logic and frontend components when behavior changes.
- Keep file uploads private by default.
- Document new APIs, configuration, and analysis module behavior.
- Prefer small pull requests with clear scope.

## Backend Checks

```bash
pytest
```

## Frontend Checks

```bash
cd frontend
npm run test -- --run
npm run build
```

## Docker Checks

Use Docker Compose when you want a clean Python and Node environment without installing dependencies directly on your machine:

```bash
docker compose -f docker-compose.test.yml run --rm backend-tests
docker compose -f docker-compose.test.yml run --rm frontend-tests
```

## Analysis Module Standards

Good modules should:

- Return structured findings.
- Explain what was detected and what it does not prove.
- Include score deltas only when the signal is meaningful.
- Avoid black-box judgments.
- Include tests with realistic fake examples.

## Pull Request Notes

Please include:

- What changed
- Why it changed
- How you tested it
- Any privacy or safety considerations
