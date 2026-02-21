import {useEffect, useMemo, useRef, useState} from "react";
import {useTranslation} from "react-i18next";
import {NavLink, Link, useLocation} from "react-router-dom";
import {Home, FileText, MessageSquare, Menu, X, Microchip, User, LogOut, LayoutGrid} from "lucide-react";
import {motion, AnimatePresence} from "framer-motion";
import {LanguageSwitcher} from "../header/LanguageSwitcher";
import mimirLogo from "../../assets/mimir-logo.png"
import {useAuthWrapper} from "../../hooks/auth/useAuthWrapper.ts";

export const Header = () => {
    const {t} = useTranslation();
    const [mobileOpen, setMobileOpen] = useState(false);
    const [profileOpen, setProfileOpen] = useState(false);
    const location = useLocation();
    const {isAuthenticated, isLoading, login, logout, user} = useAuthWrapper();
    const profileRef = useRef<HTMLDivElement | null>(null);

    const publicLinks = [
        { path: "/", labelKey: "header.nav.home", icon: Home },
        { path: "/realms", labelKey: "header.nav.realms", icon: LayoutGrid },
    ];

    const protectedLinks = [
        { path: "/documents", labelKey: "header.nav.documents", icon: FileText },
        { path: "/chat", labelKey: "header.nav.chat", icon: MessageSquare },
        { path: "/adapters", labelKey: "header.nav.adapters", icon: Microchip },
    ];

    const visibleLinks = useMemo(() => {
        if (isLoading) return publicLinks;
        return isAuthenticated
            ? [...publicLinks, ...protectedLinks]
            : publicLinks;
    }, [isAuthenticated, isLoading]);

    useEffect(() => {
        function handleClick(e: MouseEvent) {
            if (!profileRef.current) return;
            if (!profileRef.current.contains(e.target as Node)) {
                setProfileOpen(false);
            }
        }

        if (profileOpen) {
            document.addEventListener("mousedown", handleClick);
            return () => document.removeEventListener("mousedown", handleClick);
        }
    }, [profileOpen]);

    return (
        <header
            className="sticky top-0 z-50 w-full border-b border-base-content/10 bg-base-100/60 backdrop-blur-md transition-all duration-300">
            <div className="container mx-auto px-4 py-2">
                <div className="navbar min-h-16 px-0">
                    <div className="navbar-start">
                        <Link
                            to="/"
                            className="group flex items-center gap-3 focus-visible:outline-primary rounded-lg transition-all"
                            aria-label={t("header.nav.home")}
                        >
                            <motion.div whileHover={{scale: 1.01}} whileTap={{scale: 0.99}}
                                        className="flex items-center gap-3">
                                <img src={mimirLogo} alt="Mimir Logo" className="h-10 w-auto"/>
                                <span
                                    className="hidden text-xl font-bold tracking-tight text-base-content sm:inline-block">{t("header.title")}</span>
                            </motion.div>
                        </Link>
                    </div>

                    <div className="navbar-center hidden lg:flex">
                        <nav aria-label={t("header.navLabel")}>
                            <ul className="flex items-center gap-1 p-0">
                                {visibleLinks.map((link) => {
                                    const Icon = link.icon;
                                    const isActive = location.pathname === link.path;
                                    return (
                                        <li key={link.path} className="relative">
                                            <NavLink
                                                to={link.path}
                                                className={({isActive}) =>
                                                    `relative flex items-center gap-2 px-4 py-2 text-sm font-medium transition-colors hover:text-primary ${
                                                        isActive ? "text-primary" : "text-base-content/70"
                                                    }`
                                                }
                                            >
                                                <Icon size={18} strokeWidth={isActive ? 2.5 : 2}/>
                                                <span>{t(link.labelKey)}</span>

                                                {isActive && (
                                                    <motion.div
                                                        layoutId="nav-active"
                                                        className="absolute inset-0 -z-10 rounded-lg bg-primary/10"
                                                        transition={{type: "spring", duration: 0.5}}
                                                    />
                                                )}
                                            </NavLink>
                                        </li>
                                    );
                                })}
                            </ul>
                        </nav>
                    </div>

                    <div className="navbar-end gap-2 flex items-center">
                        <div className="hidden sm:flex mr-2">
                            <LanguageSwitcher />
                        </div>

                        {/* PROFILE / LOGIN area */}
                        <div className="relative" ref={profileRef}>
                            {isLoading ? (
                                <div className="flex h-10 w-10 items-center justify-center">
                                    <span className="loading loading-spinner loading-sm text-primary"/>
                                </div>
                            ) : isAuthenticated ? (
                                <>
                                    <button
                                        className="btn btn-ghost btn-circle"
                                        aria-label="Profile"
                                        onClick={() => setProfileOpen((s) => !s)}
                                        title={user!.profile.preferred_username ?? user!.profile.sub}
                                    >
                                        <User size={18}/>
                                    </button>

                                    <AnimatePresence>
                                        {profileOpen && (
                                            <motion.div
                                                initial={{opacity: 0, scale: 0.95, y: -6}}
                                                animate={{opacity: 1, scale: 1, y: 0}}
                                                exit={{opacity: 0, scale: 0.95, y: -6}}
                                                transition={{duration: 0.12}}
                                                className="absolute right-0 mt-2 w-40 rounded-lg border bg-base-100 p-2 shadow-md"
                                            >
                                                <div className="flex flex-col gap-1">
                                                    <div className="px-2 py-1 text-xs text-base-content/70">
                                                        {user!.profile.preferred_username ?? user!.profile.sub}
                                                    </div>
                                                    <button
                                                        className="flex w-full items-center gap-2 rounded-md px-2 py-2 text-sm hover:bg-base-200"
                                                        onClick={logout}
                                                    >
                                                        <LogOut size={16}/>
                                                        <span>Logout</span>
                                                    </button>
                                                </div>
                                            </motion.div>
                                        )}
                                    </AnimatePresence>
                                </>
                            ) : (
                                <button className="btn" onClick={login}>
                                    {t("header.login", "Login")}
                                </button>
                            )}
                        </div>

                        {/* mobile menu toggle */}
                        <button
                            className="btn btn-ghost btn-circle lg:hidden ml-2"
                            aria-expanded={mobileOpen}
                            aria-controls="mobile-menu"
                            aria-label={mobileOpen ? t("header.closeMenu") : t("header.openMenu")}
                            onClick={() => setMobileOpen((s) => !s)}
                        >
                            {mobileOpen ? <X size={20}/> : <Menu size={20}/>}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile menu */}
            <AnimatePresence>
                {mobileOpen && (
                    <motion.div
                        id="mobile-menu"
                        initial={{height: 0, opacity: 0}}
                        animate={{height: "auto", opacity: 1}}
                        exit={{height: 0, opacity: 0}}
                        className="overflow-hidden lg:hidden border-t border-base-content/10 bg-base-100"
                    >
                        <nav className="flex flex-col gap-1 p-4" aria-label={t("header.navLabel")}>
                            {visibleLinks.map((link) => {
                                const Icon = link.icon;
                                return (
                                    <NavLink
                                        key={link.path}
                                        to={link.path}
                                        onClick={() => setMobileOpen(false)}
                                        className={({isActive}) =>
                                            `flex items-center gap-4 rounded-xl px-4 py-3 text-base font-medium transition-all ${
                                                isActive
                                                    ? "bg-primary text-primary-content shadow-md"
                                                    : "hover:bg-base-200 text-base-content/80"
                                            }`
                                        }
                                    >
                                        <Icon size={20}/>
                                        <span>{t(link.labelKey)}</span>
                                    </NavLink>
                                );
                            })}

                            <div className="mt-4 border-t border-base-content/5 pt-4 sm:hidden">
                                <p className="mb-2 px-4 text-xs font-semibold uppercase tracking-wider text-base-content/40">
                                    {t("header.settings.language")}
                                </p>
                                <div className="px-2">
                                    <LanguageSwitcher/>
                                </div>
                            </div>

                            {/* mobile auth controls */}
                            <div className="px-4 pt-4">
                                {isLoading ? (
                                    <div className="flex h-10 w-10 items-center justify-center">
                                        <span className="loading loading-spinner loading-sm text-primary"/>
                                    </div>
                                ) : isAuthenticated ? (
                                    <div className="flex gap-2 items-center">
                                        <div
                                            className="flex-1 text-sm">{user!.profile.preferred_username ?? user!.profile.sub}</div>
                                        <button className="btn btn-ghost" onClick={logout}>
                                            Logout
                                        </button>
                                    </div>
                                ) : (
                                    <button className="btn w-full" onClick={login}>
                                        {t("header.login", "Login")}
                                    </button>
                                )}
                            </div>
                        </nav>
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
};