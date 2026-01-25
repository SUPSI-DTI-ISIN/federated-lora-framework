/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            animation: {
                'fade-in': 'fadeIn 0.3s ease-out',
                'slide-in': 'slideIn 0.3s ease-out',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideIn: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(0)' },
                },
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
            },
        },
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: [
            {
                light: {
                    ...require("daisyui/src/theming/themes")["light"],
                    "primary": "#3b82f6",
                    "secondary": "#8b5cf6",
                    "accent": "#06b6d4",
                    "neutral": "#1f2937",
                    "base-100": "#ffffff",
                    "base-200": "#f8fafc",
                    "base-300": "#f1f5f9",
                    "base-content": "#1e293b",
                    "info": "#0ea5e9",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                },
                dark: {
                    ...require("daisyui/src/theming/themes")["dark"],
                    "primary": "#60a5fa",
                    "secondary": "#a78bfa",
                    "accent": "#22d3ee",
                    "neutral": "#374151",
                    "base-100": "#0f172a",
                    "base-200": "#1e293b",
                    "base-300": "#334155",
                    "base-content": "#f8fafc",
                    "info": "#38bdf8",
                    "success": "#34d399",
                    "warning": "#fbbf24",
                    "error": "#f87171",
                },
            },
        ],
        darkTheme: "dark",
        base: true,
        styled: true,
        utils: true,
        logs: false,
    },
}