import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useChatApi } from '../useChatApi';
import { ChatApiContext } from '../../../contexts/api/chatApiContext';
import { createElement } from 'react';

const mockChatApiValue = {
    chatApi: { _isChatApi: true } as never,
    messagesApi: { _isMessagesApi: true } as never,
};

const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(ChatApiContext.Provider, { value: mockChatApiValue }, children);

describe('useChatApi', () => {
    it('returns the context value when inside provider', () => {
        const { result } = renderHook(() => useChatApi(), { wrapper });
        expect(result.current.chatApi).toBeDefined();
        expect(result.current.messagesApi).toBeDefined();
    });

    it('throws when used outside ChatApiProvider', () => {
        expect(() => renderHook(() => useChatApi())).toThrow(
            'useChatApi must be used within ChatApiProvider'
        );
    });
});
