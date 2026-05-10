import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DataApiContext } from '../../../../../contexts/api/dataApiContext';
import { createElement } from 'react';
import { useUpdateSectionContent } from '../useUpdateSectionContent';

function createWrapper(sectionsApi: { updateSectionApiDataSectionsSectionIdPut: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { documentsApi: {} as never, sectionsApi: sectionsApi as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: contextValue }, children)) };
}

describe('useUpdateSectionContent', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with correct params', async () => {
        const updatedSection = { id: 3, title: 'S1', content: 'New content' };
        const sectionsApi = { updateSectionApiDataSectionsSectionIdPut: vi.fn().mockResolvedValue({ data: updatedSection }) };

        const { wrapper } = createWrapper(sectionsApi);
        const { result } = renderHook(() => useUpdateSectionContent(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ sectionId: 3, documentId: 10, updatedContent: 'New content' });
        });

        expect(sectionsApi.updateSectionApiDataSectionsSectionIdPut).toHaveBeenCalledWith(3, { updated_content: 'New content' });
    });

    it('updates the section in the document cache', async () => {
        const doc = {
            id: 10, number: 'DOC-001', title: 'Doc', is_trainable: false,
            sections: [{ id: 3, title: 'S1', content: 'Old' }, { id: 4, title: 'S2', content: 'Other' }],
        };
        const updatedSection = { id: 3, title: 'S1', content: 'New content' };
        const sectionsApi = { updateSectionApiDataSectionsSectionIdPut: vi.fn().mockResolvedValue({ data: updatedSection }) };

        const { queryClient, wrapper } = createWrapper(sectionsApi);
        queryClient.setQueryData(['documents', 10], doc);

        const { result } = renderHook(() => useUpdateSectionContent(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ sectionId: 3, documentId: 10, updatedContent: 'New content' });
        });

        const cached = queryClient.getQueryData<typeof doc>(['documents', 10]);
        expect(cached?.sections[0].content).toBe('New content');
        expect(cached?.sections[1].content).toBe('Other');
    });

    it('does not modify cache when document is not cached', async () => {
        const updatedSection = { id: 3, title: 'S1', content: 'New' };
        const sectionsApi = { updateSectionApiDataSectionsSectionIdPut: vi.fn().mockResolvedValue({ data: updatedSection }) };

        const { queryClient, wrapper } = createWrapper(sectionsApi);
        const { result } = renderHook(() => useUpdateSectionContent(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ sectionId: 3, documentId: 99, updatedContent: 'New' });
        });

        expect(queryClient.getQueryData(['documents', 99])).toBeUndefined();
    });
});
