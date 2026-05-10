import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { createElement } from 'react';
import { AdaptersPage } from '../AdaptersPage';
import { ModelApiContext } from '../../contexts/api/modelApiContext';
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

vi.mock('../../hooks/useReducedMotion', () => ({
    useReducedMotion: vi.fn().mockReturnValue(false),
}));

vi.mock('../../hooks/institute/model/useGetAllAvailableAdapters', () => ({
    useGetAllAvailableAdapters: vi.fn(),
}));

vi.mock('../../components/adapters/institute/AdaptersList', () => ({
    AdaptersList: ({ adapters }: { adapters: unknown[] }) => (
        <div data-testid="adapters-list">{adapters.length} adapters</div>
    ),
}));

vi.mock('../../components/common/LoadingSkeleton', () => ({
    LoadingSkeleton: () => <div data-testid="loading-skeleton" />,
}));

vi.mock('../../components/common/EmptyState', () => ({
    EmptyState: ({ title }: { title: string }) => <div data-testid="empty-state">{title}</div>,
}));

vi.mock('../../components/common/SearchBar', () => ({
    SearchBar: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
        <input data-testid="search-bar" value={value} onChange={(e) => onChange(e.target.value)} />
    ),
}));

import { useGetAllAvailableAdapters } from '../../hooks/institute/model/useGetAllAvailableAdapters';

function renderPage(queryResult: { data?: unknown; isLoading: boolean; error?: Error | null }) {
    vi.mocked(useGetAllAvailableAdapters).mockReturnValue(queryResult as never);
    const queryClient = new QueryClient();
    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ModelApiContext.Provider, { value: { adaptersApi: {} as never } },
                createElement(MemoryRouter, {}, <AdaptersPage />)))
    );
}

describe('AdaptersPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders loading skeleton when loading', () => {
        renderPage({ isLoading: true });
        expect(screen.getByTestId('loading-skeleton')).toBeTruthy();
    });

    it('renders error alert when fetch fails', () => {
        renderPage({ isLoading: false, error: new Error('fail') });
        expect(screen.getByRole('alert')).toBeTruthy();
        expect(screen.getByText('adapters.errorFetch')).toBeTruthy();
    });

    it('renders page title', () => {
        renderPage({ isLoading: false, data: { adapters: [] } });
        expect(screen.getByText('adapters.title')).toBeTruthy();
    });

    it('renders adapters list when adapters exist', () => {
        const data = { adapters: [{ version: 1, available_local: true }, { version: 2, available_local: false }] };
        renderPage({ isLoading: false, data });
        expect(screen.getByTestId('adapters-list').textContent).toContain('2 adapters');
    });

    it('renders empty state when no adapters', () => {
        renderPage({ isLoading: false, data: { adapters: [] } });
        expect(screen.getByTestId('empty-state')).toBeTruthy();
    });

    it('renders empty state when adapters is null', () => {
        renderPage({ isLoading: false, data: { adapters: null } });
        expect(screen.getByTestId('empty-state')).toBeTruthy();
    });

    it('filters adapters by version search query', () => {
        const data = { adapters: [{ version: 1, available_local: true }, { version: 2, available_local: false }] };
        renderPage({ isLoading: false, data });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: '1' } });
        expect(screen.getByTestId('adapters-list').textContent).toContain('1 adapters');
    });

    it('filters adapters by local only checkbox', () => {
        const data = { adapters: [{ version: 1, available_local: true }, { version: 2, available_local: false }] };
        renderPage({ isLoading: false, data });
        const checkbox = screen.getByRole('checkbox');
        fireEvent.click(checkbox);
        expect(screen.getByTestId('adapters-list').textContent).toContain('1 adapters');
    });

    it('renders local only filter label', () => {
        renderPage({ isLoading: false, data: { adapters: [] } });
        expect(screen.getByText('adapters.filter.localOnly')).toBeTruthy();
    });

    it('renders search bar', () => {
        renderPage({ isLoading: false, data: { adapters: [] } });
        expect(screen.getByTestId('search-bar')).toBeTruthy();
    });
});
