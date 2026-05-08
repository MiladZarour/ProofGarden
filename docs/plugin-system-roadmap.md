# Plugin System Roadmap

ProofGarden should become a platform for transparent verification modules. The MVP keeps modules in the backend codebase, but future versions can support installable plugins.

## Candidate Modules

- Email header analyzer
- PDF tampering checker
- Browser extension capture workflow
- Reverse image search integration
- OCR module
- AI-generated image artifact module
- Scam database integration
- Source reputation module
- Timeline builder
- Multilingual report templates

## Plugin Principles

- Plugins must describe what data they read.
- Plugins must disclose network calls.
- Plugins must return structured findings.
- Plugins must explain uncertainty and false positives.
- Plugins must include tests and example fixtures.
- Plugins should be disabled by default if they contact external services.

## Possible Interface

Future plugins may expose:

- Metadata schema
- Required permissions
- Input file types
- Analysis function
- Score contribution policy
- Report rendering section

