import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { createElement } from 'react';
import { RealmsPage } from '../RealmsPage';
import { AuthWrapperContext } from '../../contexts/auth/authWrapperContext';
import { SelectorRealmContext } from '../../contexts/realm/selectorRealmContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string, fallback?: string) => fallback ?? key }),
}));

vi.mock('framer-motion', () => ({
    motion: {
        div: ({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) => <div {...props}>{children}</div>,
    },
}));

vi.mock('../../hooks/department/institutes/useGetAllInstitutes', () => ({
    useGetAllInstitutes: vi.fn(),
}));

vi.mock('../../components/realm/RealmList', () => ({
    RealmList: ({ realms }: { realms: unknown[] }) => <div data-testid="realm-list">{realms.length} realms</div>,
}));

import { useGetAllInstitutes } from '../../hooks/department/institutes/useGetAllInstitutes';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
    return { ...actual, useNavigate: () => mockNavigate };
});

function renderPage(auth: { isAuthenticated: boolean }, queryResult: { data?: unknown[]; isLoading: boolean; error?: Error | null }) {
    vi.mocked(useGetAllInstitutes).mockReturnValue(queryResult as never);
    const queryClient = new QueryClient();
    const authValue = { user: null, isAuthenticated: auth.isAuthenticated, isLoading: false, isDepartmentAdmin: false, login: vi.fn(), logout: vi.fn() };
    const realmValue = { realm: undefined, setRealm: vi.fn(), pendingLogin: false, clearPendingLogin: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(AuthWrapperContext.Provider, { value: authValue },
                createElement(SelectorRealmContext.Provider, { value: realmValue },
                    createElement(MemoryRouter, {}, <RealmsPage />))))
    );
}

describe('RealmsPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders loading skeleton when loading', () => {
        renderPage({ isAuthenticated: false }, { isLoading: true });
        expect(document.querySelector('.animate-pulse')).toBeTruthy();
    });

    it('renders error state when fetch fails', () => {
        renderPage({ isAuthenticated: false }, { isLoading: false, error: new Error('fail'), data: undefined });
        expect(screen.getByText('Errore di caricamento')).toBeTruthy();
    });

    it('renders error state when data is undefined', () => {
        renderPage({ isAuthenticated: false }, { isLoading: false, data: undefined });
        expect(screen.getByText('Errore di caricamento')).toBeTruthy();
    });

    it('renders realm list when data is available', () => {
        const realms = [{ id: 1, name: 'Alpha', url: 'http://alpha.local' }];
        renderPage({ isAuthenticated: false }, { isLoading: false, data: realms });
        expect(screen.getByTestId('realm-list')).toBeTruthy();
        expect(screen.getByText('1 realms')).toBeTruthy();
    });

    it('renders page title', () => {
        renderPage({ isAuthenticated: false }, { isLoading: false, data: [] });
        expect(screen.getByText('Istituti')).toBeTruthy();
    });

    it('navigates to / when user is already authenticated', () => {
        renderPage({ isAuthenticated: true }, { isLoading: false, data: [] });
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });

    it('does not navigate when user is not authenticated', () => {
        renderPage({ isAuthenticated: false }, { isLoading: false, data: [] });
        expect(mockNavigate).not.toHaveBeenCalled();
    });
});
