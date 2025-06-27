'''src/traffic_monitor/security.py

Security primitives for API hardening: API key auth, secret management, CORS tightening.
'''
import os
from fastapi import Depends, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.cors import CORSMiddleware

API_KEY_NAME = os.getenv('TRAFFIC_API_KEY_NAME', 'x-api-key')
API_KEY_VALUE = os.getenv('TRAFFIC_API_KEY')
ALLOWED_ORIGINS = os.getenv('TRAFFIC_CORS_ORIGINS', 'http://localhost:3000').split(',')

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(request: Request, api_key_header: str = Depends(api_key_header)):
    if API_KEY_VALUE is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured on server."
        )
    key = api_key_header or request.headers.get(API_KEY_NAME)
    if key == API_KEY_VALUE:
        return key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key.",
        headers={"WWW-Authenticate": "API Key"},
    )

def apply_security(app):
    # Strict CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=[API_KEY_NAME, "Content-Type", "Authorization"],
    )
    return app
