import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useGetDocumentById } from '../useGetDocumentById';

function createWrapper(documentsApi: { getByIdApiDataDocumentsDocumentIdGet: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: documentsApi as never, sectionsApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useGetDocumentById', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns document on success', async () => {
        const doc = { id: 5, number: 'DOC-005', title: 'Doc', is_trainable: false, sections: [] };
        const documentsApi = { getByIdApiDataDocumentsDocumentIdGet: vi.fn().mockResolvedValue({ data: doc }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useGetDocumentById(5), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(doc);
    });

    it('calls the API with the correct documentId', async () => {
        const documentsApi = { getByIdApiDataDocumentsDocumentIdGet: vi.fn().mockResolvedValue({ data: {} }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useGetDocumentById(42), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(documentsApi.getByIdApiDataDocumentsDocumentIdGet).toHaveBeenCalledWith(42);
    });

    it('sets error state on failure', async () => {
        const documentsApi = { getByIdApiDataDocumentsDocumentIdGet: vi.fn().mockRejectedValue(new Error('fail')) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useGetDocumentById(1), { wrapper });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
