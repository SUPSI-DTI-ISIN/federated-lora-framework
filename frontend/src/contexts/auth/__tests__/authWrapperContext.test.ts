import { describe, it, expect } from 'vitest';
import { AuthWrapperContext } from '../authWrapperContext';

describe('AuthWrapperContext', () => {
    it('is defined', () => {
        expect(AuthWrapperContext).toBeDefined();
    });

    it('has undefined as default value', () => {
        expect((AuthWrapperContext as unknown as { _currentValue: unknown })._currentValue).toBeUndefined();
    });
});
