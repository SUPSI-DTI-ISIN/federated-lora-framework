import { describe, it, expect } from 'vitest';
import { ApiBasePathContext } from '../apiBasePathContext';

describe('ApiBasePathContext', () => {
    it('is defined', () => {
        expect(ApiBasePathContext).toBeDefined();
    });

    it('has undefined as default value', () => {
        expect((ApiBasePathContext as unknown as { _currentValue: unknown })._currentValue).toBeUndefined();
    });
});
