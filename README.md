# AI Emotion Ring

AI Emotion Ring is an enterprise-oriented prototype for physiological-signal trend assessment and health-behavior intervention. It is not a medical diagnosis system.

## Repository layout

- `apps/admin-console`: Vue 3 + Vite administration console.
- `services/api-server`: Flask API service, authentication, and domain endpoints.
- `ml`: algorithm boundary, evaluation notes, and future model work.
- `firmware`: BLE protocol and embedded integration boundary.
- `data`: schemas, synthetic samples, and data-governance notes.
- `docs`: product and architecture documents.
- `scripts`: local API and LAN test helpers.

## Local development

Backend:

```powershell
cd services/api-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JWT_SECRET_KEY = "replace-with-a-long-random-development-secret"
python run.py
```

Admin console:

```powershell
cd apps/admin-console
npm install
npm run dev
```

The API defaults to `http://localhost:5000`; the Vite development server normally uses `http://localhost:5173`.

## Public repository safety

The public repository intentionally excludes signing keys, user data, runtime logs, dependency caches, and environment files. Use `.env.example` as a starting point and replace every placeholder before running outside local development.

## Scope and limitations

The current codebase is an MVP foundation. It does not claim clinical accuracy, medical diagnosis, or production readiness. Real hardware integration, privacy review, model validation, deployment hardening, and compliance work remain separate deliverables.
