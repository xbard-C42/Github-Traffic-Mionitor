/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider, Link } from 'react-router-dom';
import axios from 'axios';
import App from './traffic_dashboard_react.jsx';
import EnvSetupGuarded from './env_setup_react_admin_guard.jsx';
import './main.css';

// Set the base URL for all axios requests to the current window's origin.
// This ensures that relative API paths like "/api/traffic" resolve correctly
// in all environments, fixing "Invalid URL" errors.
if (typeof window !== 'undefined') {
  axios.defaults.baseURL = window.location.origin;
}

const ErrorPage = () => (
    <div className="min-h-screen bg-gray-950 text-white font-mono px-6 py-8 flex flex-col items-center justify-center text-center">
        <h1 className="text-4xl font-bold text-red-500 mb-4">Oops! Page Not Found</h1>
        <p className="text-lg text-gray-400 mb-6">The page you are looking for does not exist.</p>
        <Link to="/" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Return to Dashboard
        </Link>
    </div>
);


const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: '/setup',
    element: <EnvSetupGuarded />,
  },
]);

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <RouterProvider router={router} />
    </React.StrictMode>
  );
}