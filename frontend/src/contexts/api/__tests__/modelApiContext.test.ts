import { describe, it, expect } from 'vitest';
import { ModelApiContext } from '../modelApiContext';

describe('ModelApiContext', () => {
    it('is defined', () => {
        expect(ModelApiContext).toBeDefined();
    });

    it('has undefined as default value', () => {
        expect((ModelApiContext as unknown as { _currentValue: unknown })._currentValue).toBeUndefined();
    });
});
