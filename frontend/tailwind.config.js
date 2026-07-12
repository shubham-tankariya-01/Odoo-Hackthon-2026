/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        md: {
          primary: '#6750A4',
          'on-primary': '#FFFFFF',
          'secondary-container': '#E8DEF8',
          'on-secondary-container': '#1D192B',
          tertiary: '#7D5260',
          'surface-container': '#F3EDF7',
          'surface-container-low': '#E7E0EC',
          background: '#FFFBFE',
          surface: '#FFFBFE',
          'on-surface': '#1C1B1F',
          outline: '#79747E',
          'on-surface-variant': '#49454F',
        }
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
      transitionTimingFunction: {
        'md-emphasized': 'cubic-bezier(0.2, 0, 0, 1)',
      }
    },
  },
  plugins: [],
}
