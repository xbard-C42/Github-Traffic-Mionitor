// src/traffic_monitor/ui/EnvSetupGuarded.jsx
import React, { useState } from "react";
import EnvSetup from "./env_setup_react.jsx";

// Secure admin panel with simple token guard in sessionStorage
export default function EnvSetupGuarded() {
  const [hasToken, setHasToken] = useState(!!sessionStorage.getItem('setup_token'));
  const [input, setInput] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) {
      setError("Enter your setup token.");
      return;
    }
    // Just store locally for panel access (does not validate with server until write)
    sessionStorage.setItem('setup_token', input);
    setHasToken(true);
    setInput("");
    setError(null);
  };

  // Patch EnvSetup to always use the stored token for server writes
  function EnvSetupWithAutoToken(props) {
    const token = sessionStorage.getItem('setup_token') || "";
    return <EnvSetup autoToken={token} {...props} />;
  }

  if (!hasToken) {
    return (
      <div className="max-w-md mx-auto mt-32 bg-gray-900 p-10 rounded-xl text-white">
        <h2 className="text-2xl font-bold mb-6 text-center">Admin Setup Login</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="setup-token-input" className="sr-only">Setup Token</label>
          <input
            id="setup-token-input"
            type="password"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Enter setup token"
            className="mb-4 px-4 py-2 w-full rounded bg-gray-800 text-white border border-gray-700"
            autoFocus
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full"
          >
            Unlock Admin Panel
          </button>
          {error && <div className="mt-3 text-red-400 text-sm">{error}</div>}
        </form>
      </div>
    );
  }

  return <EnvSetupWithAutoToken />;
}