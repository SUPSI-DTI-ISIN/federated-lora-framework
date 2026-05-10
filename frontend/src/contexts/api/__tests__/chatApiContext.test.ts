import { describe, it, expect } from 'vitest';
import { ChatApiContext } from '../chatApiContext';

describe('ChatApiContext', () => {
    it('is defined', () => {
        expect(ChatApiContext).toBeDefined();
    });

    it('has undefined as default value', () => {
        expect((ChatApiContext as unknown as { _currentValue: unknown })._currentValue).toBeUndefined();
    });
});
