import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useLocation, NavLink } from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  Home,
  FileText,
  MessageSquare,
  Microchip,
  LayoutGrid,
  X,
} from "lucide-react";
import { Header } from "../common/Header";
import { useAuthWrapper } from "../../hooks/auth/useAuthWrapper";

interface NavigationShellProps {
  children: React.ReactNode;
}

/**
 * NavigationShell Component
 * 
 * Top-level layout wrapper providing consistent navigation structure across all pages.
 * 
 * Features:
 * - Top navbar with h-16 sticky positioning
 * - Sidebar with animated collapse: w-64 (expanded) ↔ w-16 (collapsed) on desktop
 * - Sidebar hidden with drawer overlay on mobile
 * - Main content area with max-w-screen-2xl container
 * - Responsive padding (p-6 desktop, p-4 mobile)
 * - Smooth sidebar collapse transitions with Framer Motion (0.3s easeInOut)
 * - Background scroll prevention when drawer is open
 * - Drawer closes on overlay click or Escape key
 * 
 * Requirements satisfied:
 * - 3.1: Top navbar with h-16 sticky positioning
 * - 3.2: Sidebar on left with w-64 on desktop
 * - 3.3: Main content area to the right of sidebar
 * - 3.4: Display sidebar with icons and labels on desktop (≥1280px)
 * - 3.5: Collapse sidebar to icon-only (w-16) on tablet (≥768px and <1280px)
 * - 3.6: Hide sidebar and provide drawer overlay on mobile (<768px)
 * - 3.7: Animate sidebar collapse transitions with duration 0.3s and easeInOut easing
 * - 3.8: Contain main content within max-w-screen-2xl mx-auto container
 * - 3.9: Apply p-6 padding on desktop, p-4 on mobile
 * - 6.5: Show icon-only nav items with tooltips when sidebar is collapsed
 * - 6.6: Show icon + label nav items when sidebar is expanded
 * - 6.8: Render sidebar as drawer overlay on mobile
 * - 6.9: Prevent background scroll when drawer overlay is open
 * - 6.10: Close drawer on overlay click or Escape key press
 * - 9.5: Hide sidebar and use drawer navigation on mobile (<768px)
 * - 9.6: Collapse sidebar to icon-only on tablet (≥768px and <1280px)
 * - 9.7: Display full sidebar with icons and labels on desktop (≥1280px)
 * - 9.8: Use p-4 padding on mobile (<768px)
 * - 9.9: Use p-6 padding on desktop (≥768px)
 * - 10.6: Animate sidebar collapse/expand with duration 0.3s and easeInOut easing
 */
