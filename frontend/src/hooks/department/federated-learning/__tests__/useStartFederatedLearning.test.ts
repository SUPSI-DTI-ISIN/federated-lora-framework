import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useStartFederatedLearning } from '../useStartFederatedLearning';

vi.mock('../../../../config/federatedLearningManagementServiceClient', () => ({
    federatedLearningJobsApi: {
        startFederatedLearningApiFederatedLearningManagementJobsPost: vi.fn(),
    },
}));

import { federatedLearningJobsApi } from '../../../../config/federatedLearningManagementServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children) };
}

describe('useStartFederatedLearning', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API on mutate', async () => {
        const newJob = { id: 1, celery_task_id: 'task-1', status: 'IN_PROGRESS' };
        vi.mocked(federatedLearningJobsApi.startFederatedLearningApiFederatedLearningManagementJobsPost).mockResolvedValue({ data: newJob } as never);

        const { wrapper } = createWrapper();
        const { result } = renderHook(() => useStartFederatedLearning(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync();
        });

        expect(federatedLearningJobsApi.startFederatedLearningApiFederatedLearningManagementJobsPost).toHaveBeenCalledOnce();
    });

    it('appends the new job to the cache on success', async () => {
        const existing = [{ id: 1, celery_task_id: 'task-0', status: 'SUCCESS' }];
        const newJob = { id: 2, celery_task_id: 'task-1', status: 'IN_PROGRESS' };
        vi.mocked(federatedLearningJobsApi.startFederatedLearningApiFederatedLearningManagementJobsPost).mockResolvedValue({ data: newJob } as never);

        const { queryClient, wrapper } = createWrapper();
        queryClient.setQueryData(['federated-learning-jobs'], existing);

        const { result } = renderHook(() => useStartFederatedLearning(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync();
        });

        const cached = queryClient.getQueryData<typeof existing>(['federated-learning-jobs']);
        expect(cached).toHaveLength(2);
        expect(cached?.[1]).toEqual(newJob);
    });

    it('creates a new list when cache is empty', async () => {
        const newJob = { id: 1, celery_task_id: 'task-1', status: 'IN_PROGRESS' };
        vi.mocked(federatedLearningJobsApi.startFederatedLearningApiFederatedLearningManagementJobsPost).mockResolvedValue({ data: newJob } as never);

        const { queryClient, wrapper } = createWrapper();
        const { result } = renderHook(() => useStartFederatedLearning(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync();
        });

        expect(queryClient.getQueryData(['federated-learning-jobs'])).toEqual([newJob]);
    });
});
