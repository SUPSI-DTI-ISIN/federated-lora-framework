import { describe, it, expect } from 'vitest';
import { SelectorRealmContext } from '../selectorRealmContext';

describe('SelectorRealmContext', () => {
    it('is defined', () => {
        expect(SelectorRealmContext).toBeDefined();
    });

    it('has undefined as default value', () => {
        expect((SelectorRealmContext as unknown as { _currentValue: unknown })._currentValue).toBeUndefined();
    });
});
