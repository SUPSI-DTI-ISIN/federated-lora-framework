import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useApiBasePath } from '../useApiBasePath';
import { ApiBasePathContext } from '../../../contexts/api/apiBasePathContext';
import { createElement } from 'react';

const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(ApiBasePathContext.Provider, { value: { basePath: 'http://localhost:8081' } }, children);

describe('useApiBasePath', () => {
    it('returns the basePath from context', () => {
        const { result } = renderHook(() => useApiBasePath(), { wrapper });
        expect(result.current.basePath).toBe('http://localhost:8081');
    });

    it('throws when used outside ApiBasePathProvider', () => {
        expect(() => renderHook(() => useApiBasePath())).toThrow(
            'useApiBasePath must be used within ApiBasePathProvider'
        );
    });
});
