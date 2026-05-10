import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ModelApiContext } from '../../../../contexts/api/modelApiContext';
import { createElement } from 'react';
import { useGetAllAvailableLocalAdapters } from '../useGetAllAvailableLocalAdapters';

function createWrapper(adaptersApi: { getAvailableLocalAdaptersApiModelModelsModelKeyAdaptersLocalGet: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { adaptersApi: adaptersApi as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ModelApiContext.Provider, { value: contextValue }, children)) };
}

describe('useGetAllAvailableLocalAdapters', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns local adapters on success', async () => {
        const data = { model_key: 'llama-3', adapters: [{ version: 1, available_local: true }] };
        const adaptersApi = { getAvailableLocalAdaptersApiModelModelsModelKeyAdaptersLocalGet: vi.fn().mockResolvedValue({ data }) };

        const { wrapper } = createWrapper(adaptersApi);
        const { result } = renderHook(() => useGetAllAvailableLocalAdapters('llama-3'), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(data);
    });

    it('calls the API with the correct modelKey', async () => {
        const adaptersApi = { getAvailableLocalAdaptersApiModelModelsModelKeyAdaptersLocalGet: vi.fn().mockResolvedValue({ data: {} }) };

        const { wrapper } = createWrapper(adaptersApi);
        const { result } = renderHook(() => useGetAllAvailableLocalAdapters('mistral'), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(adaptersApi.getAvailableLocalAdaptersApiModelModelsModelKeyAdaptersLocalGet).toHaveBeenCalledWith('mistral');
    });

    it('sets error state on failure', async () => {
        const adaptersApi = { getAvailableLocalAdaptersApiModelModelsModelKeyAdaptersLocalGet: vi.fn().mockRejectedValue(new Error('fail')) };

        const { wrapper } = createWrapper(adaptersApi);
        const { result } = renderHook(() => useGetAllAvailableLocalAdapters('llama-3'), { wrapper });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
