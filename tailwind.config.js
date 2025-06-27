// tailwind.config.js
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          950: '#0f1117',
        },
        blue: {
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
        },
        green: {
          500: '#22c55e',
          600: '#16a34a',
          800: '#166534',
        },
        red: {
          800: '#7f1d1d',
        },
      },
      fontFamily: {
        mono: ['Fira Mono', 'Menlo', 'Monaco', 'monospace'],
      },
      borderRadius: {
        'xl': '1rem',
      },
    },
  },
  plugins: [],
};
