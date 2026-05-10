import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useUploadDocument } from '../useUploadDocument';

function createWrapper(documentsApi: { uploadApiDataDocumentsUploadPost: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: documentsApi as never, sectionsApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useUploadDocument', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with isExternallyApproved and file', async () => {
        const uploaded = { id: 1, number: 'DOC-001', title: 'Doc', is_trainable: false, sections: [] };
        const documentsApi = { uploadApiDataDocumentsUploadPost: vi.fn().mockResolvedValue({ data: uploaded }) };
        const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUploadDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ file, isExternallyApproved: false });
        });

        expect(documentsApi.uploadApiDataDocumentsUploadPost).toHaveBeenCalledWith(false, file);
    });

    it('passes isExternallyApproved true correctly', async () => {
        const uploaded = { id: 1, number: 'DOC-001', title: 'Doc', is_trainable: false, sections: [] };
        const documentsApi = { uploadApiDataDocumentsUploadPost: vi.fn().mockResolvedValue({ data: uploaded }) };
        const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });

        const { wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUploadDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ file, isExternallyApproved: true });
        });

        expect(documentsApi.uploadApiDataDocumentsUploadPost).toHaveBeenCalledWith(true, file);
    });

    it('appends the uploaded document to the cache', async () => {
        const existing = [{ id: 1, number: 'DOC-001', title: 'Old', is_trainable: false, sections: [] }];
        const uploaded = { id: 2, number: 'DOC-002', title: 'New', is_trainable: false, sections: [] };
        const documentsApi = { uploadApiDataDocumentsUploadPost: vi.fn().mockResolvedValue({ data: uploaded }) };
        const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });

        const { queryClient, wrapper } = createWrapper(documentsApi);
        queryClient.setQueryData(['documents'], existing);

        const { result } = renderHook(() => useUploadDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ file, isExternallyApproved: false });
        });

        const cached = queryClient.getQueryData<typeof existing>(['documents']);
        expect(cached).toHaveLength(2);
        expect(cached?.[1]).toEqual(uploaded);
    });

    it('creates a new list when cache is empty', async () => {
        const uploaded = { id: 1, number: 'DOC-001', title: 'Doc', is_trainable: false, sections: [] };
        const documentsApi = { uploadApiDataDocumentsUploadPost: vi.fn().mockResolvedValue({ data: uploaded }) };
        const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });

        const { queryClient, wrapper } = createWrapper(documentsApi);
        const { result } = renderHook(() => useUploadDocument(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ file, isExternallyApproved: false });
        });

        expect(queryClient.getQueryData(['documents'])).toEqual([uploaded]);
    });
});
