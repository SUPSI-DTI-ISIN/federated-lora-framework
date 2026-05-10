import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { createElement } from 'react';
import { useCreateChat } from '../useCreateChat';

function createWrapper(chatApi: { createChatApiChatChatsPost: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { chatApi: chatApi as never, messagesApi: {} as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ChatApiContext.Provider, { value: contextValue }, children)) };
}

describe('useCreateChat', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with the title', async () => {
        const newChat = { id: 1, title: 'New Chat', user_id: 'u-1', is_doing_inference: false };
        const chatApi = { createChatApiChatChatsPost: vi.fn().mockResolvedValue({ data: newChat }) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useCreateChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ title: 'New Chat' });
        });

        expect(chatApi.createChatApiChatChatsPost).toHaveBeenCalledWith({ title: 'New Chat' });
    });

    it('appends the new chat to the cache', async () => {
        const existing = [{ id: 1, title: 'Old', user_id: 'u-1', is_doing_inference: false }];
        const newChat = { id: 2, title: 'New', user_id: 'u-1', is_doing_inference: false };
        const chatApi = { createChatApiChatChatsPost: vi.fn().mockResolvedValue({ data: newChat }) };

        const { queryClient, wrapper } = createWrapper(chatApi);
        queryClient.setQueryData(['chats'], existing);

        const { result } = renderHook(() => useCreateChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ title: 'New' });
        });

        const cached = queryClient.getQueryData<typeof existing>(['chats']);
        expect(cached).toHaveLength(2);
        expect(cached?.[1]).toEqual(newChat);
    });

    it('creates a new list when cache is empty', async () => {
        const newChat = { id: 1, title: 'First', user_id: 'u-1', is_doing_inference: false };
        const chatApi = { createChatApiChatChatsPost: vi.fn().mockResolvedValue({ data: newChat }) };

        const { queryClient, wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useCreateChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ title: 'First' });
        });

        expect(queryClient.getQueryData(['chats'])).toEqual([newChat]);
    });

    it('works with null title', async () => {
        const newChat = { id: 1, title: null, user_id: 'u-1', is_doing_inference: false };
        const chatApi = { createChatApiChatChatsPost: vi.fn().mockResolvedValue({ data: newChat }) };

        const { wrapper } = createWrapper(chatApi);
        const { result } = renderHook(() => useCreateChat(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ title: null });
        });

        expect(chatApi.createChatApiChatChatsPost).toHaveBeenCalledWith({ title: null });
    });
});
