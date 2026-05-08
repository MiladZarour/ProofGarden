# ProofGarden Backend

FastAPI backend for the ProofGarden evidence workspace.

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Development

```bash
pytest
```

The default database is `proofgarden.db`. Uploads are stored in `uploads/`. Override paths with:

```bash
PROOFGARDEN_DATABASE_URL=sqlite:///./custom.db
PROOFGARDEN_UPLOAD_DIR=./custom_uploads
```

## Modules

- `analysis/image_metadata.py`: reads safe image metadata and dimensions.
- `analysis/text_patterns.py`: finds suspicious non-AI text patterns.
- `analysis/risk_score.py`: calculates transparent risk scores.
- `utils/report_markdown.py`: generates exportable Markdown reports.

