import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { AuthProviders } from '../AuthProviders';
import { SelectorRealmContext } from '../../../contexts/realm/selectorRealmContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('../../../config/axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
    setAuthToken: vi.fn(),
}));

vi.mock('../../../auth/auth', () => ({
    getOidcAuthConfiguration: vi.fn().mockReturnValue({
        authority: 'http://keycloak.test/realms/TestRealm',
        client_id: 'test-client',
        redirect_uri: 'http://localhost:3000',
    }),
}));

vi.mock('react-oidc-context', () => ({
    AuthProvider: ({ children }: { children: React.ReactNode }) => (
        <div data-testid="auth-provider">{children}</div>
    ),
    useAuth: vi.fn().mockReturnValue({
        isLoading: false,
        isAuthenticated: false,
        user: null,
        activeNavigator: undefined,
        error: undefined,
        signinRedirect: vi.fn(),
        signinSilent: vi.fn().mockResolvedValue(undefined),
        signoutRedirect: vi.fn(),
        removeUser: vi.fn(),
    }),
    hasAuthParams: vi.fn().mockReturnValue(false),
}));

function renderProviders(realm: string | undefined, children: React.ReactNode) {
    const queryClient = new QueryClient();
    const realmValue = { realm, setRealm: vi.fn(), pendingLogin: false, clearPendingLogin: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(SelectorRealmContext.Provider, { value: realmValue },
                <AuthProviders>{children}</AuthProviders>))
    );
}

describe('AuthProviders', () => {
    it('renders children', () => {
        renderProviders('TestRealm', <div data-testid="child">Child</div>);
        expect(screen.getByTestId('child')).toBeTruthy();
    });

    it('wraps children with AuthProvider', () => {
        renderProviders('TestRealm', <div data-testid="child">Child</div>);
        expect(screen.getByTestId('auth-provider')).toBeTruthy();
    });

    it('renders without crashing when realm is undefined', () => {
        expect(() => renderProviders(undefined, <span>test</span>)).not.toThrow();
    });

    it('passes realm to getOidcAuthConfiguration', async () => {
        const { getOidcAuthConfiguration } = await import('../../../auth/auth');
        renderProviders('MyRealm', <span>test</span>);
        expect(getOidcAuthConfiguration).toHaveBeenCalledWith('MyRealm');
    });
});
