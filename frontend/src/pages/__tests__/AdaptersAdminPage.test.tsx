import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { createElement } from 'react';
import { AdaptersAdminPage } from '../AdaptersAdminPage';
import { AuthWrapperContext } from '../../contexts/auth/authWrapperContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string) => key }),
}));

vi.mock('framer-motion', () => ({
    motion: {
        div: ({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) => <div {...props}>{children}</div>,
    },
}));

vi.mock('../../utils/envUtils', () => ({
    getModelKey: vi.fn().mockReturnValue('llama-3'),
}));

vi.mock('../../hooks/department/mlflow/useGetAllDepartmentAdapters', () => ({
    useGetAllDepartmentAdapters: vi.fn(),
}));

vi.mock('../../hooks/department/federated-learning/useFederatedLearningJobSse', () => ({
    useFederatedLearningJobSse: vi.fn(),
}));

vi.mock('../../components/adapters/department/DepartmentAdaptersList', () => ({
    DepartmentAdaptersList: ({ adapters }: { adapters: unknown[] }) => (
        <div data-testid="dept-adapters-list">{adapters.length} adapters</div>
    ),
}));

vi.mock('../../components/common/LoadingSkeleton', () => ({
    LoadingSkeleton: () => <div data-testid="loading-skeleton" />,
}));

vi.mock('../../components/common/SearchBar', () => ({
    SearchBar: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
        <input data-testid="search-bar" value={value} onChange={(e) => onChange(e.target.value)} />
    ),
}));

import { useGetAllDepartmentAdapters } from '../../hooks/department/mlflow/useGetAllDepartmentAdapters';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
    return { ...actual, useNavigate: () => mockNavigate };
});

function renderPage(isDepartmentAdmin: boolean, queryResult: { data?: unknown; isLoading: boolean; error?: Error | null }) {
    vi.mocked(useGetAllDepartmentAdapters).mockReturnValue(queryResult as never);
    const queryClient = new QueryClient();
    const authValue = { user: null, isAuthenticated: true, isLoading: false, isDepartmentAdmin, login: vi.fn(), logout: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(AuthWrapperContext.Provider, { value: authValue },
                createElement(MemoryRouter, {}, <AdaptersAdminPage />)))
    );
}

describe('AdaptersAdminPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders loading skeleton when loading', () => {
        renderPage(true, { isLoading: true });
        expect(screen.getByTestId('loading-skeleton')).toBeTruthy();
    });

    it('renders error state when fetch fails', () => {
        renderPage(true, { isLoading: false, error: new Error('fail') });
        expect(screen.getByText('adapters.errorFetch')).toBeTruthy();
    });

    it('renders page title', () => {
        renderPage(true, { isLoading: false, data: { adapters_version: [] } });
        expect(screen.getByText('adapters.title')).toBeTruthy();
    });

    it('renders adapters list', () => {
        renderPage(true, { isLoading: false, data: { adapters_version: [1, 2, 3] } });
        expect(screen.getByTestId('dept-adapters-list').textContent).toContain('3 adapters');
    });

    it('renders empty adapters list when null', () => {
        renderPage(true, { isLoading: false, data: { adapters_version: null } });
        expect(screen.getByTestId('dept-adapters-list').textContent).toContain('0 adapters');
    });

    it('filters adapters by search query', () => {
        renderPage(true, { isLoading: false, data: { adapters_version: [1, 2, 12] } });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: '1' } });
        expect(screen.getByTestId('dept-adapters-list').textContent).toContain('2 adapters');
    });

    it('navigates to / when user is not department admin', () => {
        renderPage(false, { isLoading: false, data: { adapters_version: [] } });
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });

    it('renders search bar', () => {
        renderPage(true, { isLoading: false, data: { adapters_version: [] } });
        expect(screen.getByTestId('search-bar')).toBeTruthy();
    });
});
