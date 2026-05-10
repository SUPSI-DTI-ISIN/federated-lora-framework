import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useDeleteDepartmentAdapters } from '../useDeleteDepartmentAdapters';

vi.mock('../../../../config/mlflowServiceClient', () => ({
    departmentAdaptersApi: {
        deleteAdapterVersionApiMlflowModelModelKeyAdaptersAdapterVersionDelete: vi.fn(),
    },
}));

import { departmentAdaptersApi } from '../../../../config/mlflowServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children) };
}

describe('useDeleteDepartmentAdapters', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with modelKey and adapterVersion', async () => {
        vi.mocked(departmentAdaptersApi.deleteAdapterVersionApiMlflowModelModelKeyAdaptersAdapterVersionDelete).mockResolvedValue({ data: undefined } as never);

        const { wrapper } = createWrapper();
        const { result } = renderHook(() => useDeleteDepartmentAdapters(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ modelKey: 'llama-3', adapterVersion: 2 });
        });

        expect(departmentAdaptersApi.deleteAdapterVersionApiMlflowModelModelKeyAdaptersAdapterVersionDelete).toHaveBeenCalledWith('llama-3', 2);
    });

    it('invalidates department-adapters query on success', async () => {
        vi.mocked(departmentAdaptersApi.deleteAdapterVersionApiMlflowModelModelKeyAdaptersAdapterVersionDelete).mockResolvedValue({ data: undefined } as never);

        const { queryClient, wrapper } = createWrapper();
        const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');

        const { result } = renderHook(() => useDeleteDepartmentAdapters(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ modelKey: 'llama-3', adapterVersion: 1 });
        });

        expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['department-adapters'] });
    });
});
