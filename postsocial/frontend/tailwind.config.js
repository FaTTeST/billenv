/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fdf8f6',
          100: '#f2e8e4',
          200: '#eaddd7',
          300: '#e0ccc5',
          400: '#d6b3a8',
          500: '#c99384',
          600: '#b87562',
          700: '#a05f4e',
          800: '#854f41',
          900: '#6e4439',
        },
      },
    },
  },
  plugins: [],
}
