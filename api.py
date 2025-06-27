'''src/traffic_monitor/api.py

FastAPI backend for GitHub Traffic Monitor React UI.
Hardened: API key, CORS, rate limiting, audit logging, HTTPS enforced.
'''
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from pathlib import Path
import os
import json
from datetime import datetime
from traffic_monitor.fetcher import GitHubFetcher
from traffic_monitor.config import load_config
from traffic_monitor.security import apply_security, get_api_key
from traffic_monitor.security_hardening import (
    setup_rate_limiting, enforce_https, limiter, log_admin_action
)

HISTORY_FILE = os.getenv("TRAFFIC_HISTORY", "traffic_history.json")
CONFIG_FILE = os.getenv("TRAFFIC_CONFIG", "config.yml")

app = FastAPI(title="GitHub Traffic Monitor API")
app = apply_security(app)
app = setup_rate_limiting(app)
if os.getenv("ENFORCE_HTTPS", "0") == "1":
    app = enforce_https(app)

class TrafficStat(BaseModel):
    name: str
    views_count: int
    views_uniques: int
    clones_count: int
    clones_uniques: int
    timestamp: str

# --- Persistence utils ---
def load_history():
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

# --- API endpoints ---
@app.get("/api/traffic", response_model=dict, dependencies=[Depends(get_api_key)])
@limiter.limit("30/minute")
def get_traffic(request: Request):
    log_admin_action(request, action="get_traffic", extra={})
    hist = load_history()
    return {"history": hist}

@app.post("/api/refresh", response_model=dict, dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
def refresh_traffic(request: Request):
    log_admin_action(request, action="refresh_traffic", extra={})
    cfg = load_config(CONFIG_FILE)
    fetcher = GitHubFetcher(token=cfg.token, org=cfg.organization)
    stats = fetcher.fetch_all()
    now = datetime.utcnow().isoformat()
    for s in stats:
        s['timestamp'] = now
    # Append to history
    history = load_history()
    history.extend(stats)
    save_history(history)
    return {"added": len(stats), "history_len": len(history)}

@app.get("/api/health", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
def health(request: Request):
    log_admin_action(request, action="health_check", extra={})
    return {"status": "ok"}
