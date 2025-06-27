# Github-Traffic-Monitor

# GitHub Traffic Monitor - Frontend

This is the React-based frontend for the **GitHub Traffic Monitor**, a secure, full-stack application designed to track, visualize, and analyze traffic to your GitHub repositories. It provides a modern, interactive dashboard with trend analytics and an optional admin-only panel for server configuration.

Built with **React, Vite, Tailwind CSS, and Recharts**.

---

## 📊 Features

- **Interactive Dashboard:** Visualize views, clones, and unique visitor counts for all your repositories.
- **Repository Selector:** Easily switch between different repositories to view their specific traffic data.
- **Trend Analysis:** An interactive line chart shows traffic trends over time, based on historical snapshots collected by the backend.
- **Metric Cards:** At-a-glance cards show the latest traffic numbers and the percentage change compared to the previous data point.
- **AI-Powered Insights:** A built-in "AI Traffic Analyst" feature (powered by Google Gemini) provides a narrative summary of repository trends.
- **Secure Admin Panel:** A separate, token-protected route (`/setup`) allows administrators to configure the backend server's environment variables directly from the UI.

### UI Mockup
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

---

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (LTS version recommended)
- `npm` or `yarn` for package management
- A running instance of the [GitHub Traffic Monitor backend API](https://github.com/your-org/github-traffic-monitor). This frontend is configured to proxy API requests to `http://localhost:8000` during development.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```sh
    npm install
    ```

### Running the Development Server

To start the Vite development server, run:

```sh
npm run dev
```

This will start the application, typically on `http://localhost:5173`. The app will automatically reload when you make changes to the source files.

**API Proxying:** All API requests made from the frontend to `/api/...` will be automatically proxied to the backend server running at `http://localhost:8000`. This is configured in `vite.config.js` and avoids CORS issues during local development.

---

## ⚙️ Available Scripts

This project uses `npm` scripts for common tasks:

-   `npm run dev`: Starts the Vite development server with Hot Module Replacement (HMR).
-   `npm run build`: Compiles and bundles the React application for production into the `dist` directory.
-   `npm run preview`: Serves the production build locally to preview it before deployment.
-   `npm run start`: An alias for `npm run dev`.

---

## 🏗️ Building for Production

To create an optimized production build, run:

```sh
npm run build
```

This will generate static HTML, CSS, and JavaScript files in the `./dist` directory. These files are ready to be deployed to any static hosting service or served by the Python backend.

---

## License
