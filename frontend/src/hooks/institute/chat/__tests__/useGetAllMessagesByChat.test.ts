import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { createElement } from 'react';
import { useGetAllMessagesByChat } from '../useGetAllMessagesByChat';

function createWrapper(messagesApi: { getMessagesApiChatChatsChatIdMessagesGet: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { chatApi: {} as never, messagesApi: messagesApi as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ChatApiContext.Provider, { value: contextValue }, children)) };
}

describe('useGetAllMessagesByChat', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns messages on success', async () => {
        const messages = [{ id: 1, chat_id: 10, role: 'user', content: 'Hello', model_key: 'k', adapter_version: null }];
        const messagesApi = { getMessagesApiChatChatsChatIdMessagesGet: vi.fn().mockResolvedValue({ data: messages }) };

        const { wrapper } = createWrapper(messagesApi);
        const { result } = renderHook(() => useGetAllMessagesByChat(10), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(messages);
    });

    it('calls the API with the correct chatId', async () => {
        const messagesApi = { getMessagesApiChatChatsChatIdMessagesGet: vi.fn().mockResolvedValue({ data: [] }) };

        const { wrapper } = createWrapper(messagesApi);
        const { result } = renderHook(() => useGetAllMessagesByChat(7), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(messagesApi.getMessagesApiChatChatsChatIdMessagesGet).toHaveBeenCalledWith(7);
    });

    it('sets error state on failure', async () => {
        const messagesApi = { getMessagesApiChatChatsChatIdMessagesGet: vi.fn().mockRejectedValue(new Error('fail')) };

        const { wrapper } = createWrapper(messagesApi);
        const { result } = renderHook(() => useGetAllMessagesByChat(1), { wrapper });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
