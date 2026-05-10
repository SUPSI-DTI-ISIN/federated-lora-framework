import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { Home } from '../Home';
import { AuthWrapperContext } from '../../contexts/auth/authWrapperContext';
import { createElement } from 'react';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({
        t: (key: string, opts?: Record<string, unknown>) => {
            if (opts?.name) return `Welcome, ${opts.name}`;
            return key;
        },
    }),
}));

vi.mock('framer-motion', () => ({
    motion: {
        section: ({ children, ...props }: React.HTMLAttributes<HTMLElement>) => <section {...props}>{children}</section>,
        div: ({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) => <div {...props}>{children}</div>,
    },
    AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

function renderHome(auth: { isAuthenticated: boolean; isDepartmentAdmin: boolean; user?: unknown }) {
    const value = {
        user: auth.user ?? null,
        isAuthenticated: auth.isAuthenticated,
        isDepartmentAdmin: auth.isDepartmentAdmin,
        isLoading: false,
        login: vi.fn(),
        logout: vi.fn(),
    };
    return render(
        createElement(AuthWrapperContext.Provider, { value: value as never },
            createElement(MemoryRouter, {}, <Home />))
    );
}

describe('Home', () => {
    it('renders the hero title', () => {
        renderHome({ isAuthenticated: false, isDepartmentAdmin: false });
        expect(screen.getByText('home.hero.title')).toBeTruthy();
    });

    it('renders the hero subtitle', () => {
        renderHome({ isAuthenticated: false, isDepartmentAdmin: false });
        expect(screen.getByText('home.hero.subtitle')).toBeTruthy();
    });

    it('renders features section title', () => {
        renderHome({ isAuthenticated: false, isDepartmentAdmin: false });
        expect(screen.getByText('home.features.title')).toBeTruthy();
    });

    it('renders how it works section', () => {
        renderHome({ isAuthenticated: false, isDepartmentAdmin: false });
        expect(screen.getByText('home.howItWorks.title')).toBeTruthy();
    });

    it('shows welcome message when authenticated', () => {
        const user = { profile: { preferred_username: 'jdoe' } };
        renderHome({ isAuthenticated: true, isDepartmentAdmin: false, user });
        expect(screen.getByText('Welcome, jdoe')).toBeTruthy();
    });

    it('shows guest name when user has no profile username', () => {
        renderHome({ isAuthenticated: true, isDepartmentAdmin: false, user: { profile: {} } });
        expect(screen.getByText(/Welcome,/)).toBeTruthy();
    });

    it('shows CTA buttons for authenticated non-admin users', () => {
        renderHome({ isAuthenticated: true, isDepartmentAdmin: false });
        expect(screen.getByText('home.hero.cta.documents')).toBeTruthy();
        expect(screen.getByText('home.hero.cta.chat')).toBeTruthy();
    });

    it('does not show CTA buttons for unauthenticated users', () => {
        renderHome({ isAuthenticated: false, isDepartmentAdmin: false });
        expect(screen.queryByText('home.hero.cta.documents')).toBeNull();
    });

    it('does not show CTA buttons for department admin', () => {
        renderHome({ isAuthenticated: true, isDepartmentAdmin: true });
        expect(screen.queryByText('home.hero.cta.documents')).toBeNull();
    });

    it('shows user workflow steps for non-admin', () => {
        renderHome({ isAuthenticated: false, isDepartmentAdmin: false });
        expect(screen.getByText('home.howItWorks.user.step1.title')).toBeTruthy();
        expect(screen.getByText('home.howItWorks.user.step2.title')).toBeTruthy();
        expect(screen.getByText('home.howItWorks.user.step3.title')).toBeTruthy();
    });

    it('shows admin workflow steps for department admin', () => {
        renderHome({ isAuthenticated: true, isDepartmentAdmin: true });
        expect(screen.getByText('home.howItWorks.admin.step1.title')).toBeTruthy();
        expect(screen.getByText('home.howItWorks.admin.step2.title')).toBeTruthy();
        expect(screen.getByText('home.howItWorks.admin.step3.title')).toBeTruthy();
    });

    it('uses profile.name as fallback when preferred_username is missing', () => {
        const user = { profile: { name: 'John Doe' } };
        renderHome({ isAuthenticated: true, isDepartmentAdmin: false, user });
        expect(screen.getByText('Welcome, John Doe')).toBeTruthy();
    });
});
