import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { createElement } from 'react';
import { ChatPage } from '../ChatPage';
import { ChatApiContext } from '../../contexts/api/chatApiContext';
import { AuthWrapperContext } from '../../contexts/auth/authWrapperContext';
import { ApiBasePathContext } from '../../contexts/api/apiBasePathContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string) => key }),
}));

vi.mock('framer-motion', () => ({
    motion: {
        div: ({ children, ...props }: React.HTMLAttributes<HTMLDivElement>) => <div {...props}>{children}</div>,
    },
    AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock('../../utils/envUtils', () => ({
    getModelKey: vi.fn().mockReturnValue('llama-3'),
}));

vi.mock('../../hooks/useReducedMotion', () => ({
    useReducedMotion: vi.fn().mockReturnValue(false),
}));

vi.mock('../../hooks/institute/chat/useChatSse', () => ({
    useChatSse: vi.fn(),
}));

vi.mock('../../hooks/institute/chat/useGetAllChats', () => ({
    useGetAllChats: vi.fn(),
}));

vi.mock('../../hooks/institute/chat/useDeleteChat', () => ({
    useDeleteChat: vi.fn(),
}));

vi.mock('react-hot-toast', () => ({
    default: { success: vi.fn(), error: vi.fn() },
}));

vi.mock('../../components/chat/CreateChatModal', () => ({
    CreateChatModal: ({ isOpen, onClose, onChatCreated }: { isOpen: boolean; onClose: () => void; onChatCreated: (id: number) => void }) =>
        isOpen ? (
            <div data-testid="create-chat-modal">
                <button onClick={onClose}>Close Modal</button>
                <button onClick={() => onChatCreated(99)}>Create Chat</button>
            </div>
        ) : null,
}));

vi.mock('../../components/chat/ChatInterface', () => ({
    ChatInterface: ({ chatId }: { chatId: number }) => <div data-testid="chat-interface">Chat {chatId}</div>,
}));

vi.mock('../../components/chat/EmptyChatState', () => ({
    EmptyChatState: () => <div data-testid="empty-chat-state" />,
}));

vi.mock('../../components/common/DeleteConfirmModal', () => ({
    DeleteConfirmModal: ({ isOpen, onConfirm, onCancel }: { isOpen: boolean; onConfirm: () => void; onCancel: () => void }) =>
        isOpen ? (
            <div data-testid="delete-modal">
                <button onClick={onConfirm}>Confirm Delete</button>
                <button onClick={onCancel}>Cancel Delete</button>
            </div>
        ) : null,
}));

import { useGetAllChats } from '../../hooks/institute/chat/useGetAllChats';
import { useDeleteChat } from '../../hooks/institute/chat/useDeleteChat';

const mockChats = [
    { id: 1, title: 'Chat One', user_id: 'u-1', is_doing_inference: false, created_at: '2024-01-02T00:00:00Z', updated_at: '2024-01-02T00:00:00Z' },
    { id: 2, title: 'Chat Two', user_id: 'u-1', is_doing_inference: true, created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z' },
];

function renderPage(chats = mockChats, isLoading = false) {
    vi.mocked(useGetAllChats).mockReturnValue({ data: chats, isLoading } as never);
    vi.mocked(useDeleteChat).mockReturnValue({ mutateAsync: vi.fn().mockResolvedValue(undefined) } as never);

    const queryClient = new QueryClient();
    const authValue = { user: { profile: { sub: 'u-1' } } as never, isAuthenticated: true, isLoading: false, isDepartmentAdmin: false, login: vi.fn(), logout: vi.fn() };
    const basePathValue = { basePath: 'http://localhost' };
    const chatApiValue = { chatApi: {} as never, messagesApi: {} as never };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(AuthWrapperContext.Provider, { value: authValue },
                createElement(ApiBasePathContext.Provider, { value: basePathValue },
                    createElement(ChatApiContext.Provider, { value: chatApiValue },
                        createElement(MemoryRouter, {}, <ChatPage />)))))
    );
}

describe('ChatPage', () => {
    beforeEach(() => vi.clearAllMocks());

    it('renders the new chat button', () => {
        renderPage();
        expect(screen.getByText('chat.sidebar.newChat')).toBeTruthy();
    });

    it('renders chat list', () => {
        renderPage();
        expect(screen.getByText('Chat One')).toBeTruthy();
        expect(screen.getByText('Chat Two')).toBeTruthy();
    });

    it('renders loading skeletons when loading', () => {
        renderPage([], true);
        expect(document.querySelector('.animate-pulse')).toBeTruthy();
    });

    it('renders empty state message when no chats', () => {
        renderPage([]);
        expect(screen.getByText('chat.sidebar.noChats')).toBeTruthy();
    });

    it('renders empty chat state when no chat is selected', () => {
        renderPage();
        expect(screen.getByTestId('empty-chat-state')).toBeTruthy();
    });

    it('renders chat interface when a chat is selected', () => {
        renderPage();
        fireEvent.click(screen.getByText('Chat One'));
        expect(screen.getByTestId('chat-interface').textContent).toContain('Chat 1');
    });

    it('opens create chat modal when new chat button is clicked', () => {
        renderPage();
        fireEvent.click(screen.getByText('chat.sidebar.newChat'));
        expect(screen.getByTestId('create-chat-modal')).toBeTruthy();
    });

    it('closes create chat modal when onClose is called', () => {
        renderPage();
        fireEvent.click(screen.getByText('chat.sidebar.newChat'));
        fireEvent.click(screen.getByText('Close Modal'));
        expect(screen.queryByTestId('create-chat-modal')).toBeNull();
    });

    it('selects newly created chat', () => {
        renderPage();
        fireEvent.click(screen.getByText('chat.sidebar.newChat'));
        fireEvent.click(screen.getByText('Create Chat'));
        expect(screen.getByTestId('chat-interface').textContent).toContain('Chat 99');
    });

    it('shows delete modal when delete button is clicked', () => {
        renderPage();
        const deleteButtons = document.querySelectorAll('.btn-circle');
        fireEvent.click(deleteButtons[0]);
        expect(screen.getByTestId('delete-modal')).toBeTruthy();
    });

    it('hides delete modal when cancel is clicked', () => {
        renderPage();
        const deleteButtons = document.querySelectorAll('.btn-circle');
        fireEvent.click(deleteButtons[0]);
        fireEvent.click(screen.getByText('Cancel Delete'));
        expect(screen.queryByTestId('delete-modal')).toBeNull();
    });

    it('calls deleteChat on confirm', async () => {
        const mockDelete = vi.fn().mockResolvedValue(undefined);
        vi.mocked(useDeleteChat).mockReturnValue({ mutateAsync: mockDelete } as never);
        vi.mocked(useGetAllChats).mockReturnValue({ data: mockChats, isLoading: false } as never);

        const queryClient = new QueryClient();
        const authValue = { user: { profile: { sub: 'u-1' } } as never, isAuthenticated: true, isLoading: false, isDepartmentAdmin: false, login: vi.fn(), logout: vi.fn() };
        render(
            createElement(QueryClientProvider, { client: queryClient },
                createElement(AuthWrapperContext.Provider, { value: authValue },
                    createElement(ApiBasePathContext.Provider, { value: { basePath: 'http://localhost' } },
                        createElement(ChatApiContext.Provider, { value: { chatApi: {} as never, messagesApi: {} as never } },
                            createElement(MemoryRouter, {}, <ChatPage />)))))
        );

        const deleteButtons = document.querySelectorAll('.btn-circle');
        fireEvent.click(deleteButtons[0]);
        fireEvent.click(screen.getByText('Confirm Delete'));
        await waitFor(() => expect(mockDelete).toHaveBeenCalledOnce());
    });

    it('deselects chat when the selected chat is deleted', async () => {
        const mockDelete = vi.fn().mockResolvedValue(undefined);
        vi.mocked(useDeleteChat).mockReturnValue({ mutateAsync: mockDelete } as never);
        vi.mocked(useGetAllChats).mockReturnValue({ data: mockChats, isLoading: false } as never);

        const queryClient = new QueryClient();
        const authValue = { user: { profile: { sub: 'u-1' } } as never, isAuthenticated: true, isLoading: false, isDepartmentAdmin: false, login: vi.fn(), logout: vi.fn() };
        render(
            createElement(QueryClientProvider, { client: queryClient },
                createElement(AuthWrapperContext.Provider, { value: authValue },
                    createElement(ApiBasePathContext.Provider, { value: { basePath: 'http://localhost' } },
                        createElement(ChatApiContext.Provider, { value: { chatApi: {} as never, messagesApi: {} as never } },
                            createElement(MemoryRouter, {}, <ChatPage />)))))
        );

        fireEvent.click(screen.getByText('Chat One'));
        expect(screen.getByTestId('chat-interface')).toBeTruthy();
        const deleteButtons = document.querySelectorAll('.btn-circle');
        fireEvent.click(deleteButtons[0]);
        fireEvent.click(screen.getByText('Confirm Delete'));
        await waitFor(() => expect(screen.getByTestId('empty-chat-state')).toBeTruthy());
    });

    it('renders model key in footer', () => {
        renderPage();
        expect(screen.getByText('llama-3')).toBeTruthy();
    });

    it('renders inference spinner for chats doing inference', () => {
        renderPage();
        expect(document.querySelector('[aria-label="Inference in progress"]')).toBeTruthy();
    });

    it('sorts chats by created_at descending', () => {
        renderPage();
        const chatItems = screen.getAllByText(/Chat (One|Two)/);
        expect(chatItems[0].textContent).toBe('Chat One');
        expect(chatItems[1].textContent).toBe('Chat Two');
    });
});
