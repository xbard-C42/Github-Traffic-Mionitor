'''src/traffic_monitor/api.py

FastAPI backend for GitHub Traffic Monitor React UI.
Hardened: API key, CORS, rate limiting, audit logging, HTTPS enforced.
Includes AI analysis endpoint using Google Gemini API.
'''
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from pathlib import Path
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any
from traffic_monitor.fetcher import GitHubFetcher
from traffic_monitor.config import load_config
from traffic_monitor.security import apply_security, get_api_key
from traffic_monitor.security_hardening import (
    setup_rate_limiting, enforce_https, limiter, log_admin_action
)

HISTORY_FILE = os.getenv("TRAFFIC_HISTORY", "traffic_history.json")
CONFIG_FILE = os.getenv("TRAFFIC_CONFIG", "config.yml")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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

class AnalyzeRequest(BaseModel):
    repoName: str
    repoHistory: List[Dict[str, Any]]

# --- Persistence utils ---
def load_history():
    if Path(HISTORY_FILE).exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def generate_ai_analysis(repo_name: str, repo_history: List[Dict[str, Any]]) -> str:
    """
    Generate AI analysis using Google Gemini API.
    Keeps API key secure on server-side.
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Gemini API key not configured on server"
        )
    
    if len(repo_history) < 2:
        return "Insufficient data for analysis. Need at least 2 data points to identify trends."
    
    # Prepare data summary for AI
    latest = repo_history[-1]
    previous = repo_history[-2] if len(repo_history) > 1 else repo_history[-1]
    oldest = repo_history[0]
    
    # Calculate trends
    views_trend = latest['views_count'] - previous['views_count']
    clones_trend = latest['clones_count'] - previous['clones_count']
    total_snapshots = len(repo_history)
    time_span = f"from {oldest['timestamp'][:10]} to {latest['timestamp'][:10]}"
    
    prompt = f"""Analyze the GitHub repository traffic data for '{repo_name}' and provide insights.

Repository: {repo_name}
Time period: {time_span}
Total snapshots: {total_snapshots}

Latest metrics:
- Views: {latest['views_count']} (unique: {latest['views_uniques']})
- Clones: {latest['clones_count']} (unique: {latest['clones_uniques']})

Recent trend (vs previous snapshot):
- Views change: {views_trend:+d}
- Clones change: {clones_trend:+d}

Historical data points: {len(repo_history)} snapshots

Please provide a concise analysis (2-3 paragraphs) covering:
1. Overall traffic trends and patterns
2. Notable changes or anomalies
3. Actionable insights for the repository owner

Keep the tone professional but accessible."""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 500,
            }
        }
        
        response = requests.post(
            url, 
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini API error: {response.status_code}"
            )
        
        data = response.json()
        
        if 'candidates' in data and len(data['candidates']) > 0:
            content = data['candidates'][0].get('content', {})
            parts = content.get('parts', [])
            if parts and 'text' in parts[0]:
                return parts[0]['text'].strip()
        
        return "Analysis could not be generated. Please try again later."
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Gemini API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis generation failed: {str(e)}"
        )

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

@app.post("/api/analyze", dependencies=[Depends(get_api_key)])
@limiter.limit("5/minute")
def analyze_traffic(request: Request, payload: AnalyzeRequest):
    """
    Generate AI-powered analysis of repository traffic trends.
    Uses Google Gemini API with server-side API key for security.
    """
    log_admin_action(
        request, 
        action="ai_analysis", 
        extra={"repo": payload.repoName, "data_points": len(payload.repoHistory)}
    )
    
    try:
        analysis = generate_ai_analysis(payload.repoName, payload.repoHistory)
        return {"analysis": analysis}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/api/health", dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute")
def health(request: Request):
    log_admin_action(request, action="health_check", extra={})
    
    # Check if Gemini API key is configured
    gemini_status = "configured" if GEMINI_API_KEY else "not_configured"
    
    return {
        "status": "ok",
        "gemini_api": gemini_status,
        "timestamp": datetime.utcnow().isoformat()
    }
