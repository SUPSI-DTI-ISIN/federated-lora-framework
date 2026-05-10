import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useAuthWrapper } from '../useAuthWrapper';
import { AuthWrapperContext } from '../../../contexts/auth/authWrapperContext';
import { createElement } from 'react';

const mockAuthValue = {
    user: null,
    isLoading: false,
    isAuthenticated: false,
    isDepartmentAdmin: false,
    login: () => {},
    logout: () => {},
};

const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(AuthWrapperContext.Provider, { value: mockAuthValue }, children);

describe('useAuthWrapper', () => {
    it('returns the context value when inside provider', () => {
        const { result } = renderHook(() => useAuthWrapper(), { wrapper });
        expect(result.current.isLoading).toBe(false);
        expect(result.current.isAuthenticated).toBe(false);
        expect(result.current.user).toBeNull();
    });

    it('throws when used outside AuthWrapperProvider', () => {
        expect(() => renderHook(() => useAuthWrapper())).toThrow(
            'useAuthWrapper must be used within AuthWrapperProvider'
        );
    });
});
