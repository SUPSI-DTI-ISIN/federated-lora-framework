import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useUpdateDocumentTrainability } from '../useUpdateDocumentTrainability';

function createWrapper(documentsApi: { updateDocumentTrainableApiDataDocumentsTrainabilityDocumentIdPut: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: documentsApi as never, sectionsApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useUpdateDocumentTrainability', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with correct params', async () => {
        const updated = { id: 1, number: 'DOC-001', title: 'Doc', is_trainable: true, sections: [] };
        const documentsApi = { updateDocumentTrainableApiDataDocumentsTrainabilityDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUpdateDocumentTrainability(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isTrainable: true });
        });

        expect(documentsApi.updateDocumentTrainableApiDataDocumentsTrainabilityDocumentIdPut).toHaveBeenCalledWith(1, { is_trainable: true });
    });

    it('updates the document in the cache', async () => {
        const existing = [{ id: 1, number: 'DOC-001', is_trainable: false }, { id: 2, number: 'DOC-002', is_trainable: false }];
        const updated = { id: 1, number: 'DOC-001', is_trainable: true };
        const documentsApi = { updateDocumentTrainableApiDataDocumentsTrainabilityDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { queryClient, wrapper } = createWrapper(documentsApi);
        queryClient.setQueryData(['documents'], existing);

        const { result } = renderHook(() => useUpdateDocumentTrainability(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isTrainable: true });
        });

        const cached = queryClient.getQueryData<typeof existing>(['documents']);
        expect(cached?.[0]).toEqual(updated);
        expect(cached?.[1]).toEqual(existing[1]);
    });

    it('creates a list with the updated document when cache is empty', async () => {
        const updated = { id: 1, number: 'DOC-001', is_trainable: true };
        const documentsApi = { updateDocumentTrainableApiDataDocumentsTrainabilityDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { queryClient, wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUpdateDocumentTrainability(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isTrainable: true });
        });

        expect(queryClient.getQueryData(['documents'])).toEqual([updated]);
    });
});
