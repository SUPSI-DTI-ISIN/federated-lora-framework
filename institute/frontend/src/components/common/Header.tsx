import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { FileText, MessageSquare, Home } from 'lucide-react';
import { motion } from 'framer-motion';
import {LanguageSwitcher} from "../header/LanguageSwitcher.tsx";

export const Header = () => {
    const { t } = useTranslation();
    const location = useLocation();

    const navigationLinks = [
        { path: '/', label: 'header.nav.home', icon: Home },
        { path: '/documents', label: 'header.nav.documents', icon: FileText },
        { path: '/chat', label: 'header.nav.chat', icon: MessageSquare },
    ];

    const isActive = (path: string) => location.pathname === path;

    return (
        <header className="sticky top-0 z-50 bg-base-200 shadow-lg">
            <div className="navbar max-w-7xl mx-auto px-4">
                <div className="navbar-start">
                    <Link to="/" className="flex items-center gap-2 group">
                        <motion.div
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="flex items-center gap-2"
                        >
                            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center text-primary-content font-bold text-xl">
                                IS
                            </div>
                            <span className="text-xl font-bold text-base-content group-hover:text-primary transition-colors">
                                {t('header.title')}
                            </span>
                        </motion.div>
                    </Link>
                </div>

                <div className="navbar-center hidden lg:flex">
                    <ul className="menu menu-horizontal px-1 gap-2">
                        {navigationLinks.map((navigationLink) => {
                            const Icon = navigationLink.icon;
                            const active = isActive(navigationLink.path);

                            return (
                                <li key={navigationLink.path}>
                                    <Link
                                        to={navigationLink.path}
                                        className={`flex items-center gap-2 ${
                                            active
                                                ? 'bg-primary text-primary-content'
                                                : 'hover:bg-base-300'
                                        }`}
                                    >
                                        <Icon size={18} />
                                        {t(navigationLink.label)}
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                </div>

                <div className="navbar-end">
                    {/* Mobile Menu */}
                    <div className="dropdown dropdown-end lg:hidden">
                        <label tabIndex={0} className="btn btn-ghost btn-circle">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7" />
                            </svg>
                        </label>
                        <ul tabIndex={0} className="menu menu-sm dropdown-content mt-3 z-1 p-2 shadow bg-base-200 rounded-box w-52">
                            {navigationLinks.map((navigationLink) => {
                                const Icon = navigationLink.icon;
                                const active = isActive(navigationLink.path);

                                return (
                                    <li key={navigationLink.path}>
                                        <Link to={navigationLink.path} className={`flex items-center gap-2 ${
                                            active
                                                ? 'bg-primary text-primary-content'
                                                : 'hover:bg-base-300'
                                        }`}>
                                            <Icon size={18} />
                                            {t(navigationLink.label)}
                                        </Link>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                </div>

                <LanguageSwitcher />
            </div>
        </header>
    );
};