import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatApiContext } from '../../../../contexts/api/chatApiContext';
import { AuthWrapperContext } from '../../../../contexts/auth/authWrapperContext';
import { ApiBasePathContext } from '../../../../contexts/api/apiBasePathContext';
import { createElement } from 'react';
import { useChatSse } from '../useChatSse';

vi.mock('../../../../utils/sse/sseUrls', () => ({
    getChatSseUrl: vi.fn().mockReturnValue('http://localhost/api_chat/chats/sse/user-123'),
}));

const mockEventSource = {
    addEventListener: vi.fn(),
    close: vi.fn(),
    onerror: null as ((e: Event) => void) | null,
};

type MessageHandler = (e: MessageEvent) => void;

function getHandler(eventName: string): MessageHandler {
    const call = (mockEventSource.addEventListener.mock.calls as Array<[string, MessageHandler]>)
        .find(([event]) => event === eventName);
    return call![1];
}

const mockUser = { profile: { sub: 'user-123' } };
const mockAuthValue = {
    user: mockUser as never,
    isLoading: false,
    isAuthenticated: true,
    isDepartmentAdmin: false,
    login: vi.fn(),
    logout: vi.fn(),
};
const mockBasePathValue = { basePath: 'http://localhost' };

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return {
        queryClient,
        wrapper: ({ children }: { children: React.ReactNode }) =>
            createElement(QueryClientProvider, { client: queryClient },
                createElement(AuthWrapperContext.Provider, { value: mockAuthValue },
                    createElement(ApiBasePathContext.Provider, { value: mockBasePathValue },
                        createElement(ChatApiContext.Provider, {
                            value: { chatApi: {} as never, messagesApi: {} as never },
                        }, children)))),
    };
}

describe('useChatSse', () => {
    let MockEventSource: ReturnType<typeof vi.fn>;

    beforeEach(() => {
        vi.clearAllMocks();
        MockEventSource = vi.fn().mockImplementation(function (this: typeof mockEventSource) {
            Object.assign(this, mockEventSource);
            return this;
        });
        vi.stubGlobal('EventSource', MockEventSource);
    });

    afterEach(() => vi.unstubAllGlobals());

    it('creates an EventSource when user is authenticated', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useChatSse(), { wrapper });
        expect(MockEventSource).toHaveBeenCalledOnce();
    });

    it('registers inference_job_success event listener', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useChatSse(), { wrapper });
        expect(mockEventSource.addEventListener).toHaveBeenCalledWith('inference_job_success', expect.any(Function));
    });

    it('registers inference_job_failure event listener', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useChatSse(), { wrapper });
        expect(mockEventSource.addEventListener).toHaveBeenCalledWith('inference_job_failure', expect.any(Function));
    });

    it('closes the EventSource on unmount', () => {
        const { wrapper } = createWrapper();
        const { unmount } = renderHook(() => useChatSse(), { wrapper });
        unmount();
        expect(mockEventSource.close).toHaveBeenCalledOnce();
    });

    it('does not create EventSource when user has no sub', () => {
        const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
        const noSubAuth = { ...mockAuthValue, user: { profile: {} } as never };
        const wrapper = ({ children }: { children: React.ReactNode }) =>
            createElement(QueryClientProvider, { client: queryClient },
                createElement(AuthWrapperContext.Provider, { value: noSubAuth },
                    createElement(ApiBasePathContext.Provider, { value: mockBasePathValue },
                        createElement(ChatApiContext.Provider, {
                            value: { chatApi: {} as never, messagesApi: {} as never },
                        }, children))));

        renderHook(() => useChatSse(), { wrapper });
        expect(MockEventSource).not.toHaveBeenCalled();
    });

    it('updates messages cache on inference_job_success', () => {
        type MessageDTO = { id: number; chat_id: number; role: string; content: string; model_key: string; adapter_version: number | null };
        const { queryClient, wrapper } = createWrapper();
        const assistantMessage: MessageDTO = { id: 99, chat_id: 10, role: 'assistant', content: 'Hi', model_key: 'k', adapter_version: null };
        queryClient.setQueryData<MessageDTO[]>(['messages', 10], []);
        queryClient.setQueryData(['chats'], [{ id: 10, is_doing_inference: true }]);

        renderHook(() => useChatSse(), { wrapper });

        getHandler('inference_job_success')({ data: JSON.stringify(assistantMessage) } as MessageEvent);

        const messages = queryClient.getQueryData<MessageDTO[]>(['messages', 10]);
        expect(messages).toHaveLength(1);
        expect(messages?.[0]).toEqual(assistantMessage);
    });

    it('updates chats cache is_doing_inference on inference_job_success', () => {
        type ChatDTO = { id: number; is_doing_inference: boolean };
        const { queryClient, wrapper } = createWrapper();
        const assistantMessage = { id: 99, chat_id: 10, role: 'assistant', content: 'Hi', model_key: 'k', adapter_version: null };
        queryClient.setQueryData<ChatDTO[]>(['chats'], [{ id: 10, is_doing_inference: true }, { id: 11, is_doing_inference: true }]);
        queryClient.setQueryData(['messages', 10], []);

        renderHook(() => useChatSse(), { wrapper });

        getHandler('inference_job_success')({ data: JSON.stringify(assistantMessage) } as MessageEvent);

        const chats = queryClient.getQueryData<ChatDTO[]>(['chats']);
        expect(chats?.[0].is_doing_inference).toBe(false);
        expect(chats?.[1].is_doing_inference).toBe(true);
    });

    it('does not crash on invalid JSON in success handler', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useChatSse(), { wrapper });
        expect(() => getHandler('inference_job_success')({ data: 'invalid-json' } as MessageEvent)).not.toThrow();
    });

    it('invalidates chats and messages queries on inference_job_failure', async () => {
        const { queryClient, wrapper } = createWrapper();
        const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');

        renderHook(() => useChatSse(), { wrapper });

        await getHandler('inference_job_failure')({ data: JSON.stringify({ result: { chat_id: 10 } }) } as MessageEvent);

        expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['chats'] });
        expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['messages', 10], refetchType: 'all' });
    });

    it('does not crash on invalid JSON in failure handler', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useChatSse(), { wrapper });
        expect(() => getHandler('inference_job_failure')({ data: 'invalid-json' } as MessageEvent)).not.toThrow();
    });

    it('triggers onerror handler without crashing', () => {
        const { wrapper } = createWrapper();
        renderHook(() => useChatSse(), { wrapper });
        const instance = MockEventSource.mock.instances[0] as typeof mockEventSource;
        expect(() => instance.onerror?.(new Event('error'))).not.toThrow();
    });
});
