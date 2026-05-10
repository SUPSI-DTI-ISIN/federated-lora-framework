import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { createElement } from 'react';
import { AuthWrapperProvider } from '../AuthWrapperProvider';
import { SelectorRealmContext } from '../../../contexts/realm/selectorRealmContext';
import { AuthWrapperContext } from '../../../contexts/auth/authWrapperContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('../../../config/axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
    setAuthToken: vi.fn(),
}));

vi.mock('react-oidc-context', () => ({
    useAuth: vi.fn(),
    hasAuthParams: vi.fn().mockReturnValue(false),
}));

import { useAuth, hasAuthParams } from 'react-oidc-context';
import { setAuthToken } from '../../../config/axios';

const mockSigninRedirect = vi.fn().mockResolvedValue(undefined);
const mockSigninSilent = vi.fn().mockResolvedValue(undefined);
const mockSignoutRedirect = vi.fn().mockResolvedValue(undefined);
const mockRemoveUser = vi.fn();

function makeAuth(overrides: Partial<ReturnType<typeof useAuth>> = {}): ReturnType<typeof useAuth> {
    return {
        isLoading: false,
        isAuthenticated: false,
        user: null,
        activeNavigator: undefined,
        error: undefined,
        signinRedirect: mockSigninRedirect,
        signinSilent: mockSigninSilent,
        signoutRedirect: mockSignoutRedirect,
        removeUser: mockRemoveUser,
        ...overrides,
    } as never;
}

function TestConsumer() {
    return (
        <AuthWrapperContext.Consumer>
            {(value) => (
                <div>
                    <span data-testid="is-loading">{String(value?.isLoading)}</span>
                    <span data-testid="is-authenticated">{String(value?.isAuthenticated)}</span>
                    <span data-testid="is-admin">{String(value?.isDepartmentAdmin)}</span>
                    <span data-testid="user">{value?.user ? 'present' : 'null'}</span>
                    <button onClick={() => value?.login()}>Login</button>
                    <button onClick={() => value?.logout()}>Logout</button>
                </div>
            )}
        </AuthWrapperContext.Consumer>
    );
}

function renderProvider(authOverrides: Partial<ReturnType<typeof useAuth>> = {}, realm = 'TestRealm') {
    vi.mocked(useAuth).mockReturnValue(makeAuth(authOverrides));
    const queryClient = new QueryClient();
    const realmValue = {
        realm,
        setRealm: vi.fn(),
        pendingLogin: false,
        clearPendingLogin: vi.fn(),
    };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(SelectorRealmContext.Provider, { value: realmValue },
                <AuthWrapperProvider>
                    <TestConsumer />
                </AuthWrapperProvider>))
    );
}

