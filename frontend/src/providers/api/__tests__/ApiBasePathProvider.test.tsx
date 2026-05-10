import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { ApiBasePathProvider } from '../ApiBasePathProvider';
import { SelectorRealmContext } from '../../../contexts/realm/selectorRealmContext';
import { ApiBasePathContext } from '../../../contexts/api/apiBasePathContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('../../../utils/envUtils', () => ({
    isInDevelopmentEnvironment: vi.fn(),
    getDepartmentRealm: vi.fn().mockReturnValue('Department'),
}));

vi.mock('../../../hooks/department/institutes/useGetInstituteByName', () => ({
    useGetInstituteByName: vi.fn(),
}));

vi.mock('react-icons/cg', () => ({
    CgSpinner: () => <div data-testid="spinner" />,
}));

import { isInDevelopmentEnvironment, getDepartmentRealm } from '../../../utils/envUtils';
import { useGetInstituteByName } from '../../../hooks/department/institutes/useGetInstituteByName';

function TestConsumer() {
    return (
        <ApiBasePathContext.Consumer>
            {(value) => <span data-testid="base-path">{value?.basePath ?? 'no-value'}</span>}
        </ApiBasePathContext.Consumer>
    );
}

function renderProvider(realm: string | undefined, instituteResult: { data?: unknown; isLoading: boolean }) {
    vi.mocked(useGetInstituteByName).mockReturnValue(instituteResult as never);
    const queryClient = new QueryClient();
    const realmValue = { realm, setRealm: vi.fn(), pendingLogin: false, clearPendingLogin: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(SelectorRealmContext.Provider, { value: realmValue },
                <ApiBasePathProvider>
                    <TestConsumer />
                </ApiBasePathProvider>))
    );
}

describe('ApiBasePathProvider', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(getDepartmentRealm).mockReturnValue('Department');
    });

    it('returns empty basePath in development environment', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(true);
        renderProvider('TestRealm', { isLoading: false, data: { url: 'http://inst.local' } });
        expect(screen.getByTestId('base-path').textContent).toBe('');
    });

    it('returns empty basePath when realm is undefined', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(false);
        renderProvider(undefined, { isLoading: false });
        expect(screen.getByTestId('base-path').textContent).toBe('');
    });

    it('returns empty basePath when realm is the department realm', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(false);
        renderProvider('Department', { isLoading: false });
        expect(screen.getByTestId('base-path').textContent).toBe('');
    });

    it('returns institute url as basePath in production with non-department realm', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(false);
        renderProvider('TestRealm', { isLoading: false, data: { url: 'http://inst.local' } });
        expect(screen.getByTestId('base-path').textContent).toBe('http://inst.local');
    });

    it('shows spinner when loading institute and realm is not department', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(false);
        renderProvider('TestRealm', { isLoading: true });
        expect(screen.getByTestId('spinner')).toBeTruthy();
    });

    it('shows spinner when basePath is null (institute not yet loaded)', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(false);
        renderProvider('TestRealm', { isLoading: false, data: undefined });
        expect(screen.getByTestId('spinner')).toBeTruthy();
    });

    it('renders children when basePath is resolved', () => {
        vi.mocked(isInDevelopmentEnvironment).mockReturnValue(true);
        renderProvider('TestRealm', { isLoading: false, data: { url: 'http://inst.local' } });
        expect(screen.getByTestId('base-path')).toBeTruthy();
    });
});
