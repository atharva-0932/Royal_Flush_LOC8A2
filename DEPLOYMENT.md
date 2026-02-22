# Deployment Guide (Frontend -> Vercel, Backend -> Render)

This file documents the exact steps to deploy the Frontend (Vite) to Vercel and the Backend (FastAPI) to Render, plus recommended environment variables and quick verification commands.

Frontend (Vercel)
1. In Vercel, create a new project and import this GitHub repository.
2. During import set:
   - Root Directory: `Frontend`
   - Install Command: `npm ci`
   - Build Command: `npm run build`
   - Output Directory: `dist`
3. Add Environment Variables (Vercel > Settings > Environment Variables):
   - `VITE_API_BASE_URL` = `https://<your-render-url>/api` (set to the Render backend URL)
   - Any other `VITE_` prefixed envs used by the app
4. Trigger a deployment (Vercel will build and publish).

Backend (Render)
1. In Render, create a new Web Service and connect to the same GitHub repo.
2. Use the branch you want to deploy.
3. Set the root build path and commands as needed. Since requirements are now exposed at the repo root, Render will detect Python.
4. Set the Start Command (Render service settings) to:
   - `bash -lc "cd Backend && uvicorn main:app --host 0.0.0.0 --port $PORT"`
   or set the `Procfile` to `Backend/Procfile` and point Render to run the web process.
5. Add Environment Variables under Render service settings (Secrets):
   - `GNEWS_API_KEY`, `DATABASE_URL`, etc. (whatever your backend needs)
6. Set the health check path to `/health`.

Local verification commands

Frontend:
```bash
cd Frontend
npm ci
npm run build
npm run preview
```

Backend:
```bash
cd Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
curl http://localhost:8000/health
```

Notes & caveats
- The backend's `requirements.txt` includes heavy packages (numpy, pandas, scikit-learn). Build time on Render may be long or may require prebuilt wheels. If build fails due to compilation, consider using Render's Docker service or a slimmer runtime for inference.
- For production security, replace CORS wildcard in `Backend/main.py` with your Vercel domain.
