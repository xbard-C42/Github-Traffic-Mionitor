'''src/traffic_monitor/api.py

FastAPI backend for GitHub Traffic Monitor React UI.
Exposes traffic stats, history, and on-demand refresh.
'''
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
import json
from datetime import datetime
from traffic_monitor.fetcher import GitHubFetcher
from traffic_monitor.config import load_config

HISTORY_FILE = os.getenv("TRAFFIC_HISTORY", "traffic_history.json")
CONFIG_FILE = os.getenv("TRAFFIC_CONFIG", "config.yml")

app = FastAPI(title="GitHub Traffic Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.get("/api/traffic", response_model=dict)
def get_traffic():
    """
    Returns { history: [TrafficStat, ...] }
    """
    hist = load_history()
    return {"history": hist}

@app.post("/api/refresh", response_model=dict)
def refresh_traffic():
    """
    Fetches new stats and appends to history. Returns new snapshot.
    """
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

@app.get("/api/health")
def health():
    return {"status": "ok"}
