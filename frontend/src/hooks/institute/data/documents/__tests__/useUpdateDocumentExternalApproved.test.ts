import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useUpdateDocumentExternalApproved } from '../useUpdateDocumentExternalApproved';

function createWrapper(documentsApi: { updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: documentsApi as never, sectionsApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useUpdateDocumentExternalApproved', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with correct params', async () => {
        const updated = { id: 1, number: 'DOC-001', title: 'Doc', is_trainable: false, is_externally_approved: true, sections: [] };
        const documentsApi = { updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUpdateDocumentExternalApproved(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isExternallyApproved: true });
        });

        expect(documentsApi.updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut).toHaveBeenCalledWith(1, { is_externally_approved: true });
    });

    it('updates the document in the cache', async () => {
        const existing = [
            { id: 1, number: 'DOC-001', is_externally_approved: false },
            { id: 2, number: 'DOC-002', is_externally_approved: false },
        ];
        const updated = { id: 1, number: 'DOC-001', is_externally_approved: true };
        const documentsApi = { updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { queryClient, wrapper } = createWrapper(documentsApi);
        queryClient.setQueryData(['documents'], existing);

        const { result } = renderHook(() => useUpdateDocumentExternalApproved(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isExternallyApproved: true });
        });

        const cached = queryClient.getQueryData<typeof existing>(['documents']);
        expect(cached?.[0]).toEqual(updated);
        expect(cached?.[1]).toEqual(existing[1]);
    });

    it('creates a list with the updated document when cache is empty', async () => {
        const updated = { id: 1, number: 'DOC-001', is_externally_approved: true };
        const documentsApi = { updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { queryClient, wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUpdateDocumentExternalApproved(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isExternallyApproved: true });
        });

        expect(queryClient.getQueryData(['documents'])).toEqual([updated]);
    });

    it('sets isExternallyApproved to false correctly', async () => {
        const updated = { id: 1, number: 'DOC-001', is_externally_approved: false };
        const documentsApi = { updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut: vi.fn().mockResolvedValue({ data: updated }) };

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUpdateDocumentExternalApproved(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ documentId: 1, isExternallyApproved: false });
        });

        expect(documentsApi.updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut).toHaveBeenCalledWith(1, { is_externally_approved: false });
    });
});
