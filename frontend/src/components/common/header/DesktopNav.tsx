import {NavLink, useLocation} from "react-router-dom";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import type {LucideIcon} from "lucide-react";

interface NavLink {
    path: string;
    labelKey: string;
    icon: LucideIcon;
}

interface DesktopNavProps {
    links: NavLink[];
}

export const DesktopNav = ({links}: DesktopNavProps) => {
    const {t} = useTranslation();
    const location = useLocation();

    return (
        <nav aria-label={t("header.navLabel")}>
            <ul className="flex items-center gap-1 p-0">
                {links.map((link) => {
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
    );
}
