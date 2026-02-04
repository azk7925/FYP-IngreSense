/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#0f172a", // Slate 900
                secondary: "#334155", // Slate 700
                accent: "#3b82f6", // Blue 500
                "accent-dark": "#1d4ed8", // Blue 700
                safe: "#10b981", // Emerald 500
                danger: "#ef4444", // Red 500
                warning: "#f59e0b", // Amber 500
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
