import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useDeleteDocument } from '../useDeleteDocument';

function createWrapper(documentsApi: { deleteByIdApiDataDocumentsDocumentIdDelete: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: documentsApi as never, sectionsApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useDeleteDocument', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with the correct documentId', async () => {
        const documentsApi = { deleteByIdApiDataDocumentsDocumentIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useDeleteDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        expect(documentsApi.deleteByIdApiDataDocumentsDocumentIdDelete).toHaveBeenCalledWith(1);
    });

    it('removes the deleted document from the cache', async () => {
        const docs = [{ id: 1, number: 'DOC-001' }, { id: 2, number: 'DOC-002' }];
        const documentsApi = { deleteByIdApiDataDocumentsDocumentIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { queryClient, wrapper } = createWrapper(documentsApi);
        queryClient.setQueryData(['documents'], docs);

        const { result } = renderHook(() => useDeleteDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        const cached = queryClient.getQueryData<typeof docs>(['documents']);
        expect(cached).toHaveLength(1);
        expect(cached?.[0].id).toBe(2);
    });

    it('returns undefined when cache is empty', async () => {
        const documentsApi = { deleteByIdApiDataDocumentsDocumentIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { queryClient, wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useDeleteDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        expect(queryClient.getQueryData(['documents'])).toBeUndefined();
    });
});
