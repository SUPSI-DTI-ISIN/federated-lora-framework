import { useEffect, useState } from 'react';
import { Moon, Sun } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';

type Theme = 'light' | 'dark';

interface ThemeToggleProps {
  className?: string;
}

/**
 * ThemeToggle Component
 * 
 * A reusable component that manages dark/light theme switching with localStorage persistence.
 * 
 * Features:
 * - Persists theme preference to localStorage under the key "theme"
 * - Detects OS preference using window.matchMedia when no saved theme exists
 * - Updates html data-theme attribute for DaisyUI theme switching
 * - Animates icon transitions using Framer Motion AnimatePresence
 * - Displays Sun icon for light mode and Moon icon for dark mode
 * - Fully accessible with aria-label and title attributes
 * 
 * Requirements satisfied:
 * - 2.1: Persist theme preference in localStorage
 * - 2.2: Detect OS preference when no saved preference exists
 * - 2.3: Apply saved theme on initialization
 * - 2.4: Update data-theme attribute on toggle
 * - 2.5: Save new preference to localStorage
 * - 2.6: Provide toggle with Sun/Moon icons
 * - 2.7: Place toggle in navbar (integrated in Header component)
 * - 2.8: Animate icon transition with Framer Motion
 */
export function ThemeToggle({ className = '' }: ThemeToggleProps) {
  const { t } = useTranslation();
  const [theme, setTheme] = useState<Theme>('light');

  // Initialize theme on mount
  useEffect(() => {
    // Check localStorage first
    const savedTheme = localStorage.getItem('theme') as Theme | null;
    
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
      // Detect OS preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const detectedTheme: Theme = prefersDark ? 'dark' : 'light';
      setTheme(detectedTheme);
      document.documentElement.setAttribute('data-theme', detectedTheme);
      localStorage.setItem('theme', detectedTheme);
    }
  }, []);

  const toggleTheme = () => {
    const newTheme: Theme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <button
      onClick={toggleTheme}
      className={`btn btn-ghost btn-circle ${className}`}
      aria-label={t(`theme.${theme === 'light' ? 'dark' : 'light'}`)}
      title={t(`theme.${theme === 'light' ? 'dark' : 'light'}`)}
    >
      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={theme}
          initial={{ opacity: 0, scale: 0.8, rotate: -90 }}
          animate={{ opacity: 1, scale: 1, rotate: 0 }}
          exit={{ opacity: 0, scale: 0.8, rotate: 90 }}
          transition={{ duration: 0.2 }}
        >
          {theme === 'light' ? (
            <Moon size={20} strokeWidth={2} />
          ) : (
            <Sun size={20} strokeWidth={2} />
          )}
        </motion.div>
      </AnimatePresence>
    </button>
  );
}
