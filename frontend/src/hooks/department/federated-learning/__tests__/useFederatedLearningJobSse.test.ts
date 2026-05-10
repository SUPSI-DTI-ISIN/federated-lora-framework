import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useFederatedLearningJobSse } from '../useFederatedLearningJobSse';

vi.mock('../../../../utils/sse/sseUrls', () => ({
    getFederatedLearningJobSseUrl: vi.fn().mockReturnValue('/api_federated_learning_management/jobs/sse'),
}));

const mockEventSource = {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    close: vi.fn(),
    onerror: null as ((e: Event) => void) | null,
};

function getHandler(eventName: string): (e: MessageEvent) => void {
    const call = (mockEventSource.addEventListener.mock.calls as Array<[string, (e: MessageEvent) => void]>)
        .find(([event]) => event === eventName);
    return call![1];
}

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children) };
}

describe('useFederatedLearningJobSse', () => {
    let MockEventSource: ReturnType<typeof vi.fn>;

    beforeEach(() => {
        vi.clearAllMocks();
        MockEventSource = vi.fn().mockImplementation(function (this: typeof mockEventSource) {
            Object.assign(this, mockEventSource);
            return this;
        });
        vi.stubGlobal('EventSource', MockEventSource);
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    it('creates an EventSource on mount', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useFederatedLearningJobSse(), { wrapper });
        expect(MockEventSource).toHaveBeenCalledWith('/api_federated_learning_management/jobs/sse');
    });

    it('registers a federated_learning_job_update event listener', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useFederatedLearningJobSse(), { wrapper });
        expect(mockEventSource.addEventListener).toHaveBeenCalledWith(
            'federated_learning_job_update',
            expect.any(Function)
        );
    });

    it('closes the EventSource on unmount', () => {
        const { wrapper } = createWrapper();
        const { unmount } = renderHook(() => useFederatedLearningJobSse(), { wrapper });
        unmount();
        expect(mockEventSource.close).toHaveBeenCalledOnce();
    });

    it('updates job status in cache when event fires', () => {
        const { queryClient, wrapper } = createWrapper();
        const jobs = [{ id: 1, celery_task_id: 'task-1', status: 'IN_PROGRESS' }];
        queryClient.setQueryData(['federated-learning-jobs'], jobs);

        renderHook(() => useFederatedLearningJobSse(), { wrapper });

        getHandler('federated_learning_job_update')(
            { data: JSON.stringify({ job_id: 'task-1', result_type: 'SUCCESS' }) } as MessageEvent
        );

        const cached = queryClient.getQueryData<typeof jobs>(['federated-learning-jobs']);
        expect(cached?.[0].status).toBe('SUCCESS');
    });

    it('does not crash when cache is empty', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useFederatedLearningJobSse(), { wrapper });

        expect(() =>
            getHandler('federated_learning_job_update')(
                { data: JSON.stringify({ job_id: 'task-1', result_type: 'SUCCESS' }) } as MessageEvent
            )
        ).not.toThrow();
    });

    it('does not crash on invalid JSON payload', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useFederatedLearningJobSse(), { wrapper });

        expect(() =>
            getHandler('federated_learning_job_update')({ data: 'not-valid-json' } as MessageEvent)
        ).not.toThrow();
    });

    it('triggers onerror handler without crashing', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useFederatedLearningJobSse(), { wrapper });

        const instance = MockEventSource.mock.instances[0] as typeof mockEventSource;
        expect(() => instance.onerror?.(new Event('error'))).not.toThrow();
    });

    it('invalidates department-adapters on job update', () => {
        const { queryClient, wrapper } = createWrapper();
        const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');

        renderHook(() => useFederatedLearningJobSse(), { wrapper });

        getHandler('federated_learning_job_update')(
            { data: JSON.stringify({ job_id: 'task-1', result_type: 'SUCCESS' }) } as MessageEvent
        );

        expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['department-adapters'] });
    });
});
