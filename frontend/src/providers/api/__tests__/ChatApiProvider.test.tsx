import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { ChatApiProvider } from '../ChatApiProvider';
import { ApiBasePathContext } from '../../../contexts/api/apiBasePathContext';
import { ChatApiContext } from '../../../contexts/api/chatApiContext';

vi.mock('../../../config/axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
}));

vi.mock('@isin/chat-service-client', () => ({
    Configuration: vi.fn().mockImplementation(function (this: object, opts: object) {
        Object.assign(this, opts);
    }),
    ChatApi: vi.fn().mockImplementation(function (this: object) {
        Object.assign(this, { _type: 'ChatApi' });
    }),
    MessagesApi: vi.fn().mockImplementation(function (this: object) {
        Object.assign(this, { _type: 'MessagesApi' });
    }),
}));

function TestConsumer() {
    return (
        <ChatApiContext.Consumer>
            {(value) => (
                <div>
                    <span data-testid="chat-api">{value?.chatApi ? 'present' : 'absent'}</span>
                    <span data-testid="messages-api">{value?.messagesApi ? 'present' : 'absent'}</span>
                </div>
            )}
        </ChatApiContext.Consumer>
    );
}

function renderProvider(basePath = '') {
    return render(
        createElement(ApiBasePathContext.Provider, { value: { basePath } },
            <ChatApiProvider>
                <TestConsumer />
            </ChatApiProvider>)
    );
}

describe('ChatApiProvider', () => {
    it('provides chatApi to consumers', () => {
        renderProvider();
        expect(screen.getByTestId('chat-api').textContent).toBe('present');
    });

    it('provides messagesApi to consumers', () => {
        renderProvider();
        expect(screen.getByTestId('messages-api').textContent).toBe('present');
    });

    it('renders children', () => {
        renderProvider();
        expect(screen.getByTestId('chat-api')).toBeTruthy();
    });

    it('creates Configuration with the provided basePath', async () => {
        const { Configuration } = await import('@isin/chat-service-client');
        renderProvider('http://custom-base');
        expect(vi.mocked(Configuration)).toHaveBeenCalledWith(
            expect.objectContaining({ basePath: 'http://custom-base' })
        );
    });

    it('recreates APIs when basePath changes', () => {
        const { rerender } = renderProvider('http://base-1');
        rerender(
            createElement(ApiBasePathContext.Provider, { value: { basePath: 'http://base-2' } },
                <ChatApiProvider>
                    <TestConsumer />
                </ChatApiProvider>)
        );
        expect(screen.getByTestId('chat-api').textContent).toBe('present');
    });
});
