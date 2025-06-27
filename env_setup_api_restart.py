'''src/traffic_monitor/env_api.py

Extends env_api with:
- Server restart support (supervisor/systemd or process self-termination)
- Admin-only route protection using setup token
'''
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from pathlib import Path
import signal
import sys
import subprocess

SETUP_TOKEN = os.getenv("TRAFFIC_SETUP_TOKEN")
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", ".env")
RESTART_MODE = os.getenv("RESTART_MODE", "auto")  # auto, supervisor, systemd, killself, none

class EnvVar(BaseModel):
    name: str
    value: str

class EnvPayload(BaseModel):
    token: str
    env_vars: list[EnvVar]
    restart: bool = False

app = FastAPI(title="Traffic Monitor Env API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

def require_setup_token(payload: EnvPayload):
    if SETUP_TOKEN is None or payload.token != SETUP_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing setup token"
        )
    return True

def restart_server():
    mode = RESTART_MODE.lower()
    if mode == "none":
        return False
    if mode == "supervisor":
        # Supervisor managed
        try:
            subprocess.run(["supervisorctl", "restart", os.getenv("SUPERVISOR_PROGRAM", "traffic-api")], check=True)
            return True
        except Exception:
            return False
    if mode == "systemd":
        try:
            subprocess.run(["systemctl", "restart", os.getenv("SYSTEMD_UNIT", "traffic-api.service")], check=True)
            return True
        except Exception:
            return False
    if mode == "killself" or mode == "auto":
        os.kill(os.getpid(), signal.SIGTERM)
        return True
    return False

@app.post("/api/setup/env")
def write_env(payload: EnvPayload):
    require_setup_token(payload)
    # Write .env file
    lines = [f"{item.name}={item.value!r}" for item in payload.env_vars]
    try:
        with open(ENV_FILE_PATH, "w") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Write failed: {e}")
    restarted = False
    if payload.restart:
        restarted = restart_server()
    return {"success": True, "path": ENV_FILE_PATH, "restarted": restarted}
