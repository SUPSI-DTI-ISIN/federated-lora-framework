import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { createElement } from 'react';
import { RealmsAdminPage } from '../RealmsAdminPage';
import { AuthWrapperContext } from '../../contexts/auth/authWrapperContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string, fallback?: string) => fallback ?? key }),
}));

vi.mock('framer-motion', () => ({
    motion: {
        div: ({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) => <div {...props}>{children}</div>,
    },
    AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock('../../hooks/department/institutes/useGetAllInstitutes', () => ({
    useGetAllInstitutes: vi.fn(),
}));

vi.mock('../../components/realm/RealmList', () => ({
    RealmList: ({ realms }: { realms: unknown[] }) => <div data-testid="realm-list">{realms.length} realms</div>,
}));

vi.mock('../../components/realm/CreateRealmModal', () => ({
    CreateRealmModal: ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) =>
        isOpen ? <div data-testid="create-modal"><button onClick={onClose}>Close</button></div> : null,
}));

vi.mock('../../components/common/SearchBar', () => ({
    SearchBar: ({ value, onChange, placeholder }: { value: string; onChange: (v: string) => void; placeholder: string }) => (
        <input data-testid="search-bar" value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} />
    ),
}));

import { useGetAllInstitutes } from '../../hooks/department/institutes/useGetAllInstitutes';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
    return { ...actual, useNavigate: () => mockNavigate };
});

function renderPage(isDepartmentAdmin: boolean, queryResult: { data?: unknown[]; isLoading: boolean; error?: Error | null }) {
    vi.mocked(useGetAllInstitutes).mockReturnValue(queryResult as never);
    const queryClient = new QueryClient();
    const authValue = { user: null, isAuthenticated: true, isLoading: false, isDepartmentAdmin, login: vi.fn(), logout: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(AuthWrapperContext.Provider, { value: authValue },
                createElement(MemoryRouter, {}, <RealmsAdminPage />)))
    );
}

describe('RealmsAdminPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders loading skeleton when loading', () => {
        renderPage(true, { isLoading: true });
        expect(document.querySelector('.animate-pulse')).toBeTruthy();
    });

    it('renders error state when fetch fails', () => {
        renderPage(true, { isLoading: false, error: new Error('fail'), data: undefined });
        expect(screen.getByText('Errore di caricamento')).toBeTruthy();
    });

    it('renders realm list when data is available', () => {
        const realms = [{ id: 1, name: 'Alpha', url: 'http://alpha.local' }];
        renderPage(true, { isLoading: false, data: realms });
        expect(screen.getByTestId('realm-list')).toBeTruthy();
    });

    it('renders page title', () => {
        renderPage(true, { isLoading: false, data: [] });
        expect(screen.getByText('Istituti')).toBeTruthy();
    });

    it('renders add new institute button', () => {
        renderPage(true, { isLoading: false, data: [] });
        expect(screen.getByText('Nuovo Istituto')).toBeTruthy();
    });

    it('opens create modal when button is clicked', () => {
        renderPage(true, { isLoading: false, data: [] });
        fireEvent.click(screen.getByText('Nuovo Istituto'));
        expect(screen.getByTestId('create-modal')).toBeTruthy();
    });

    it('closes create modal when onClose is called', () => {
        renderPage(true, { isLoading: false, data: [] });
        fireEvent.click(screen.getByText('Nuovo Istituto'));
        fireEvent.click(screen.getByText('Close'));
        expect(screen.queryByTestId('create-modal')).toBeNull();
    });

    it('filters realms by search query', () => {
        const realms = [
            { id: 1, name: 'Alpha', url: 'http://alpha.local' },
            { id: 2, name: 'Beta', url: 'http://beta.local' },
        ];
        renderPage(true, { isLoading: false, data: realms });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: 'alpha' } });
        expect(screen.getByText('1 realms')).toBeTruthy();
    });

    it('shows no results message when search has no matches', () => {
        const realms = [{ id: 1, name: 'Alpha', url: 'http://alpha.local' }];
        renderPage(true, { isLoading: false, data: realms });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: 'zzz' } });
        expect(screen.getByText('Nessun istituto corrisponde alla ricerca.')).toBeTruthy();
    });

    it('navigates to / when user is not department admin', () => {
        renderPage(false, { isLoading: false, data: [] });
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });
});
