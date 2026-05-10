import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { createElement } from 'react';
import { useDeleteChat } from '../useDeleteChat';

function createWrapper(chatApi: { deleteChatApiChatChatsChatIdDelete: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { chatApi: chatApi as never, messagesApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ChatApiContext.Provider, { value: contextValue }, children)) };
}

describe('useDeleteChat', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with the correct chatId', async () => {
        const chatApi = { deleteChatApiChatChatsChatIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useDeleteChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(3);
        });

        expect(chatApi.deleteChatApiChatChatsChatIdDelete).toHaveBeenCalledWith(3);
    });

    it('removes the deleted chat from the cache', async () => {
        const chats = [{ id: 1, title: 'A' }, { id: 2, title: 'B' }];
        const chatApi = { deleteChatApiChatChatsChatIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { queryClient, wrapper } = createWrapper(chatApi);
        queryClient.setQueryData(['chats'], chats);

        const { result } = renderHook(() => useDeleteChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        const cached = queryClient.getQueryData<typeof chats>(['chats']);
        expect(cached).toHaveLength(1);
        expect(cached?.[0].id).toBe(2);
    });

    it('returns undefined when cache is empty', async () => {
        const chatApi = { deleteChatApiChatChatsChatIdDelete: vi.fn().mockResolvedValue({ data: undefined }) };

        const { queryClient, wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useDeleteChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        expect(queryClient.getQueryData(['chats'])).toBeUndefined();
    });
});
