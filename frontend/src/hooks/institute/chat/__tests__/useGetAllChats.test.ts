import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { createElement } from 'react';
import { useGetAllChats } from '../useGetAllChats';

function createWrapper(chatApi: { listChatsApiChatChatsGet: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { chatApi: chatApi as never, messagesApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ChatApiContext.Provider, { value: contextValue }, children)) };
}

describe('useGetAllChats', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns chats on success', async () => {
        const chats = [{ id: 1, title: 'Chat 1', user_id: 'u-1', is_doing_inference: false }];
        const chatApi = { listChatsApiChatChatsGet: vi.fn().mockResolvedValue({ data: chats }) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useGetAllChats(), { wrapper });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(chats);
    });

    it('sets error state on failure', async () => {
        const chatApi = { listChatsApiChatChatsGet: vi.fn().mockRejectedValue(new Error('fail')) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useGetAllChats(), { wrapper });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