export function NavigationShell({ children }: NavigationShellProps) {
  const { t } = useTranslation();
  const location = useLocation();
  const { isAuthenticated, isLoading, isDepartmentAdmin } = useAuthWrapper();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Define navigation links
  const publicLinks = [
    { path: "/", labelKey: "header.nav.home", icon: Home },
  ];

  const protectedLinks = [
    { path: "/documents", labelKey: "header.nav.documents", icon: FileText },
    { path: "/chat", labelKey: "header.nav.chat", icon: MessageSquare },
    { path: "/adapters", labelKey: "header.nav.adapters", icon: Microchip },
  ];

  const departmentAdminProtectedLinks = [
    { path: "/realms-admin", labelKey: "header.nav.realms", icon: LayoutGrid },
    { path: "/adapters-admin", labelKey: "header.nav.adapters", icon: Microchip },
  ];

  // Determine visible links based on auth state
  const visibleLinks = (() => {
    if (isLoading) return publicLinks;
    const links = isDepartmentAdmin ? departmentAdminProtectedLinks : protectedLinks;
    return isAuthenticated ? [...publicLinks, ...links] : publicLinks;
  })();

  // Close drawer on route change
  useEffect(() => {
    setDrawerOpen(false);
  }, [location.pathname]);

  // Prevent background scroll when drawer is open
  useEffect(() => {
    if (drawerOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [drawerOpen]);

  // Close drawer on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && drawerOpen) {
        setDrawerOpen(false);
      }
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [drawerOpen]);

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Navbar */}
      <Header 
        onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
        onToggleDrawer={() => setDrawerOpen(!drawerOpen)}
      />

      <div className="flex flex-1 relative">
        {/* Desktop Sidebar - Animated collapse between w-64 and w-16 on desktop (≥1280px) */}
        <motion.aside
          initial={false}
          animate={{ width: sidebarCollapsed ? 64 : 256 }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
          className="hidden lg:flex flex-col border-r border-base-content/10 bg-base-100"
          aria-label={t("header.navLabel")}
          aria-expanded={!sidebarCollapsed}
        >
          <nav className="flex-1 p-4">
            <ul className="space-y-1">
              {visibleLinks.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.path;
                return (
                  <li key={link.path}>
                    {sidebarCollapsed ? (
                      <div className="tooltip tooltip-right" data-tip={t(link.labelKey)}>
                        <NavLink
                          to={link.path}
                          className={({ isActive }) =>
                            `flex items-center justify-center w-12 h-12 rounded-lg transition-all ${
                              isActive
                                ? "bg-primary/10 text-primary"
                                : "text-base-content/70 hover:bg-base-200 hover:text-base-content"
                            }`
                          }
                          aria-label={t(link.labelKey)}
                        >
                          <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
                        </NavLink>
                      </div>
                    ) : (
                      <NavLink
                        to={link.path}
                        className={({ isActive }) =>
                          `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                            isActive
                              ? "bg-primary/10 text-primary border-l-4 border-primary"
                              : "text-base-content/70 hover:bg-base-200 hover:text-base-content"
                          }`
                        }
                      >
                        <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
                        <span>{t(link.labelKey)}</span>
                      </NavLink>
                    )}
                  </li>
                );
              })}
            </ul>
          </nav>

          {/* Sidebar Footer */}
          {!sidebarCollapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="p-4 border-t border-base-content/10"
            >
              <p className="text-xs text-base-content/50 text-center">
                {t("app.version")}
              </p>
            </motion.div>
          )}
        </motion.aside>

        {/* Tablet Sidebar - w-16 icon-only on tablet (≥768px and <1280px) */}
        <aside
          className="hidden md:flex lg:hidden flex-col w-16 border-r border-base-content/10 bg-base-100"
          aria-label={t("header.navLabel")}
        >
          <nav className="flex-1 p-2">
            <ul className="space-y-1">
              {visibleLinks.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.path;
                return (
                  <li key={link.path}>
                    <div className="tooltip tooltip-right" data-tip={t(link.labelKey)}>
                      <NavLink
                        to={link.path}
                        className={({ isActive }) =>
                          `flex items-center justify-center w-12 h-12 rounded-lg transition-all ${
                            isActive
                              ? "bg-primary/10 text-primary"
                              : "text-base-content/70 hover:bg-base-200 hover:text-base-content"
                          }`
                        }
                        aria-label={t(link.labelKey)}
                      >
                        <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
                      </NavLink>
                    </div>
                  </li>
                );
              })}
            </ul>
          </nav>
        </aside>

        {/* Mobile Drawer Overlay */}
        <AnimatePresence>
          {drawerOpen && (
            <>
              {/* Backdrop */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 md:hidden"
                onClick={() => setDrawerOpen(false)}
                aria-hidden="true"
              />

              {/* Drawer */}
              <motion.aside
                initial={{ x: -280 }}
                animate={{ x: 0 }}
                exit={{ x: -280 }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
                className="fixed left-0 top-0 bottom-0 w-64 bg-base-100 z-50 md:hidden flex flex-col shadow-xl"
                aria-label={t("header.navLabel")}
              >
                {/* Drawer Header */}
                <div className="flex items-center justify-between p-4 border-b border-base-content/10">
                  <h2 className="text-lg font-semibold">{t("header.title")}</h2>
                  <button
                    onClick={() => setDrawerOpen(false)}
                    className="btn btn-ghost btn-sm btn-circle"
                    aria-label={t("header.closeMenu")}
                  >
                    <X size={20} />
                  </button>
                </div>

                {/* Drawer Navigation */}
                <nav className="flex-1 p-4 overflow-y-auto">
                  <ul className="space-y-1">
                    {visibleLinks.map((link) => {
                      const Icon = link.icon;
                      const isActive = location.pathname === link.path;
                      return (
                        <li key={link.path}>
                          <NavLink
                            to={link.path}
                            className={({ isActive }) =>
                              `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                                isActive
                                  ? "bg-primary text-primary-content"
                                  : "text-base-content/70 hover:bg-base-200 hover:text-base-content"
                              }`
                            }
                          >
                            <Icon size={20} strokeWidth={isActive ? 2.5 : 2} />
                            <span>{t(link.labelKey)}</span>
                          </NavLink>
                        </li>
                      );
                    })}
                  </ul>
                </nav>

                {/* Drawer Footer */}
                <div className="p-4 border-t border-base-content/10">
                  <p className="text-xs text-base-content/50 text-center">
                    {t("app.version")}
                  </p>
                </div>
              </motion.aside>
            </>
          )}
        </AnimatePresence>

        {/* Main Content Area */}
        <main className="flex-1 overflow-x-hidden">
          <div className="container mx-auto max-w-screen-2xl px-4 md:px-6 py-4 md:py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
