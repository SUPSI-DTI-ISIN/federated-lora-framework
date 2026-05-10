import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { createElement } from 'react';
import { FederatedLearningJobsPage } from '../FederatedLearningJobsPage';
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

vi.mock('../../hooks/department/federated-learning/useGetAllFederatedLearningJobs', () => ({
    useGetAllFederatedLearningJobs: vi.fn(),
}));

vi.mock('../../hooks/department/federated-learning/useFederatedLearningJobSse', () => ({
    useFederatedLearningJobSse: vi.fn(),
}));

vi.mock('../../components/common/LoadingSkeleton', () => ({
    LoadingSkeleton: () => <div data-testid="loading-skeleton" />,
}));

vi.mock('../../components/federated-learning/FederatedLearningActions', () => ({
    FederatedLearningActions: () => <div data-testid="fl-actions" />,
}));

vi.mock('../../components/federated-learning/institute-participation/InstituteTrainingParticipationCard', () => ({
    InstituteTrainingParticipationCard: () => <div data-testid="participation-card" />,
}));

vi.mock('../../components/federated-learning/job/FederatedLearningJobsCard', () => ({
    FederatedLearningJobsCard: ({ jobs, searchQuery }: { jobs: unknown[]; searchQuery: string }) => (
        <div data-testid="jobs-card" data-count={jobs.length} data-query={searchQuery}>
            {jobs.length} jobs
        </div>
    ),
}));

vi.mock('../../components/common/SearchBar', () => ({
    SearchBar: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
        <input data-testid="search-bar" value={value} onChange={(e) => onChange(e.target.value)} />
    ),
}));

import { useGetAllFederatedLearningJobs } from '../../hooks/department/federated-learning/useGetAllFederatedLearningJobs';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
    return { ...actual, useNavigate: () => mockNavigate };
});

const mockJobs = [
    { id: 1, celery_task_id: 'task-abc-123', status: 'SUCCESS' },
    { id: 2, celery_task_id: 'task-def-456', status: 'IN_PROGRESS' },
];

function renderPage(isDepartmentAdmin: boolean, queryResult: { data?: unknown; isLoading: boolean; error?: Error | null }) {
    vi.mocked(useGetAllFederatedLearningJobs).mockReturnValue(queryResult as never);
    const queryClient = new QueryClient();
    const authValue = { user: null, isAuthenticated: true, isLoading: false, isDepartmentAdmin, login: vi.fn(), logout: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(AuthWrapperContext.Provider, { value: authValue },
                createElement(MemoryRouter, {}, <FederatedLearningJobsPage />)))
    );
}

describe('FederatedLearningJobsPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders loading skeleton when loading', () => {
        renderPage(true, { isLoading: true });
        expect(screen.getByTestId('loading-skeleton')).toBeTruthy();
    });

    it('renders error state when fetch fails', () => {
        renderPage(true, { isLoading: false, error: new Error('fail') });
        expect(screen.getByText('federatedLearning.errorFetch')).toBeTruthy();
    });

    it('renders page title', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        expect(screen.getByText('federatedLearning.title')).toBeTruthy();
    });

    it('renders federated learning actions', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        expect(screen.getByTestId('fl-actions')).toBeTruthy();
    });

    it('renders participation card', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        expect(screen.getByTestId('participation-card')).toBeTruthy();
    });

    it('renders jobs card with all jobs', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        expect(screen.getByTestId('jobs-card').textContent).toContain('2 jobs');
    });

    it('renders search bar', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        expect(screen.getByTestId('search-bar')).toBeTruthy();
    });

    it('filters jobs by celery_task_id', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: 'abc' } });
        expect(screen.getByTestId('jobs-card').textContent).toContain('1 jobs');
    });

    it('filters jobs by id', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: 'task-abc' } });
        expect(screen.getByTestId('jobs-card').textContent).toContain('1 jobs');
    });

    it('shows all jobs when search is empty', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        expect(screen.getByTestId('jobs-card').textContent).toContain('2 jobs');
    });

    it('handles null jobs gracefully', () => {
        renderPage(true, { isLoading: false, data: null });
        expect(screen.getByTestId('jobs-card').textContent).toContain('0 jobs');
    });

    it('navigates to / when user is not department admin', () => {
        renderPage(false, { isLoading: false, data: mockJobs });
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });

    it('passes search query to jobs card', () => {
        renderPage(true, { isLoading: false, data: mockJobs });
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: 'test' } });
        expect(screen.getByTestId('jobs-card').getAttribute('data-query')).toBe('test');
    });
});
