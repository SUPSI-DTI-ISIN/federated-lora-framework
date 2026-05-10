import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useModelApi } from '../useModelApi';
import { ModelApiContext } from '../../../contexts/api/modelApiContext';
import { createElement } from 'react';

const mockModelApiValue = {
    adaptersApi: { _isAdaptersApi: true } as never,
};

const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(ModelApiContext.Provider, { value: mockModelApiValue }, children);

describe('useModelApi', () => {
    it('returns the context value when inside provider', () => {
        const { result } = renderHook(() => useModelApi(), { wrapper });
        expect(result.current.adaptersApi).toBeDefined();
    });

    it('throws when used outside ModelApiProvider', () => {
        expect(() => renderHook(() => useModelApi())).toThrow(
            'useModelApi must be used within ModelApiProvider'
        );
    });
});
