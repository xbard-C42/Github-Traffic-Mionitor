# GitHub Traffic Monitor – Feature Overview & UI

## What does the app do?

**GitHub Traffic Monitor** is a secure, full-stack solution for:

- Fetching and displaying traffic analytics (views, unique views, clones, unique clones) for *all* your GitHub repositories.
- Automatically storing a history of each traffic snapshot over time (with timestamps).
- Presenting real-time and historical traffic trends in an interactive, modern dashboard.
- Providing a secure, admin-only panel for environment/config setup and live secret management.

---

## What does it display? (UI)

### 1. **Login/Admin Guard (Setup only)**

- If enabled, an admin login prompts for a setup token before exposing sensitive environment/secret config routes.

### 2. **Main Dashboard**

- **Repository selector:** Dropdown to filter analytics by any repo in your GitHub account/org
- **Latest metrics cards:**
  - Views (latest)
  - Unique views (latest)
  - Clones (latest)
  - Unique clones (latest)
  - Each card shows percent change vs previous snapshot
- **Trends chart:**
  - Interactive line chart for views and clones (over time, per repo)
  - X-axis: timestamp, Y-axis: count
  - Supports long-term historical tracking (all snapshots)
- **History table:** (optional, easy to add)
  - Each snapshot per repo, with all stats and timestamp

### 3. **Environment Setup Panel (Admin only, optional)**

- Fill-in-the-blank form for all required `.env`/secret values
- “Write to Server” securely updates backend config
- Option to trigger safe server restart from UI
- Full copy-paste `.env` generator for manual or CI/CD use

### 4. **Security, Monitoring, and Audit**

- All traffic and refresh endpoints require API key authentication
- Rate limiting on all API endpoints (default: 30/min)
- Admin/audit actions logged with IP and timestamp
- HTTPS enforced (if enabled)
- Admin setup panel protected by one-time setup token (session-only access)

---

## Who is this for?

- Indie devs, teams, or orgs who want a private, multi-repo GitHub traffic dashboard
- Security-conscious users (never expose secrets, strict admin controls)
- Anyone who wants modern UI/UX and real trend analytics for their code visibility

---

## Example (UI screenshot)\*

```
+--------------------------------------------------------------+
|        GitHub Traffic Monitor 📊   [Repo selector ▼]         |
+------------------+-----------------+------------------------+
|  Views:   1400   |  Clones: 21     |  Unique Views: 210     |
|  Δ +12% vs prev  |  Δ -2%  vs prev |  Unique Clones: 9      |
+------------------+-----------------+------------------------+
|     [  Trend chart: views/clones vs time  ]                 |
+-------------------------------------------------------------+
|        [History Table: per-snapshot, per-repo stats]        |
+-------------------------------------------------------------+
|   [Setup Panel: only for admins during config, not public]   |
+-------------------------------------------------------------+
```

\*Replace with real screenshot when deployed.

---

For more, see the README, security notes, or run the app in dev mode!

