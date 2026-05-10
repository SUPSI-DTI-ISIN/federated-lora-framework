import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useGetAllDepartmentAdapters } from '../useGetAllDepartmentAdapters';

vi.mock('../../../../config/mlflowServiceClient', () => ({
    departmentAdaptersApi: {
        getAdaptersVersionApiMlflowModelModelKeyAdaptersGet: vi.fn(),
    },
}));

import { departmentAdaptersApi } from '../../../../config/mlflowServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useGetAllDepartmentAdapters', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns adapters on success', async () => {
        const data = { model_key: 'llama-3', adapters_version: [1, 2] };
        vi.mocked(departmentAdaptersApi.getAdaptersVersionApiMlflowModelModelKeyAdaptersGet).mockResolvedValue({ data } as never);

        const { result } = renderHook(() => useGetAllDepartmentAdapters('llama-3'), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(data);
    });

    it('calls the API with the correct modelKey', async () => {
        vi.mocked(departmentAdaptersApi.getAdaptersVersionApiMlflowModelModelKeyAdaptersGet).mockResolvedValue({ data: {} } as never);

        const { result } = renderHook(() => useGetAllDepartmentAdapters('mistral'), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(departmentAdaptersApi.getAdaptersVersionApiMlflowModelModelKeyAdaptersGet).toHaveBeenCalledWith('mistral');
    });

    it('sets error state on failure', async () => {
        vi.mocked(departmentAdaptersApi.getAdaptersVersionApiMlflowModelModelKeyAdaptersGet).mockRejectedValue(new Error('fail'));

        const { result } = renderHook(() => useGetAllDepartmentAdapters('llama-3'), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
