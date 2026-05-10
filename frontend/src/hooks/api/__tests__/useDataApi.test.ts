import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useDataApi } from '../useDataApi';
import { DataApiContext } from '../../../contexts/api/dataApiContext';
import { createElement } from 'react';

const mockDataApiValue = {
    documentsApi: { _isDocumentsApi: true } as never,
    sectionsApi: { _isSectionsApi: true } as never,
};

const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(DataApiContext.Provider, { value: mockDataApiValue }, children);

describe('useDataApi', () => {
    it('returns the context value when inside provider', () => {
        const { result } = renderHook(() => useDataApi(), { wrapper });
        expect(result.current.documentsApi).toBeDefined();
        expect(result.current.sectionsApi).toBeDefined();
    });

    it('throws when used outside DataApiProvider', () => {
        expect(() => renderHook(() => useDataApi())).toThrow(
            'useDataApi must be used within DataApiProvider'
        );
    });
});
