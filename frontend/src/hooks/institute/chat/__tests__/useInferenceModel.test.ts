import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { createElement } from 'react';
import { useInferenceModel } from '../useInferenceModel';

type MessageDTO = { id: number; chat_id: number; role: string; content: string; model_key: string; adapter_version: number | null };

function createWrapper(messagesApi: { sendMessageApiChatChatsChatIdMessagesPost: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { chatApi: {} as never, messagesApi: messagesApi as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ChatApiContext.Provider, { value: contextValue }, children)) };
}

describe('useInferenceModel', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with correct params', async () => {
        const userMessage: MessageDTO = { id: 1, chat_id: 10, role: 'user', content: 'Hello', model_key: 'k', adapter_version: 1 };
        const messagesApi = { sendMessageApiChatChatsChatIdMessagesPost: vi.fn().mockResolvedValue({ data: userMessage }) };

        const { wrapper } = createWrapper(messagesApi);
        const { result } = renderHook(() => useInferenceModel(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ chatId: 10, modelKey: 'k', adapterVersion: 1, prompt: 'Hello' });
        });

        expect(messagesApi.sendMessageApiChatChatsChatIdMessagesPost).toHaveBeenCalledWith(10, {
            model_key: 'k',
            adapter_version: 1,
            prompt: 'Hello',
        });
    });

    it('appends the user message to the messages cache', async () => {
        const userMessage: MessageDTO = { id: 2, chat_id: 10, role: 'user', content: 'Hi', model_key: 'k', adapter_version: null };
        const messagesApi = { sendMessageApiChatChatsChatIdMessagesPost: vi.fn().mockResolvedValue({ data: userMessage }) };

        const { queryClient, wrapper } = createWrapper(messagesApi);
        queryClient.setQueryData<MessageDTO[]>(['messages', 10], []);

        const { result } = renderHook(() => useInferenceModel(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ chatId: 10, modelKey: 'k', adapterVersion: null, prompt: 'Hi' });
        });

        const cached = queryClient.getQueryData<MessageDTO[]>(['messages', 10]);
        expect(cached).toHaveLength(1);
        expect(cached?.[0]).toEqual(userMessage);
    });

    it('creates a new messages list when cache is empty', async () => {
        const userMessage: MessageDTO = { id: 1, chat_id: 5, role: 'user', content: 'Hey', model_key: 'k', adapter_version: null };
        const messagesApi = { sendMessageApiChatChatsChatIdMessagesPost: vi.fn().mockResolvedValue({ data: userMessage }) };

        const { queryClient, wrapper } = createWrapper(messagesApi);
        const { result } = renderHook(() => useInferenceModel(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ chatId: 5, modelKey: 'k', adapterVersion: null, prompt: 'Hey' });
        });

        expect(queryClient.getQueryData<MessageDTO[]>(['messages', 5])).toEqual([userMessage]);
    });

    it('invalidates chats query on success', async () => {
        const userMessage: MessageDTO = { id: 1, chat_id: 10, role: 'user', content: 'Hi', model_key: 'k', adapter_version: null };
        const messagesApi = { sendMessageApiChatChatsChatIdMessagesPost: vi.fn().mockResolvedValue({ data: userMessage }) };

        const { queryClient, wrapper } = createWrapper(messagesApi);
        const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');

        const { result } = renderHook(() => useInferenceModel(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ chatId: 10, modelKey: 'k', adapterVersion: null, prompt: 'Hi' });
        });

        expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['chats'] });
    });
});
