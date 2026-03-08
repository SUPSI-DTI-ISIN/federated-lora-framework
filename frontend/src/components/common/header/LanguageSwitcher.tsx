import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { FiChevronDown, FiGlobe } from 'react-icons/fi';
import { AnimatePresence, motion } from 'framer-motion';
import i18n from "../../../i18n/i18n.ts";
import ReactCountryFlag from "react-country-flag";

export const LanguageSwitcher = () => {
    const { t } = useTranslation();
    const currentLang = i18n.language as string;
    const supportedLngs = (i18n.options.supportedLngs as string[]).filter(l => l !== "cimode");
    const [open, setOpen] = useState(false);
    const switcherRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (switcherRef.current && !switcherRef.current.contains(event.target as Node)) {
                setOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const changeLanguage = (code: string) => {
        i18n.changeLanguage(code);
        setOpen(false);
    };

    return (
        <div ref={switcherRef} className="relative">
            <motion.button
                onClick={() => setOpen(!open)}
                className="flex items-center gap-1.5 px-3 py-2 rounded-full hover:bg-base-200 transition-all duration-300 group"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                aria-label={t('header.language.label')}
                aria-expanded={open}
            >
                <FiGlobe className="w-5 h-5 text-base-content/80 group-hover:text-primary transition-colors" />
                <span className="text-lg">
                    <ReactCountryFlag countryCode={t(`header.language.flags.${currentLang}`)} svg />
                </span>
                <motion.span
                    animate={{ rotate: open ? 180 : 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <FiChevronDown className="w-4 h-4 text-base-content/60 group-hover:text-primary transition-colors" />
                </motion.span>
            </motion.button>

            <AnimatePresence>
                {open && (
                    <motion.ul
                        className="absolute right-0 mt-2 w-48 bg-base-100 border border-base-300 rounded-box shadow-lg overflow-hidden z-50"
                        initial={{ opacity: 0, y: -10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -10, scale: 0.95 }}
                        transition={{ type: "spring", stiffness: 400, damping: 30 }}
                    >
                        {supportedLngs.map(lang => (
                            <li key={lang}>
                                <button
                                    onClick={() => changeLanguage(lang)}
                                    className={`w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-base-200 transition-all duration-200 ${
                                        lang === currentLang
                                            ? 'bg-primary/10 text-primary font-medium'
                                            : 'text-base-content'
                                    }`}
                                    aria-current={lang === currentLang ? 'true' : undefined}
                                >
                                    <span className="text-lg">
                                        <ReactCountryFlag countryCode={t(`header.language.flags.${lang}`)} svg />
                                    </span>
                                    <span className="flex-1">{t(`header.language.${lang}`)}</span>
                                    {lang === currentLang && (
                                        <motion.div
                                            className="w-2 h-2 rounded-full bg-primary"
                                            initial={{ scale: 0 }}
                                            animate={{ scale: 1 }}
                                        />
                                    )}
                                </button>
                            </li>
                        ))}
                    </motion.ul>
                )}
            </AnimatePresence>
        </div>
    );
};