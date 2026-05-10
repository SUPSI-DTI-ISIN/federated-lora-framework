import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useDeleteSection } from '../useDeleteSection';

function createWrapper(sectionsApi: { deleteSectionByIdApiDataSectionsSectionIdDelete: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: {} as never, sectionsApi: sectionsApi as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useDeleteSection', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with the correct sectionId', async () => {
        const sectionsApi = { deleteSectionByIdApiDataSectionsSectionIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { wrapper } = createWrapper(sectionsApi);
        const { result } = renderHook(() => useDeleteSection(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ sectionId: 3, documentId: 10 });
        });

        expect(sectionsApi.deleteSectionByIdApiDataSectionsSectionIdDelete).toHaveBeenCalledWith(3);
    });

    it('removes the section from the document cache', async () => {
        const doc = { id: 10, number: 'DOC-001', title: 'Doc', is_trainable: false, sections: [{ id: 3, title: 'S1', content: 'C' }, { id: 4, title: 'S2', content: 'C' }] };
        const sectionsApi = { deleteSectionByIdApiDataSectionsSectionIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { queryClient, wrapper } = createWrapper(sectionsApi);
        queryClient.setQueryData(['documents', 10], doc);

        const { result } = renderHook(() => useDeleteSection(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ sectionId: 3, documentId: 10 });
        });

        const cached = queryClient.getQueryData<typeof doc>(['documents', 10]);
        expect(cached?.sections).toHaveLength(1);
        expect(cached?.sections[0].id).toBe(4);
    });

    it('does not modify cache when document is not cached', async () => {
        const sectionsApi = { deleteSectionByIdApiDataSectionsSectionIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { queryClient, wrapper } = createWrapper(sectionsApi);
        const { result } = renderHook(() => useDeleteSection(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ sectionId: 3, documentId: 99 });
        });

        expect(queryClient.getQueryData(['documents', 99])).toBeUndefined();
    });
});
