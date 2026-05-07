import {useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import {useNavigate} from "react-router-dom";
import {Home, FileText, MessageSquare, Menu, X, Microchip, LayoutGrid, Network} from "lucide-react";
import {LanguageSwitcher} from "./LanguageSwitcher.tsx";
import {ThemeToggle} from "./ThemeToggle.tsx";
import {useAuthWrapper} from "../../../hooks/auth/useAuthWrapper.ts";
import {useSelectorRealm} from "../../../hooks/realm/useSelectorRealm.ts";
import {HeaderBranding} from "./HeaderBranding.tsx";
import {DesktopNav} from "./DesktopNav.tsx";
import {ProfileDropdown} from "./ProfileDropdown.tsx";
import {MobileMenu} from "./MobileMenu.tsx";

export const Header = () => {
    const {t} = useTranslation();
    const navigate = useNavigate();
    const [mobileOpen, setMobileOpen] = useState(false);
    const {isAuthenticated, isLoading, logout, user, isDepartmentAdmin} = useAuthWrapper();
    const {realm} = useSelectorRealm();

    const publicLinks = [
        {path: "/", labelKey: "header.nav.home", icon: Home},
    ];

    const protectedLinks = [
        {path: "/documents", labelKey: "header.nav.documents", icon: FileText},
        {path: "/chat", labelKey: "header.nav.chat", icon: MessageSquare},
        {path: "/adapters", labelKey: "header.nav.adapters", icon: Microchip},
    ];

    const departmentAdminProtectedLinks = [
        {path: "/realms-admin", labelKey: "header.nav.realms", icon: LayoutGrid},
        {path: "/adapters-admin", labelKey: "header.nav.adapters", icon: Microchip},
        {path: "/federated-learning-jobs", labelKey: "header.nav.federatedLearning", icon: Network},
    ];

    const visibleLinks = useMemo(() => {
        if (isLoading) return publicLinks;
        const links = isDepartmentAdmin ? departmentAdminProtectedLinks : protectedLinks;
        return isAuthenticated ? [...publicLinks, ...links] : publicLinks;
    }, [isAuthenticated, isLoading, isDepartmentAdmin]);

    const handleLogin = () => {
        navigate("/realms");
    };

    return (
        <header
            className="sticky top-0 z-50 w-full border-b border-base-content/10 bg-base-100/60 backdrop-blur-md transition-all duration-300">
            <div className="container mx-auto px-4 py-2">
                <div className="navbar min-h-16 px-0">
                    <div className="navbar-start">
                        <HeaderBranding isAuthenticated={isAuthenticated} realm={realm}/>
                    </div>

                    <div className="navbar-center hidden lg:flex">
                        <DesktopNav links={visibleLinks}/>
                    </div>

                    <div className="navbar-end gap-2 flex items-center">
                        <div className="hidden sm:flex mr-2">
                            <LanguageSwitcher/>
                        </div>

                        <ThemeToggle/>

                        <div className="relative">
                            {isLoading ? (
                                <div className="flex h-10 w-10 items-center justify-center">
                                    <span className="loading loading-spinner loading-sm text-primary"/>
                                </div>
                            ) : isAuthenticated ? (
                                <ProfileDropdown
                                    username={user!.profile.preferred_username ?? user!.profile.sub}
                                    onLogout={logout}
                                />
                            ) : (
                                <button className="btn" onClick={handleLogin}>
                                    {t("header.login", "Login")}
                                </button>
                            )}
                        </div>

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

            <MobileMenu
                isOpen={mobileOpen}
                onClose={() => setMobileOpen(false)}
                links={visibleLinks}
                isAuthenticated={isAuthenticated}
                isLoading={isLoading}
                username={user?.profile.preferred_username ?? user?.profile.sub}
                onLogin={handleLogin}
                onLogout={logout}
            />
        </header>
    );
};