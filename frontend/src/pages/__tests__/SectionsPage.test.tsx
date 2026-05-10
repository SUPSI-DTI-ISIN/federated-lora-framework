import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { createElement } from 'react';
import { SectionsPage } from '../SectionsPage';
import { DataApiContext } from '../../contexts/api/dataApiContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string, opts?: Record<string, unknown>) => opts ? `${key}:${JSON.stringify(opts)}` : key }),
}));

vi.mock('react-hot-toast', () => ({
    default: { success: vi.fn(), error: vi.fn() },
}));

vi.mock('../../components/sections/SectionsHeader', () => ({
    SectionsHeader: ({ title, number }: { title: string; number: string }) => (
        <div data-testid="sections-header">{title} - {number}</div>
    ),
}));

vi.mock('../../components/sections/SectionsList', () => ({
    SectionsList: ({ sections }: { sections: unknown[] }) => (
        <div data-testid="sections-list">{sections.length} sections</div>
    ),
}));

vi.mock('../../components/sections/DocumentSettingsCard', () => ({
    DocumentSettingsCard: () => <div data-testid="document-settings" />,
}));

vi.mock('../../components/common/DeleteConfirmModal', () => ({
    DeleteConfirmModal: ({ isOpen, onConfirm, onCancel }: { isOpen: boolean; onConfirm: () => void; onCancel: () => void }) =>
        isOpen ? (
            <div data-testid="delete-modal">
                <button onClick={onConfirm}>Confirm</button>
                <button onClick={onCancel}>Cancel</button>
            </div>
        ) : null,
}));

vi.mock('../../hooks/institute/data/documents/useGetDocumentById', () => ({
    useGetDocumentById: vi.fn(),
}));

vi.mock('../../hooks/institute/data/sections/useDeleteSection', () => ({
    useDeleteSection: vi.fn(),
}));

import { useGetDocumentById } from '../../hooks/institute/data/documents/useGetDocumentById';
import { useDeleteSection } from '../../hooks/institute/data/sections/useDeleteSection';

const mockDocument = {
    id: 1,
    number: 'DOC-001',
    title: 'Test Document',
    is_trainable: false,
    sections: [
        { id: 10, title: 'Section 1', content: 'Content 1' },
        { id: 11, title: 'Section 2', content: 'Content 2' },
    ],
};

function renderPage(documentId = '1') {
    const queryClient = new QueryClient();
    const sectionsApi = {} as never;
    const documentsApi = {} as never;

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(DataApiContext.Provider, { value: { documentsApi, sectionsApi } },
                createElement(MemoryRouter, { initialEntries: [`/documents/${documentId}/sections`] },
                    createElement(Routes, {},
                        createElement(Route, { path: '/documents/:documentId/sections', element: <SectionsPage /> })))))
    );
}

describe('SectionsPage', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(useDeleteSection).mockReturnValue({ mutateAsync: vi.fn().mockResolvedValue(undefined) } as never);
    });

    it('renders loading state', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: true, data: undefined, error: null } as never);
        renderPage();
        expect(document.querySelector('.animate-pulse')).toBeTruthy();
    });

    it('renders error state when fetch fails', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: undefined, error: new Error('fail') } as never);
        renderPage();
        expect(screen.getByText('sections.error.title')).toBeTruthy();
    });

    it('renders error state when document is undefined', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: undefined, error: null } as never);
        renderPage();
        expect(screen.getByText('sections.error.title')).toBeTruthy();
    });

    it('renders document title and number', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        expect(screen.getByTestId('sections-header').textContent).toContain('Test Document - DOC-001');
    });

    it('renders sections list', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        expect(screen.getByTestId('sections-list').textContent).toContain('2 sections');
    });

    it('renders document settings card', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        expect(screen.getByTestId('document-settings')).toBeTruthy();
    });

    it('renders select all checkbox when sections exist', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        expect(screen.getByText('sections.selection.selectAll')).toBeTruthy();
    });

    it('selects all sections when select all is clicked', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        const checkbox = screen.getByRole('checkbox');
        fireEvent.click(checkbox);
        expect(screen.getByText(/sections.selection.deleteSelected/)).toBeTruthy();
    });

    it('deselects all when select all is clicked again', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        const checkbox = screen.getByRole('checkbox');
        fireEvent.click(checkbox);
        fireEvent.click(checkbox);
        expect(screen.queryByText(/sections.selection.deleteSelected/)).toBeNull();
    });

    it('shows delete modal when delete selected is clicked', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        fireEvent.click(screen.getByRole('checkbox'));
        fireEvent.click(screen.getByText(/sections.selection.deleteSelected/));
        expect(screen.getByTestId('delete-modal')).toBeTruthy();
    });

    it('hides delete modal when cancel is clicked', () => {
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);
        renderPage();
        fireEvent.click(screen.getByRole('checkbox'));
        fireEvent.click(screen.getByText(/sections.selection.deleteSelected/));
        fireEvent.click(screen.getByText('Cancel'));
        expect(screen.queryByTestId('delete-modal')).toBeNull();
    });

    it('calls deleteSection for each selected section on confirm', async () => {
        const mockDelete = vi.fn().mockResolvedValue(undefined);
        vi.mocked(useDeleteSection).mockReturnValue({ mutateAsync: mockDelete } as never);
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: mockDocument, error: null } as never);

        renderPage();
        fireEvent.click(screen.getByRole('checkbox'));
        fireEvent.click(screen.getByText(/sections.selection.deleteSelected/));
        fireEvent.click(screen.getByText('Confirm'));

        await waitFor(() => {
            expect(mockDelete).toHaveBeenCalledTimes(2);
        });
    });

    it('does not render selection controls when document has no sections', () => {
        const emptyDoc = { ...mockDocument, sections: [] };
        vi.mocked(useGetDocumentById).mockReturnValue({ isLoading: false, data: emptyDoc, error: null } as never);
        renderPage();
        expect(screen.queryByText('sections.selection.selectAll')).toBeNull();
    });
});
