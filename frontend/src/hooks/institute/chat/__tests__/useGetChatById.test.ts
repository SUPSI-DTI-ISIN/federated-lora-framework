import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { createElement } from 'react';
import { useGetChatById } from '../useGetChatById';

function createWrapper(chatApi: { getChatByIdApiChatChatsChatIdGet: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { chatApi: chatApi as never, messagesApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ChatApiContext.Provider, { value: contextValue }, children)) };
}

describe('useGetChatById', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns chat on success', async () => {
        const chat = { id: 5, title: 'My Chat', user_id: 'u-1', is_doing_inference: false };
        const chatApi = { getChatByIdApiChatChatsChatIdGet: vi.fn().mockResolvedValue({ data: chat }) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useGetChatById(5), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(chat);
    });

    it('calls the API with the correct chatId', async () => {
        const chatApi = { getChatByIdApiChatChatsChatIdGet: vi.fn().mockResolvedValue({ data: {} }) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useGetChatById(42), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(chatApi.getChatByIdApiChatChatsChatIdGet).toHaveBeenCalledWith(42);
    });

    it('sets error state on failure', async () => {
        const chatApi = { getChatByIdApiChatChatsChatIdGet: vi.fn().mockRejectedValue(new Error('fail')) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useGetChatById(1), { wrapper });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
