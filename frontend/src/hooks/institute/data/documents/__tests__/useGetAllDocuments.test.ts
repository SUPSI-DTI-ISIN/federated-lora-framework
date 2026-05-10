import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useGetAllDocuments } from '../useGetAllDocuments';

function createWrapper(documentsApi: { getAllApiDataDocumentsGet: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: documentsApi as never, sectionsApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useGetAllDocuments', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns documents on success', async () => {
        const docs = [{ id: 1, number: 'DOC-001', title: 'Doc', is_trainable: false, sections: [] }];
        const documentsApi = { getAllApiDataDocumentsGet: vi.fn().mockResolvedValue({ data: docs }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useGetAllDocuments(), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(docs);
    });

    it('sets error state on failure', async () => {
        const documentsApi = { getAllApiDataDocumentsGet: vi.fn().mockRejectedValue(new Error('fail')) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useGetAllDocuments(), { wrapper });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
