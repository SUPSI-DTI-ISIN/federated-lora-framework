import {describe, it, expect, vi} from 'vitest';
import {renderHook} from '@testing-library/react';
import {useSelectorRealm} from '../useSelectorRealm';
import {SelectorRealmContext} from '../../../contexts/realm/selectorRealmContext';
import {createElement} from 'react';

const mockRealmValue = {
    realm: 'TestRealm',
    setRealm: vi.fn(),
    pendingLogin: false,
    clearPendingLogin: vi.fn(),
};

const wrapper = ({children}: { children: React.ReactNode }) =>
    createElement(SelectorRealmContext.Provider, {value: mockRealmValue}, children);

describe('useSelectorRealm', () => {
    it('returns the context value when inside provider', () => {
        const {result} = renderHook(() => useSelectorRealm(), {wrapper});
        expect(result.current.realm).toBe('TestRealm');
        expect(result.current.pendingLogin).toBe(false);
    });

    it('throws when used outside SelectorRealmContext', () => {
        expect(() => renderHook(() => useSelectorRealm())).toThrow(
            'useSelectorRealm must be used within SelectorRealmContext'
        );
    });
});
