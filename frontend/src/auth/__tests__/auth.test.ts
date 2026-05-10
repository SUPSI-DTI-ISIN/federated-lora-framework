import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('oidc-client-ts', () => {
    const WebStorageStateStore = vi.fn().mockImplementation(function (this: object) {
        Object.assign(this, { _isStore: true });
    });
    return { WebStorageStateStore };
});

vi.mock('../../utils/envUtils', () => ({
    getKeycloakUrl: vi.fn().mockReturnValue('http://keycloak.test'),
    getClientId: vi.fn().mockReturnValue('my-client'),
    getFrontendUrl: vi.fn().mockReturnValue('http://localhost:3000'),
}));

type OidcConfig = Record<string, unknown>;

describe('getOidcAuthConfiguration', () => {
    beforeEach(() => {
        vi.resetModules();
    });

    it('returns undefined when realm is undefined', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        expect(getOidcAuthConfiguration(undefined)).toBeUndefined();
    });

    it('returns a configuration object when realm is provided', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm');
        expect(config).toBeDefined();
    });

    it('builds authority from keycloak URL and realm', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        expect(config?.authority).toBe('http://keycloak.test/realms/TestRealm');
    });

    it('sets client_id from getClientId', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        expect(config?.client_id).toBe('my-client');
    });

    it('sets redirect_uri from getFrontendUrl', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        expect(config?.redirect_uri).toBe('http://localhost:3000');
    });

    it('sets post_logout_redirect_uri from getFrontendUrl', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        expect(config?.post_logout_redirect_uri).toBe('http://localhost:3000');
    });

    it('sets response_type to code', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        expect(config?.response_type).toBe('code');
    });

    it('sets scope to openid profile email', async () => {
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        expect(config?.scope).toBe('openid profile email');
    });

    it('creates a WebStorageStateStore for userStore', async () => {
        const { WebStorageStateStore } = await import('oidc-client-ts');
        const { getOidcAuthConfiguration } = await import('../auth');
        getOidcAuthConfiguration('TestRealm');
        expect(WebStorageStateStore).toHaveBeenCalledWith({ store: window.localStorage });
    });

    it('onSigninCallback replaces browser history state', async () => {
        const replaceStateSpy = vi.spyOn(window.history, 'replaceState').mockImplementation(() => {});
        const { getOidcAuthConfiguration } = await import('../auth');
        const config = getOidcAuthConfiguration('TestRealm') as OidcConfig;
        const callback = config?.onSigninCallback as ((user: unknown) => void) | undefined;
        callback?.(undefined);
        expect(replaceStateSpy).toHaveBeenCalledWith({}, document.title, window.location.pathname);
        replaceStateSpy.mockRestore();
    });
});
