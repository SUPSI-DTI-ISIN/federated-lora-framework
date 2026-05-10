import { describe, it, expect } from 'vitest';
import { getFederatedLearningJobSseUrl, getChatSseUrl } from '../sseUrls';

describe('getFederatedLearningJobSseUrl', () => {
    it('returns the correct federated learning SSE URL', () => {
        expect(getFederatedLearningJobSseUrl()).toBe(
            '/api_federated_learning_management/jobs/sse'
        );
    });
});

describe('getChatSseUrl', () => {
    it('builds the correct chat SSE URL', () => {
        expect(getChatSseUrl('http://localhost:8081', 'user-123')).toBe(
            'http://localhost:8081/api_chat/chats/sse/user-123'
        );
    });

    it('uses the provided basePath', () => {
        const url = getChatSseUrl('https://api.example.com', 'abc-456');
        expect(url).toContain('https://api.example.com');
    });

    it('includes the userId in the URL', () => {
        const url = getChatSseUrl('http://localhost', 'my-user-id');
        expect(url).toContain('my-user-id');
    });

    it('includes the SSE path segment', () => {
        const url = getChatSseUrl('http://localhost', 'u-1');
        expect(url).toContain('/api_chat/chats/sse/');
    });
});
