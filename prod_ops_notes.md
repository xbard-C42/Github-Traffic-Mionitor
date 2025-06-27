# Production Ops & Checklist: GitHub Traffic Monitor

## 1. Security & Secrets
- [ ] Set strong, unique values for `TRAFFIC_API_KEY` and `GITHUB_TOKEN`.
- [ ] Set `TRAFFIC_SETUP_TOKEN` only during initial config, then remove/unset or rotate.
- [ ] Use Docker secrets, `.env`, or environment injection (never hardcode in source).
- [ ] Restrict CORS origins with `TRAFFIC_CORS_ORIGINS` to only trusted frontend domains.
- [ ] Use HTTPS (`ENFORCE_HTTPS=1`); serve behind TLS (nginx, Caddy, or cloud provider).
- [ ] Audit `admin_audit.log` regularly for any suspicious or unauthorised access.

## 2. Deployment
- [ ] Build the multi-stage Docker image for unified frontend/backend hosting.
- [ ] If running standalone: use `supervisor`/`systemd` to auto-restart API on crash/reboot.
- [ ] If deploying in cloud (AWS, Azure, etc.), set secrets using their respective secrets manager.

## 3. Maintenance & Monitoring
- [ ] Use the React dashboard to monitor trends and ensure collection is running.
- [ ] Set up log rotation for `admin_audit.log` and `traffic_monitor.log`.
- [ ] Periodically prune old data from `traffic_history.json` as needed.
- [ ] Enable alerting for failed fetches, high error rates, or unusual traffic (optional: integrate with Slack/email).

## 4. Updates & Scaling
- [ ] Run `npm audit` and `pip list --outdated` monthly to keep deps up to date.
- [ ] Pin versions in `requirements.txt` and `package.json` for deterministic builds.
- [ ] Consider horizontal scaling via Docker Compose or Kubernetes if under high load.

## 5. Disable Admin/Setup After Use
- [ ] Remove or firewall off `/api/setup/env` and setup React routes after initial deployment.
- [ ] Rotate setup tokens and API keys if you ever suspect leak or compromise.

## 6. Additional Hardening (Optional)
- [ ] Enable IP allowlisting (via nginx/cloud/host firewall)
- [ ] Integrate 2FA for admin routes (see TOTP/OAuth libraries)
- [ ] Set up Sentry or another exception monitoring system for error alerting
- [ ] Run full end-to-end test suite after upgrades

---

**For questions or advanced ops, see: README or consult your platform’s security docs.**

