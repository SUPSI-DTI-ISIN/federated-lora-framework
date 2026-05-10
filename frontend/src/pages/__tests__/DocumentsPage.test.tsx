import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { DocumentsPage } from '../DocumentsPage';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string) => key }),
}));

vi.mock('framer-motion', () => ({
    motion: {
        div: ({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) => <div {...props}>{children}</div>,
    },
    AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock('../../components/common/PageHeader', () => ({
    PageHeader: ({ title, subtitle, action }: { title: string; subtitle: string; action?: { label: string; onClick: () => void } }) => (
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
            {action && <button onClick={action.onClick}>{action.label}</button>}
        </div>
    ),
}));

vi.mock('../../components/documents/DocumentList', () => ({
    DocumentList: ({ searchQuery }: { searchQuery: string }) => (
        <div data-testid="document-list" data-query={searchQuery}>Document List</div>
    ),
}));

vi.mock('../../components/documents/DocumentUpload', () => ({
    DocumentUpload: ({ onClose }: { onClose: (id?: number) => void }) => (
        <div data-testid="document-upload">
            <button onClick={() => onClose()}>Close Upload</button>
            <button onClick={() => onClose(42)}>Close With ID</button>
        </div>
    ),
}));

vi.mock('../../components/common/SearchBar', () => ({
    SearchBar: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
        <input data-testid="search-bar" value={value} onChange={(e) => onChange(e.target.value)} />
    ),
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
    return { ...actual, useNavigate: () => mockNavigate };
});

function renderPage() {
    return render(<MemoryRouter><DocumentsPage /></MemoryRouter>);
}

describe('DocumentsPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders the page title', () => {
        renderPage();
        expect(screen.getByText('documents.title')).toBeTruthy();
    });

    it('renders the document list', () => {
        renderPage();
        expect(screen.getByTestId('document-list')).toBeTruthy();
    });

    it('renders the search bar', () => {
        renderPage();
        expect(screen.getByTestId('search-bar')).toBeTruthy();
    });

    it('does not show upload modal initially', () => {
        renderPage();
        expect(screen.queryByTestId('document-upload')).toBeNull();
    });

    it('shows upload modal when upload button is clicked', () => {
        renderPage();
        fireEvent.click(screen.getByText('documents.uploadButton'));
        expect(screen.getByTestId('document-upload')).toBeTruthy();
    });

    it('hides upload modal when onClose is called without id', () => {
        renderPage();
        fireEvent.click(screen.getByText('documents.uploadButton'));
        fireEvent.click(screen.getByText('Close Upload'));
        expect(screen.queryByTestId('document-upload')).toBeNull();
    });

    it('navigates to sections page when onClose is called with document id', () => {
        renderPage();
        fireEvent.click(screen.getByText('documents.uploadButton'));
        fireEvent.click(screen.getByText('Close With ID'));
        expect(mockNavigate).toHaveBeenCalledWith('/documents/42/sections');
    });

    it('passes search query to document list', () => {
        renderPage();
        fireEvent.change(screen.getByTestId('search-bar'), { target: { value: 'test query' } });
        expect(screen.getByTestId('document-list').getAttribute('data-query')).toBe('test query');
    });
});
