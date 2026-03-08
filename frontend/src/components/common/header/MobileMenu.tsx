import {NavLink} from "react-router-dom";
import {useTranslation} from "react-i18next";
import {motion, AnimatePresence} from "framer-motion";
import type {LucideIcon} from "lucide-react";
import {LanguageSwitcher} from "./LanguageSwitcher.tsx";
import {ThemeToggle} from "./ThemeToggle.tsx";

interface NavLink {
    path: string;
    labelKey: string;
    icon: LucideIcon;
}

interface MobileMenuProps {
    isOpen: boolean;
    onClose: () => void;
    links: NavLink[];
    isAuthenticated: boolean;
    isLoading: boolean;
    username?: string;
    onLogin: () => void;
    onLogout: () => void;
}

export const MobileMenu = ({
                               isOpen,
                               onClose,
                               links,
                               isAuthenticated,
                               isLoading,
                               username,
                               onLogin,
                               onLogout,
                           }: MobileMenuProps) => {
    const {t} = useTranslation();

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    id="mobile-menu"
                    initial={{height: 0, opacity: 0}}
                    animate={{height: "auto", opacity: 1}}
                    exit={{height: 0, opacity: 0}}
                    className="overflow-hidden lg:hidden border-t border-base-content/10 bg-base-100"
                >
                    <nav className="flex flex-col gap-1 p-4" aria-label={t("header.navLabel")}>
                        {links.map((link) => {
                            const Icon = link.icon;
                            return (
                                <NavLink
                                    key={link.path}
                                    to={link.path}
                                    onClick={onClose}
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

                        <div className="mt-2 px-4 sm:hidden">
                            <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-base-content/40">
                                {t("header.settings.theme", "Theme")}
                            </p>
                            <ThemeToggle/>
                        </div>

                        <div className="px-4 pt-4">
                            {isLoading ? (
                                <div className="flex h-10 w-10 items-center justify-center">
                                    <span className="loading loading-spinner loading-sm text-primary"/>
                                </div>
                            ) : isAuthenticated ? (
                                <div className="flex gap-2 items-center">
                                    <div className="flex-1 text-sm">{username}</div>
                                    <button className="btn btn-ghost" onClick={onLogout}>
                                        Logout
                                    </button>
                                </div>
                            ) : (
                                <button className="btn w-full" onClick={onLogin}>
                                    {t("header.login", "Login")}
                                </button>
                            )}
                        </div>
                    </nav>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
