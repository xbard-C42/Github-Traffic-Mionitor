// src/traffic_monitor/ui/EnvSetup.jsx
import React, { useState } from "react";
import axios from "axios";

const ENV_VARS = [
  { name: 'TRAFFIC_API_KEY', label: 'API Key', description: 'A strong secret for backend protection' },
  { name: 'TRAFFIC_CORS_ORIGINS', label: 'Allowed Frontend URLs', description: 'Comma-separated list, e.g., https://yourdomain.com,http://localhost:3000' },
  { name: 'GITHUB_TOKEN', label: 'GitHub Personal Access Token', description: 'Must have repo: or public_repo: access' },
  { name: 'TRAFFIC_CONFIG', label: 'Config file path', description: 'Optional: Defaults to /app/config.yml' },
  { name: 'TRAFFIC_HISTORY', label: 'History file path', description: 'Optional: Defaults to /app/traffic_history.json' },
];

const API_URL = "/api/setup/env";

export default function EnvSetup({ autoToken }) {
  const [form, setForm] = useState(() =>
    Object.fromEntries(ENV_VARS.map(v => [v.name, ""]))
  );
  const [setupToken, setSetupToken] = useState("");
  const [restart, setRestart] = useState(false);
  const [generated, setGenerated] = useState("");
  const [serverStatus, setServerStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const finalToken = autoToken || setupToken;

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleToken = (e) => setSetupToken(e.target.value);
  const handleRestart = (e) => setRestart(e.target.checked);

  const handleGenerate = (e) => {
    e.preventDefault();
    const lines = ENV_VARS
      .filter(v => form[v.name])
      .map(v => `${v.name}=${JSON.stringify(form[v.name])}`);
    setGenerated(lines.join("\n"));
  };

  const handlePost = async (e) => {
    e.preventDefault();
    setLoading(true);
    setServerStatus(null);
    try {
      const env_vars = ENV_VARS.filter(v => form[v.name]).map(v => ({ name: v.name, value: form[v.name] }));
      const payload = { token: finalToken, env_vars, restart };
      const res = await axios.post(API_URL, payload);
      if (res.data.success) {
        setServerStatus({ ok: true, msg: `Saved to ${res.data.path}` + (res.data.restarted ? ' and server restart triggered.' : '') });
      } else {
        setServerStatus({ ok: false, msg: 'Server rejected the request' });
      }
    } catch (err) {
      setServerStatus({ ok: false, msg: err.response?.data?.detail || err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-gray-900 p-8 rounded-xl shadow text-white mt-12">
      <h2 className="text-2xl font-bold mb-6">Initial Setup: <span className="text-blue-400">.env File Generator</span></h2>
      <form onSubmit={handleGenerate}>
        {ENV_VARS.map(v => (
          <div key={v.name} className="mb-5">
            <label htmlFor={v.name} className="block font-semibold text-lg mb-1">{v.label}</label>
            <input
              id={v.name}
              type="text"
              name={v.name}
              autoComplete="off"
              className="w-full px-3 py-2 rounded bg-gray-800 text-white border border-gray-700"
              value={form[v.name]}
              onChange={handleChange}
            />
            <div className="text-xs text-gray-400 mt-1">{v.description}</div>
          </div>
        ))}
        <button type="submit" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-4 mr-2">Generate .env</button>
      </form>

      <div className="mt-8 border-t border-gray-700 pt-6">
        <label className="block font-semibold text-lg mb-2">Server-Side Write</label>
        {!autoToken && (
          <div className="mb-2">
            <label htmlFor="setup-token" className="block font-semibold text-sm mb-1">Setup Token</label>
            <input
              id="setup-token"
              type="password"
              name="setup-token"
              placeholder="Setup token (from server admin)"
              value={setupToken}
              onChange={handleToken}
              className="px-3 py-2 w-full rounded bg-gray-800 text-white border border-gray-700"
            />
          </div>
        )}
        <div className="mb-3 flex items-center gap-2">
          <input type="checkbox" id="restart" checked={restart} onChange={handleRestart} className="h-4 w-4 rounded bg-gray-700 border-gray-600 text-blue-500 focus:ring-blue-600" />
          <label htmlFor="restart" className="font-semibold">Restart server after write</label>
        </div>
        <button
          className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded disabled:bg-gray-600"
          onClick={handlePost}
          disabled={loading || !finalToken}
        >
          {loading ? "Submitting..." : "Write to Server"}
        </button>
        {serverStatus && (
          <div className={`mt-4 p-3 rounded ${serverStatus.ok ? 'bg-green-800' : 'bg-red-800'}`}>{serverStatus.msg}</div>
        )}
      </div>

      {generated && (
        <div className="mt-8">
          <label className="block font-semibold mb-2">Copy this to your <code>.env</code>:</label>
          <pre className="bg-gray-800 p-4 rounded-xl whitespace-pre-wrap text-sm overflow-x-auto">{generated}</pre>
        </div>
      )}
    </div>
  );
}