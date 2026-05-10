import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useGetAllFederatedLearningJobs } from '../useGetAllFederatedLearningJobs';

vi.mock('../../../../config/federatedLearningManagementServiceClient', () => ({
    federatedLearningJobsApi: {
        getAllFederatedLearningJobApiFederatedLearningManagementJobsGet: vi.fn(),
    },
}));

import { federatedLearningJobsApi } from '../../../../config/federatedLearningManagementServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useGetAllFederatedLearningJobs', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns jobs on success', async () => {
        const jobs = [{ id: 1, celery_task_id: 'task-1', status: 'SUCCESS' }];
        vi.mocked(federatedLearningJobsApi.getAllFederatedLearningJobApiFederatedLearningManagementJobsGet).mockResolvedValue({ data: jobs } as never);

        const { result } = renderHook(() => useGetAllFederatedLearningJobs(), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(jobs);
    });

    it('sets error state on failure', async () => {
        vi.mocked(federatedLearningJobsApi.getAllFederatedLearningJobApiFederatedLearningManagementJobsGet).mockRejectedValue(new Error('fail'));

        const { result } = renderHook(() => useGetAllFederatedLearningJobs(), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
