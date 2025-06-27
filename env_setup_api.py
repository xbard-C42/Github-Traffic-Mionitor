'''src/traffic_monitor/env_api.py

FastAPI endpoint to write a .env file from POSTed form data (admin/setup use only).
Hardened: Requires a special "setup token" (env: TRAFFIC_SETUP_TOKEN).
'''
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from pathlib import Path

SETUP_TOKEN = os.getenv("TRAFFIC_SETUP_TOKEN")
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", ".env")

class EnvVar(BaseModel):
    name: str
    value: str

class EnvPayload(BaseModel):
    token: str
    env_vars: list[EnvVar]

app = FastAPI(title="Traffic Monitor Env API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

@app.post("/api/setup/env")
def write_env(payload: EnvPayload):
    if SETUP_TOKEN is None or payload.token != SETUP_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing setup token"
        )
    # Write .env file
    lines = [f"{item.name}={item.value!r}" for item in payload.env_vars]
    try:
        with open(ENV_FILE_PATH, "w") as f:
            f.write("\n".join(lines) + "\n")
        return {"success": True, "path": ENV_FILE_PATH}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Write failed: {e}")
