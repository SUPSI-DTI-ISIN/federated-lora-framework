import { describe, it, expect } from 'vitest';
import { DataApiContext } from '../dataApiContext';

describe('DataApiContext', () => {
    it('is defined', () => {
        expect(DataApiContext).toBeDefined();
    });

    it('has undefined as default value', () => {
        expect((DataApiContext as unknown as { _currentValue: unknown })._currentValue).toBeUndefined();
    });
});