describe('AuthWrapperProvider', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(hasAuthParams).mockReturnValue(false);
    });

    it('renders children', () => {
        renderProvider();
        expect(screen.getByTestId('is-loading')).toBeTruthy();
    });

    it('exposes isLoading false when auth is not loading', () => {
        renderProvider({ isLoading: false });
        expect(screen.getByTestId('is-loading').textContent).toBe('false');
    });

    it('exposes isLoading true when auth is loading', () => {
        renderProvider({ isLoading: true });
        expect(screen.getByTestId('is-loading').textContent).toBe('true');
    });

    it('exposes isLoading true when signinRedirect is active', () => {
        renderProvider({ isLoading: false, activeNavigator: 'signinRedirect' });
        expect(screen.getByTestId('is-loading').textContent).toBe('true');
    });

    it('exposes isLoading true when signinSilent is active', () => {
        renderProvider({ isLoading: false, activeNavigator: 'signinSilent' });
        expect(screen.getByTestId('is-loading').textContent).toBe('true');
    });

    it('exposes isLoading true when signoutRedirect is active', () => {
        renderProvider({ isLoading: false, activeNavigator: 'signoutRedirect' });
        expect(screen.getByTestId('is-loading').textContent).toBe('true');
    });

    it('exposes isAuthenticated false when not authenticated', () => {
        renderProvider({ isAuthenticated: false });
        expect(screen.getByTestId('is-authenticated').textContent).toBe('false');
    });

    it('exposes isAuthenticated true when authenticated with user, profile and realm', () => {
        renderProvider({
            isAuthenticated: true,
            user: { profile: { sub: 'u-1' } } as never,
        });
        expect(screen.getByTestId('is-authenticated').textContent).toBe('true');
    });

    it('exposes isAuthenticated false when realm is missing', () => {
        vi.mocked(useAuth).mockReturnValue(makeAuth({
            isAuthenticated: true,
            user: { profile: { sub: 'u-1' } } as never,
        }));
        const queryClient = new QueryClient();
        const realmValue = { realm: undefined, setRealm: vi.fn(), pendingLogin: false, clearPendingLogin: vi.fn() };

        render(
            createElement(QueryClientProvider, { client: queryClient },
                createElement(SelectorRealmContext.Provider, { value: realmValue },
                    <AuthWrapperProvider><TestConsumer /></AuthWrapperProvider>))
        );

        expect(screen.getByTestId('is-authenticated').textContent).toBe('false');
    });

    it('exposes isDepartmentAdmin false when realm_admin is not set', () => {
        renderProvider({
            isAuthenticated: true,
            user: { profile: { sub: 'u-1', realm_admin: false } } as never,
        });
        expect(screen.getByTestId('is-admin').textContent).toBe('false');
    });

    it('exposes isDepartmentAdmin true when realm_admin is true', () => {
        renderProvider({
            isAuthenticated: true,
            user: { profile: { sub: 'u-1', realm_admin: true } } as never,
        });
        expect(screen.getByTestId('is-admin').textContent).toBe('true');
    });

    it('exposes user as null when not authenticated', () => {
        renderProvider({ user: null });
        expect(screen.getByTestId('user').textContent).toBe('null');
    });

    it('exposes user when authenticated', () => {
        renderProvider({ user: { profile: { sub: 'u-1' } } as never });
        expect(screen.getByTestId('user').textContent).toBe('present');
    });

    it('calls signinRedirect on login', async () => {
        renderProvider();
        await act(async () => {
            screen.getByText('Login').click();
        });
        expect(mockSigninRedirect).toHaveBeenCalledOnce();
    });

    it('calls signoutRedirect on logout', async () => {
        renderProvider({ user: { profile: { sub: 'u-1' } } as never });
        await act(async () => {
            screen.getByText('Logout').click();
        });
        expect(mockSignoutRedirect).toHaveBeenCalledOnce();
    });

    it('sets auth token when user access_token changes', () => {
        renderProvider({ user: { access_token: 'my-token', profile: {} } as never });
        expect(setAuthToken).toHaveBeenCalledWith('my-token');
    });

    it('clears auth token when user is null', () => {
        renderProvider({ user: null });
        expect(setAuthToken).toHaveBeenCalledWith(null);
    });

    it('attempts signinSilent when no pending login and no user', () => {
        renderProvider({ isLoading: false, user: null });
        expect(mockSigninSilent).toHaveBeenCalled();
    });

    it('calls signinRedirect when pendingLogin is true and no user', () => {
        vi.mocked(useAuth).mockReturnValue(makeAuth({ isLoading: false, user: null }));
        const queryClient = new QueryClient();
        const realmValue = { realm: 'TestRealm', setRealm: vi.fn(), pendingLogin: true, clearPendingLogin: vi.fn() };

        render(
            createElement(QueryClientProvider, { client: queryClient },
                createElement(SelectorRealmContext.Provider, { value: realmValue },
                    <AuthWrapperProvider><TestConsumer /></AuthWrapperProvider>))
        );

        expect(mockSigninRedirect).toHaveBeenCalled();
    });

    it('clears realm and pendingLogin on auth error', () => {
        const setRealm = vi.fn();
        const clearPendingLogin = vi.fn();
        vi.mocked(useAuth).mockReturnValue(makeAuth({ error: { message: 'auth error', source: 'unknown' } as never }));
        const queryClient = new QueryClient();
        const realmValue = { realm: 'TestRealm', setRealm, pendingLogin: false, clearPendingLogin };

        render(
            createElement(QueryClientProvider, { client: queryClient },
                createElement(SelectorRealmContext.Provider, { value: realmValue },
                    <AuthWrapperProvider><TestConsumer /></AuthWrapperProvider>))
        );

        expect(clearPendingLogin).toHaveBeenCalled();
        expect(setRealm).toHaveBeenCalledWith(undefined);
    });
});
