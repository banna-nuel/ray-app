/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        background: '#09090b',
        surface: '#18181b',
        border: '#27272a',
        accent: '#7c3aed',
        'accent-hover': '#6d28d9',
        'text-primary': '#fafafa',
        'text-muted': '#71717a',
      },
      fontFamily: {
        sans: ['Geist Sans', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
