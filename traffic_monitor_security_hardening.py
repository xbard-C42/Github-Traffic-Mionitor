'''src/traffic_monitor/security_hardening.py

Includes:
- Rate limiting middleware (slowapi)
- Admin/audit logging with timestamp and IP
- Enforced HTTPS redirect middleware
'''
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi import Request as FastAPIRequest
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from datetime import datetime

# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])  # change as needed

def setup_rate_limiting(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    return app

# Usage: @limiter.limit("5/minute") on critical routes

# --- Admin/Audit Logging ---
aud_logger = logging.getLogger("admin_audit")
aud_logger.setLevel(logging.INFO)
fh = logging.FileHandler("admin_audit.log")
fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
aud_logger.addHandler(fh)

def log_admin_action(request: FastAPIRequest, action: str, extra: dict = None):
    ip = request.client.host
    user = request.headers.get('x-api-key', 'unknown')
    record = {
        'timestamp': datetime.utcnow().isoformat(),
        'ip': ip,
        'user': user,
        'action': action,
        'extra': extra or {}
    }
    aud_msg = f"{record['timestamp']} | IP: {ip} | User: {user} | {action} | {record['extra']}"
    aud_logger.info(aud_msg)

# --- Enforce HTTPS Middleware ---
class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.scheme != "https":
            url = request.url.replace(scheme="https")
            return RedirectResponse(url)
        return await call_next(request)

def enforce_https(app):
    app.add_middleware(HTTPSRedirectMiddleware)
    return app
