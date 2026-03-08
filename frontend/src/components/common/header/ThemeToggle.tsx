import {useEffect, useState} from 'react';
import {Moon, Sun} from 'lucide-react';
import {motion, AnimatePresence} from 'framer-motion';
import {useTranslation} from 'react-i18next';

type Theme = 'light' | 'dark';

interface ThemeToggleProps {
    className?: string;
}

export const ThemeToggle = ({className = ''}: ThemeToggleProps) => {
    const {t} = useTranslation();
    const [theme, setTheme] = useState<Theme>('light');

    useEffect(() => {
        const savedTheme = localStorage.getItem('theme') as Theme | null;

        if (savedTheme) {
            setTheme(savedTheme);
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else {
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
                    initial={{opacity: 0, scale: 0.8, rotate: -90}}
                    animate={{opacity: 1, scale: 1, rotate: 0}}
                    exit={{opacity: 0, scale: 0.8, rotate: 90}}
                    transition={{duration: 0.2}}
                >
                    {theme === 'light' ? (
                        <Moon size={20} strokeWidth={2}/>
                    ) : (
                        <Sun size={20} strokeWidth={2}/>
                    )}
                </motion.div>
            </AnimatePresence>
        </button>
    );
}
