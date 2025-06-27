# GitHub Traffic Monitor

A modern, secure Python + React application for monitoring traffic (views, clones) across all your GitHub repositories. Features real-time metrics, historical trend analysis, and robust security—deployable via Docker or natively.

---

## Features

- **Auto-fetch traffic stats** from all repos (user or organisation) via GitHub API
- **FastAPI backend** with strict API key security, CORS, and optional setup admin interface
- **React dashboard** for live trends, metrics, percent change, and historical charts
- **One-click .env setup** (admin only, restart support)
- **Fully containerised** (multi-stage Dockerfile: backend + frontend)

---

## Quickstart

### 1. Clone and configure

```sh
git clone ...
cd github-traffic-monitor
```

### 2. (Option A) Use the React Setup Panel

1. Start backend: `uvicorn src.traffic_monitor.api:app --reload`
2. Go to `/setup` route in your frontend (or wherever you mount `EnvSetupGuarded`)
3. Enter the setup token (server admin supplies; set as `TRAFFIC_SETUP_TOKEN`)
4. Enter all required variables and click “Write to Server” (optionally, trigger restart)
5. Your `.env` is now on the server—restart if needed

### 3. (Option B) Manual setup

- Copy `.env.example` to `.env` and fill values:
  - `TRAFFIC_API_KEY` (backend secret, required for all API access)
  - `TRAFFIC_CORS_ORIGINS` (comma-separated allowed frontend URLs)
  - `GITHUB_TOKEN` (personal token for repo stats)
  - ... (see config)
- Restart server

### 4. Deploy (Docker)

```sh
docker build -t github-traffic-monitor .
docker run -p 8000:8000 --env-file .env github-traffic-monitor
```

---

## Security & Admin

- All traffic endpoints are API-key protected (set `TRAFFIC_API_KEY` in `.env` or as an environment variable)
- CORS is restricted to allowed origins (configure `TRAFFIC_CORS_ORIGINS`)
- The `/api/setup/env` endpoint and setup panel are admin-only (require `TRAFFIC_SETUP_TOKEN`)
- For production, block/remove admin setup UI/routes after initial configuration
- Supports automatic restart after setup (configurable: supervisor, systemd, self-terminate, or none)

---

## Frontend

- React + Tailwind + Recharts
- Secure admin setup UI (`EnvSetupGuarded`)
- Real-time metrics, history, percent delta, and line charts
- Customise API URL with `REACT_APP_TRAFFIC_API_URL`

---

## Advanced: Production Hardening

- Remove or rotate `TRAFFIC_SETUP_TOKEN` after use
- Use a strong random `TRAFFIC_API_KEY` (rotate regularly)
- Place the setup panel behind VPN, firewall, or admin login in production
- Use Docker secrets or environment injection for sensitive values
- Enable audit logging in the backend if needed
- Optionally add rate limiting middleware (see FastAPI extensions)

---

## License

MIT

