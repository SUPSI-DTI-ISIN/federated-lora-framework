import { useState } from "react";
import { useTranslation } from "react-i18next";
import { NavLink, Link } from "react-router-dom";
import { Home, FileText, MessageSquare, Menu, X, Microchip } from "lucide-react";
import { motion } from "framer-motion";
import { LanguageSwitcher } from "../header/LanguageSwitcher";

export const Header = () => {
    const { t } = useTranslation();
    const [mobileOpen, setMobileOpen] = useState(false);

    const navigationLinks = [
        { path: "/", labelKey: "header.nav.home", icon: Home },
        { path: "/documents", labelKey: "header.nav.documents", icon: FileText },
        { path: "/chat", labelKey: "header.nav.chat", icon: MessageSquare },
        { path: "/adapters", labelKey: "header.nav.adapters", icon: Microchip },
    ];

    return (
        <header className="sticky top-0 z-50 bg-base-200/80 backdrop-blur-sm border-b border-base-300">
            <div className="max-w-7xl mx-auto px-4">
                <div className="navbar h-16">
                    {/* START: Brand */}
                    <div className="navbar-start">
                        <Link to="/" className="flex items-center gap-3">
                            <motion.div
                                initial={{ scale: 1 }}
                                whileHover={{ scale: 1.03 }}
                                whileTap={{ scale: 0.97 }}
                                className="flex items-center gap-3"
                            >
                                <div
                                    aria-hidden
                                    className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center text-primary-content font-semibold"
                                >
                                    {t("header.logoInitials")}
                                </div>
                                <span className="hidden sm:inline text-lg font-semibold text-base-content">
                  {t("header.title")}
                </span>
                            </motion.div>
                        </Link>
                    </div>

                    {/* CENTER: Desktop nav */}
                    <div className="navbar-center hidden lg:flex">
                        <nav aria-label={t("header.navLabel") as string}>
                            <ul className="menu menu-horizontal px-1 gap-2">
                                {navigationLinks.map((link) => {
                                    const Icon = link.icon;
                                    return (
                                        <li key={link.path}>
                                            <NavLink
                                                to={link.path}
                                                className={({ isActive }) =>
                                                    `flex items-center gap-2 px-3 py-2 rounded-md transition-colors ${
                                                        isActive ? "bg-primary text-primary-content" : "hover:bg-base-300"
                                                    }`
                                                }
                                            >
                                                <Icon size={16} />
                                                <span>{t(link.labelKey)}</span>
                                            </NavLink>
                                        </li>
                                    );
                                })}
                            </ul>
                        </nav>
                    </div>

                    {/* END: actions (mobile menu + language switcher) */}
                    <div className="navbar-end flex items-center gap-3">
                        {/* Mobile menu toggle visible on small screens */}
                        <button
                            className="lg:hidden btn btn-ghost btn-circle"
                            aria-label={mobileOpen ? t("header.closeMenu") : t("header.openMenu")}
                            onClick={() => setMobileOpen((s) => !s)}
                        >
                            {mobileOpen ? <X size={18} /> : <Menu size={18} />}
                        </button>

                        {/* Language switcher component (kept as your existing one) */}
                        <div className="hidden sm:block">
                            <LanguageSwitcher />
                        </div>
                    </div>
                </div>

                {/* Mobile nav panel */}
                {mobileOpen && (
                    <div className="lg:hidden border-t border-base-300 bg-base-100/90">
                        <div className="px-4 py-3 space-y-2">
                            <nav aria-label={t("header.navLabel") as string}>
                                {navigationLinks.map((link) => {
                                    const Icon = link.icon;
                                    return (
                                        <NavLink
                                            key={link.path}
                                            to={link.path}
                                            onClick={() => setMobileOpen(false)}
                                            className={({ isActive }) =>
                                                `flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                                                    isActive ? "bg-primary text-primary-content" : "hover:bg-base-200"
                                                }`
                                            }
                                        >
                                            <Icon size={16} />
                                            <span>{t(link.labelKey)}</span>
                                        </NavLink>
                                    );
                                })}
                            </nav>

                            {/* Language switcher shown also inside mobile menu */}
                            <div className="pt-2">
                                <LanguageSwitcher />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </header>
    );
};