// src/traffic_monitor/ui/App.jsx
// GitHub Traffic Monitor React Dashboard
// Requires: React, axios, recharts, dayjs

import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import dayjs from "dayjs";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from "recharts";

const API_URL = "/api/traffic";

function percentDelta(curr, prev) {
  if (prev === 0) return curr > 0 ? "100.0" : "0.0";
  return (((curr - prev) / Math.abs(prev)) * 100).toFixed(1);
}

const AiAnalyst = ({ repoHistory, repoName }) => {
    const [analysis, setAnalysis] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAnalysis = useCallback(async () => {
        setLoading(true);
        setError("");
        setAnalysis("");

        try {
            // This new endpoint must be created on the FastAPI backend.
            // It will securely call the Gemini API with the server-side API key.
            const res = await axios.post('/api/analyze', { repoName, repoHistory });
            
            // The backend should return a JSON object like: { "analysis": "..." }
            if (res.data.analysis) {
                 setAnalysis(res.data.analysis);
            } else {
                 setError("Received an empty analysis from the server.");
            }
        } catch (err) {
            console.error("Analysis API error:", err);
            setError(err.response?.data?.detail || "Failed to generate AI analysis. Ensure the backend /api/analyze endpoint is configured correctly.");
        } finally {
            setLoading(false);
        }
    }, [repoHistory, repoName]);

    return (
        <div className="bg-gray-800 p-4 rounded-xl shadow mt-8">
            <h3 className="text-xl font-bold mb-3">AI Traffic Analyst</h3>
            <p className="text-sm text-gray-400 mb-4">Get an AI-powered summary of the trends for this repository.</p>
            <button
                onClick={handleAnalysis}
                disabled={loading || !repoHistory || repoHistory.length === 0}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded"
            >
                {loading ? "Analyzing..." : "Generate Analysis"}
            </button>
            {error && <div className="mt-4 p-3 rounded bg-red-800 text-white">{error}</div>}
            {analysis && (
                <div className="mt-4 prose prose-invert prose-sm max-w-none whitespace-pre-wrap">
                  {analysis.split('\n').map((line, i) => {
                    if (line.startsWith('* ')) {
                      return <p key={i} className="ml-4 list-item list-disc">{line.substring(2)}</p>
                    }
                    return <p key={i}>{line}</p>
                  })}
                </div>
            )}
        </div>
    );
};

export default function App() {
  const [data, setData] = useState([]);
  const [repos, setRepos] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(API_URL).then(r => {
      setData(r.data.history || []);
      const repoNames = [...new Set(r.data.history.map(x => x.name))];
      setRepos(repoNames);
      if (repoNames.length > 0) {
        setSelectedRepo(repoNames[0]);
      }
      setLoading(false);
    }).catch(err => {
      console.error("Failed to fetch traffic data:", err);
      setError("Could not connect to the traffic monitor API. Please ensure it's running and accessible.");
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-center mt-12 text-xl">Loading traffic data…</div>;
  if (error) return <div className="text-center mt-12 text-xl text-red-500">{error}</div>;
  if (!data.length) return <div className="text-center mt-12 text-xl">No traffic data found.</div>;

  const repoHistory = data.filter(d => d.name === selectedRepo);
  const latest = repoHistory.length ? repoHistory[repoHistory.length - 1] : null;
  const previous = repoHistory.length > 1 ? repoHistory[repoHistory.length - 2] : null;

  return (
    <div className="min-h-screen bg-gray-950 text-white font-mono px-6 py-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">GitHub Traffic Monitor <span className="text-blue-400">📊</span></h1>
        <p className="mb-6 text-gray-400">Track and visualise repo traffic, history and trends in one place.</p>

        <div className="flex items-center gap-2 mb-6">
          <label htmlFor="repo-select" className="font-bold text-lg">Repository:</label>
          <select
            id="repo-select"
            className="bg-gray-900 rounded px-2 py-1 text-lg border border-gray-700"
            value={selectedRepo}
            onChange={e => setSelectedRepo(e.target.value)}
          >
            {repos.map(r => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {latest && (
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="bg-gray-800 p-4 rounded-xl shadow text-center">
              <div className="text-xl font-bold">Views</div>
              <div className="text-3xl">{latest.views_count}</div>
              <div className="text-blue-400">Unique: {latest.views_uniques}</div>
              {previous && (
                <div className={parseFloat(percentDelta(latest.views_count, previous.views_count)) >= 0 ? 'text-green-400' : 'text-red-400'}>
                  {percentDelta(latest.views_count, previous.views_count)}% vs prev
                </div>
              )}
            </div>
            <div className="bg-gray-800 p-4 rounded-xl shadow text-center">
              <div className="text-xl font-bold">Clones</div>
              <div className="text-3xl">{latest.clones_count}</div>
              <div className="text-blue-400">Unique: {latest.clones_uniques}</div>
              {previous && (
                <div className={parseFloat(percentDelta(latest.clones_count, previous.clones_count)) >= 0 ? 'text-green-400' : 'text-red-400'}>
                  {percentDelta(latest.clones_count, previous.clones_count)}% vs prev
                </div>
              )}
            </div>
          </div>
        )}

        <div className="bg-gray-800 p-4 rounded-xl shadow mb-8">
          <div className="font-bold mb-2">Trend</div>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={repoHistory.map(r => ({...r, timestamp: dayjs(r.timestamp).format('YYYY-MM-DD')}))}>
              <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.2} />
              <XAxis dataKey="timestamp" minTickGap={40} tick={{ fill: '#9ca3af' }} />
              <YAxis tick={{ fill: '#9ca3af' }} />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
              <Legend />
              <Line type="monotone" dataKey="views_count" stroke="#60a5fa" name="Views" dot={false} strokeWidth={2}/>
              <Line type="monotone" dataKey="clones_count" stroke="#38bdf8" name="Clones" dot={false} strokeWidth={2}/>
            </LineChart>
          </ResponsiveContainer>
        </div>

        <AiAnalyst repoHistory={repoHistory} repoName={selectedRepo} />
      </div>
    </div>
  );
}